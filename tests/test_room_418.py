from dataclasses import replace
from datetime import date
import unittest

from planner.constraints import State, validate
from planner.models import Placement
from planner.sgu import load_sgu
from raspisanie_sgu import ROOT, faculty_modules, read_json
from rooms import RoomCalendar


class Room418Tests(unittest.TestCase):
    def test_saved_and_reversible_bookings(self):
        room = "12 корпус, 418"
        day = date(2027, 2, 1)
        calendar = RoomCalendar([(room, day.isoformat(), 500, 590)])
        self.assertEqual(calendar.free_count(room, day, 550, 600), 1)
        calendar.mark(room, day, 500, 590, True)
        self.assertTrue(calendar.busy(room, day, 550, 600))
        calendar.mark(room, day, 500, 590, False)
        self.assertEqual(calendar.free_count(room, day, 500, 590), 1)
        self.assertEqual(calendar.free_count(room, day, 590, 600), 2)
        self.assertEqual(calendar.free_count("8 корпус, 418", day, 500, 590), 1)

    def test_parallel_placements(self):
        problem, info = load_sgu(ROOT, faculty_modules, read_json)
        base = next(l for l in problem.lessons.values()
                    if any(info.room_names[r] == "12 корпус, 418" for r in l.rooms))
        rooms = tuple(r for r in base.rooms if info.room_names[r] == "12 корпус, 418")
        self.assertEqual(len(set(rooms)), 2)
        groups, teachers = list(problem.groups), list(problem.teachers)
        lessons = {str(i): replace(base, id=str(i), groups=(groups[i],), teacher=teachers[i],
                                   available=None, weeks=(0,), rooms=rooms) for i in range(3)}
        problem = replace(problem, lessons=lessons)
        a, b = (Placement(0, 0, r) for r in rooms)
        state = State(problem)
        state.add(lessons["0"], a)
        for field in ("teacher", "groups"):
            clash = replace(lessons["1"], **{field: getattr(lessons["0"], field)})
            conflict_problem = replace(problem, lessons={**lessons, "1": clash})
            checker = State(conflict_problem)
            checker.add(lessons["0"], a)
            self.assertFalse(checker.can_place(clash, b))
            self.assertTrue(validate(conflict_problem, {"0": a, "1": b}, False))
        state.add(lessons["1"], b)
        self.assertFalse(validate(problem, state.placements, False))
        for p in (a, b):
            self.assertFalse(state.can_place(lessons["2"], p))
            self.assertTrue(validate(problem, {**state.placements, "2": p}))
        state.remove(lessons["0"], a)
        self.assertTrue(state.can_place(lessons["2"], a))
