"""Интеграционные и негативные проверки. Запуск: python -m unittest discover -s tests -v"""
import json
import shutil
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from planner.constraints import validate
from planner.evaluation import evaluate, penalty_breakdown, similarity
from planner.loader import load_problem
from planner.models import Group, Lesson, Placement, Problem, Room, Subject, Teacher
from planner.optimization import Config, generate_variants
from planner.weights import PROFILES, adapt_weights


def index(items):
    return {item.id: item for item in items}


def fixture(lessons, *, days=2, periods=4, teachers=None, rooms=None, subjects=None):
    bell = tuple((480 + 100 * p, 570 + 100 * p) for p in range(periods))
    return Problem(
        index(Group(g, 12) for lesson in lessons for g in lesson.groups),
        index(teachers if teachers is not None else [Teacher(l.teacher) for l in lessons]),
        index(rooms if rooms is not None else [Room("R", 60, keys=("R",))]),
        index(subjects if subjects is not None else [Subject(l.subject) for l in lessons]),
        index(lessons), days, periods, 5, {"main": bell},
    )


def event(name, *, group=None, teacher=None, rooms=("R",), **fields):
    return Lesson(name, "S", teacher or "T" + name, (group or "G" + name,), rooms, **fields)


def windows(*periods, days=(0,), weeks=(0, 1)):
    return frozenset((w, d, p) for w in weeks for d in days for p in periods)


def solve(problem, **settings):
    config = dict(seed=7, attempts=1, variants=1, time_limit=30, max_iterations=30, randomness=0.2)
    config.update(settings)
    return generate_variants(problem, Config(**config))[0]


class SchedulingTests(unittest.TestCase):
    def test_parallel_subgroups_keep_resource_conflicts_and_count_one_period(self):
        from planner.constraints import State
        a, b = Placement(0, 0, "A"), Placement(0, 0, "B")
        lessons = [event("a", group="G", rooms=("A",), subgroup=1),
                   event("b", group="G", rooms=("A", "B"), subgroup=2)]
        p = replace(fixture(lessons, rooms=[Room("A"), Room("B")]), daily_limit=1)
        state = State(p)
        state.add(lessons[0], a)
        self.assertFalse(state.can_place(lessons[1], a))
        state.add(lessons[1], b)
        self.assertFalse(validate(p, state.placements))
        self.assertEqual(evaluate(p, state.placements)["single"], 2)
        state.remove(lessons[0], a)
        self.assertTrue(state.can_place(lessons[0], a))
        for change in (dict(subgroup=1), dict(subgroup=None), dict(teacher=lessons[0].teacher)):
            other = replace(lessons[1], **change)
            bad = replace(p, lessons=index([lessons[0], other]))
            state = State(bad)
            state.add(lessons[0], a)
            self.assertFalse(state.can_place(other, b))
            self.assertTrue(validate(bad, {"a": a, "b": b}))

    def test_course_time_is_a_preference(self):
        lessons = [event("junior"), event("senior"), event("forced", available=windows(0))]
        p = fixture(lessons, days=1, periods=6)
        courses = {"Gjunior": 2, "Gsenior": 3, "Gforced": 4}
        p = replace(p, groups={k: replace(g, course=courses[k]) for k, g in p.groups.items()})
        result = solve(p)
        self.assert_complete(p, result)
        self.assertLessEqual(result.placements["junior"].period, 2)
        self.assertGreaterEqual(result.placements["senior"].period, 4)
        self.assertEqual(result.placements["forced"].period, 0)
        self.assertEqual(result.metrics["course_time"], 8)

    def test_compact_prefers_close_starts_and_shorter_gaps(self):
        problem = fixture([event(str(i), group="G") for i in range(3)], periods=5)
        def metrics(second_period, next_start):
            return evaluate(problem, {"0": Placement(0, 0, "R"),
                                      "1": Placement(0, second_period, "R"),
                                      "2": Placement(1, next_start, "R")})
        aligned = metrics(2, 0)
        for dispersed in (metrics(3, 0), metrics(2, 3)):
            self.assertEqual(aligned["gaps"], dispersed["gaps"])
            self.assertEqual(aligned["active"], dispersed["active"])
            self.assertLess(sum(penalty_breakdown(PROFILES["compact"], aligned).values()),
                            sum(penalty_breakdown(PROFILES["compact"], dispersed).values()))

    def assert_complete(self, problem, result):
        self.assertFalse(result.missing)
        self.assertFalse(result.violations)
        self.assertEqual(set(result.placements), set(problem.lessons))
        self.assertEqual(validate(problem, result.placements), [])
        self.assertEqual(result.metrics, evaluate(problem, result.placements))
        self.assertAlmostEqual(result.baseline_score,
                               sum(penalty_breakdown(PROFILES["compromise"], result.metrics).values()))

    def test_01_smallest_lesson(self):
        problem = fixture([event("a")], days=1, periods=1)
        result = solve(problem)
        self.assert_complete(problem, result)
        self.assertEqual(result.placements["a"], Placement(0, 0, "R"))

    def test_02_large_problem(self):
        # 1200 занятий, 100 преподавателей, 100 групп и 100 аудиторий.
        # Сертификат выполнимости задан независимо уникальным окном каждого занятия.
        rooms = [Room(f"R{i}", 40, keys=(f"R{i}",)) for i in range(100)]
        events = [
            event(f"{i}-{j}", group=f"G{i}", teacher=f"T{i}", rooms=(f"R{i}",),
                  available=windows(j % 4, days=(j // 4,)))
            for i in range(100) for j in range(12)
        ]
        problem = fixture(events, days=3, rooms=rooms)
        result = solve(problem, max_iterations=1, time_limit=60)
        self.assert_complete(problem, result)
        for i in range(100):
            for j in range(12):
                self.assertEqual(result.placements[f"{i}-{j}"], Placement(j // 4, j % 4, f"R{i}"))

    def test_03_too_few_rooms(self):
        problem = fixture([event("a"), event("b")], days=1, periods=1)
        result = solve(problem)
        self.assertEqual(len(result.missing), 1)
        self.assertFalse(result.violations)
        self.assertTrue(validate(problem, result.placements))
        double_booked = {name: Placement(0, 0, "R") for name in problem.lessons}
        self.assertTrue(validate(problem, double_booked, require_complete=False))

    def test_04_only_one_computer_lab(self):
        rooms = [Room("PC", 30, frozenset({"pc"}), ("PC",)), Room("R", 60, keys=("R",))]
        problem = fixture([event("a", rooms=("R", "PC")), event("b", rooms=("R", "PC"))],
                          periods=2, days=1, rooms=rooms, subjects=[Subject("S", frozenset({"pc"}))])
        result = solve(problem)
        self.assert_complete(problem, result)
        self.assertEqual({p.room for p in result.placements.values()}, {"PC"})
        self.assertEqual({p.period for p in result.placements.values()}, {0, 1})

    def test_05_availability_on_each_required_week(self):
        allowed = {(0, 0, 0), (0, 0, 2), (1, 0, 2)}
        problem = fixture([event("a", teacher="T")], teachers=[Teacher("T", frozenset(allowed))])
        result = solve(problem)
        self.assert_complete(problem, result)
        self.assertEqual(result.placements["a"].period, 2)
        self.assertTrue(validate(problem, {"a": Placement(0, 0, "R")}))

    def test_06_opposite_week_parities_can_share_a_slot(self):
        events = [event("a", group="G", teacher="T", weeks=(0,)), event("b", group="G", teacher="T", weeks=(1,))]
        problem = fixture(events, days=1, periods=1)
        result = solve(problem)
        self.assert_complete(problem, result)
        self.assertEqual(result.placements["a"], result.placements["b"])
        same_parity = fixture([events[0], replace(events[1], weeks=(0,))], days=1, periods=1)
        self.assertTrue(validate(same_parity, result.placements))

    def test_07_joint_lecture(self):
        lecture = replace(event("L"), groups=("G1", "G2"))
        events = [lecture, event("P", group="G2", rooms=("Q",))]
        rooms = [Room("R", 30, keys=("R",)), Room("Q", 20, keys=("Q",))]
        problem = fixture(events, days=1, periods=2, rooms=rooms)
        result = solve(problem)
        self.assert_complete(problem, result)
        self.assertNotEqual(result.placements["P"].period, result.placements["L"].period)
        small = replace(problem, rooms={**problem.rooms, "R": replace(rooms[0], capacity=23)})
        self.assertTrue(validate(small, result.placements))

    def test_08_lab_needs_two_consecutive_periods(self):
        events = [event("L", group="G", duration=2, available=windows(1, 2)),
                  event("P", group="G", available=windows(0))]
        problem = fixture(events, days=1, periods=3)
        result = solve(problem)
        self.assert_complete(problem, result)
        self.assertEqual(result.placements["L"], Placement(0, 1, "R"))
        bad = dict(result.placements, L=Placement(0, 2, "R"))
        self.assertTrue(validate(problem, bad))
        fragmented = fixture([replace(events[0], available=windows(0, 2))], days=1, periods=3)
        self.assertEqual(len(solve(fragmented).missing), 1)

    def test_09_impossible_teacher_load(self):
        events = [event(str(i), teacher="T", group=f"G{i}") for i in range(3)]
        problem = replace(fixture(events, days=1, periods=4), daily_limit=2)
        result = solve(problem)
        self.assertEqual(len(result.missing), 1)
        self.assertFalse(validate(problem, result.placements, require_complete=False))
        self.assertTrue(validate(problem, {str(i): Placement(0, i, "R") for i in range(3)}))

    def test_10_feasible_but_forced_gap(self):
        events = [event("a", group="G", available=windows(0)),
                  event("b", group="G", available=windows(3))]
        problem = fixture(events, days=1)
        result = solve(problem)
        self.assert_complete(problem, result)
        self.assertGreater(result.metrics["gaps"], 0)
        self.assertGreater(result.baseline_score, 0)

    def test_11_conflicting_preferences_and_diversity(self):
        events = [event(str(i), group="G", teacher="T") for i in range(6)]
        problem = fixture(events, days=4, periods=5)
        config = Config(seed=23, variants=4, attempts=5, randomness=0.7, max_iterations=180, time_limit=20)
        results = generate_variants(problem, config)
        self.assertGreater(len(results), 1)
        for i, result in enumerate(results):
            self.assert_complete(problem, result)
            self.assertEqual(similarity(problem, result.placements, result.placements), 1.0)
            for prior in results[:i]:
                self.assertLess(similarity(problem, result.placements, prior.placements), 1.0)
        # Сравним две заведомо допустимые сетки одной нагрузки:
        # 5+1 пар в два дня либо по две пары в три дня.
        compact = {str(i): Placement(i // 5, i % 5, "R") for i in range(6)}
        even = {str(i): Placement(i // 2, i % 2, "R") for i in range(6)}
        self.assertFalse(validate(problem, compact))
        self.assertFalse(validate(problem, even))
        self.assertLess(len({p.day for p in compact.values()}), len({p.day for p in even.values()}))
        self.assertGreater(sum(p.day == 0 for p in compact.values()), sum(p.day == 0 for p in even.values()))
        compact_metrics, even_metrics = evaluate(problem, compact), evaluate(problem, even)
        def penalty(profile, metrics):
            return sum(penalty_breakdown(PROFILES[profile], metrics).values())
        self.assertLess(penalty("compact", compact_metrics), penalty("compact", even_metrics))
        self.assertGreater(penalty("balance", compact_metrics), penalty("balance", even_metrics))

    def test_12_adaptive_weights(self):
        problem = fixture([event("a", group="G", available=windows(0)), event("b", group="G", available=windows(3))])
        fixed, adaptive = [solve(problem, adaptive=flag, max_iterations=150) for flag in (False, True)]
        self.assert_complete(problem, fixed)
        self.assert_complete(problem, adaptive)
        base = dict(fixed.weights)
        changed = adapt_weights(dict(base), fixed.metrics)
        self.assertGreater(changed["gaps"], base["gaps"])
        self.assertEqual(fixed.weights, base)
        self.assertEqual(fixed.baseline_score, adaptive.baseline_score)
        self.assertEqual(fixed.adaptive_weights, fixed.weights)
        self.assertNotEqual(adaptive.adaptive_weights, adaptive.weights)

    def test_cross_bell_and_shared_room_components(self):
        rooms = [Room("A", 40, keys=("A",)), Room("AB", 40, keys=("A", "B"))]
        events = [event("a", rooms=("A",)), replace(event("b", rooms=("AB",)), bell="branch")]
        problem = fixture(events, periods=2, rooms=rooms)
        problem = replace(problem, bells={**problem.bells, "branch": ((400, 479), (520, 590))})
        self.assertTrue(validate(problem, {"a": Placement(0, 0, "A"), "b": Placement(0, 1, "AB")}))
        self.assertFalse(validate(problem, {"a": Placement(0, 0, "A"), "b": Placement(0, 0, "AB")}))

    def test_json_rejects_invalid_reference(self):
        path = ROOT / "examples"
        self.assertTrue(load_problem(path).lessons)
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            for name in ("groups", "teachers", "subjects", "lessons", "rooms"):
                shutil.copy(path / f"{name}.json", directory)
            filename = directory / "lessons.json"
            data = json.loads(filename.read_text(encoding="utf-8"))
            data["lessons"][0]["teacher"] = "unregistered_teacher"
            filename.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_problem(directory)

    def test_similarity_does_not_count_room_changes_as_different_timetables(self):
        problem = fixture([event("a", rooms=("R", "Q"))])
        first = {"a": Placement(0, 0, "R")}
        self.assertEqual(similarity(problem, first, {"a": Placement(0, 0, "Q")}), 1)
        self.assertEqual(similarity(problem, first, {"a": Placement(0, 1, "R")}), 0)
        self.assertEqual(similarity(problem, {}, {}), 1)

    def test_forced_solution_is_not_duplicated_four_times(self):
        problem = fixture([event("a")], days=1, periods=1)
        config = Config(seed=1, variants=4, attempts=4, time_limit=5, max_iterations=20)
        results = generate_variants(problem, config)
        self.assertEqual(len(results), 1)
        self.assert_complete(problem, results[0])


if __name__ == "__main__":
    unittest.main()
