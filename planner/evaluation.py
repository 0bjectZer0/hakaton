"""Независимая оценка расписания по дням групп и преподавателей."""
from collections import Counter, defaultdict
from functools import lru_cache


@lru_cache(maxsize=32768)
def day_features(intervals):
    """Окно — перерыв от 60 минут, перегруженный день — от пяти пар."""
    length = sum(item[2] for item in intervals)
    gaps = sum(b[0] - a[1] >= 60 for a, b in zip(intervals, intervals[1:]))
    return gaps, int(length >= 5), int(length == 1), int(length > 0), length * length


class DayIndex:
    def __init__(self, problem):
        self.problem = problem
        self.entries = {}
        self.counts = Counter()
        self.course_penalty = 0
        self.course_costs = {}
        for lesson in problem.lessons.values():
            courses = [problem.groups[g].course for g in lesson.groups]
            junior = sum(c in (1, 2) for c in courses)
            senior = sum(c is not None and c >= 3 for c in courses)
            count = len(problem.bells[lesson.bell])
            # Нулевая нумерация. При короткой сетке старшие ориентируются на последнюю пару.
            late = min(4, count - 1)
            costs = [junior * max(0, p-2) + senior * max(0, late-p) for p in range(count)]
            self.course_costs[lesson.id] = tuple(sum(costs[p:p+lesson.duration]) * len(lesson.weeks)
                                                 for p in range(count - lesson.duration + 1))

    def interval(self, lesson, period):
        bell = self.problem.bells[lesson.bell]
        return bell[period][0], bell[period + lesson.duration - 1][1], lesson.duration

    def start_bounds(self, group, week, exclude_day=None):
        starts = [entries[0][0] for d in range(self.problem.days) if d != exclude_day
                  if (entries := self.entries.get((("group", group), week, d)))]
        if starts:
            return min(starts), max(starts)

    @staticmethod
    def resources(lesson):
        return (("teacher", lesson.teacher), *(("group", g) for g in lesson.groups))

    def update(self, lesson, placement, add):
        cost = self.course_costs[lesson.id][placement.period]
        self.course_penalty += cost if add else -cost
        entry = self.interval(lesson, placement.period)
        for resource in self.resources(lesson):
            for week in lesson.weeks:
                key = resource, week, placement.day
                if resource[0] == "group":
                    slot = key, entry
                    self.counts[slot] += 1 if add else -1
                    if self.counts[slot] > int(add):
                        continue
                    if not add:
                        del self.counts[slot]
                day = list(self.entries.get(key, ()))
                if add:
                    day.append(entry)
                    day.sort()
                else:
                    day.remove(entry)
                if day:
                    self.entries[key] = tuple(day)
                else:
                    self.entries.pop(key)

    def metrics(self):
        names = ("gaps", "overloaded", "single", "active", "imbalance")
        totals = {prefix+key: 0 for prefix in ("", "teacher_") for key in (*names, "empty")}
        load = defaultdict(int)
        for ((role, rid), week, day), entries in self.entries.items():
            prefix = "teacher_" if role == "teacher" else ""
            for key, value in zip(names, day_features(entries)):
                totals[prefix+key] += value
            load[prefix, rid, week] += sum(entry[2] for entry in entries)
        for (prefix, _, _), total in load.items():
            totals[prefix+"imbalance"] -= total ** 2 / self.problem.days
        for prefix, resources in (("", self.problem.groups), ("teacher_", self.problem.teachers)):
            totals[prefix+"empty"] = 2 * self.problem.days * len(resources) - totals[prefix+"active"]
            totals[prefix+"imbalance"] = round(max(0, totals[prefix+"imbalance"]), 6)
        totals["start_spread_hours"] = sum((end-start) / 60 for group in self.problem.groups
                                          for w in (0, 1) if (bounds := self.start_bounds(group, w))
                                          for start, end in [bounds])
        totals["gap_hours"] = sum((b[0]-a[1]) / 60 for ((role, _), _, _), day in self.entries.items()
                                  if role == "group" for a, b in zip(day, day[1:]) if b[0]-a[1] >= 60)
        totals["course_time"] = self.course_penalty
        return totals


def interval_tokens(problem, placements):
    return {(lid, week, pos.day, pos.period + offset)
            for lid, pos in placements.items() for week in problem.lessons[lid].weeks
            for offset in range(problem.lessons[lid].duration)}


def jaccard(left, right):
    size = len(left) + len(right)
    intersection = len(left & right)
    return intersection / (size - intersection) if size else 1.0


def similarity(problem, a, b):
    """Коэффициент Жаккара для назначенных пар; замена одной аудитории даёт сходство 1."""
    return jaccard(interval_tokens(problem, a), interval_tokens(problem, b))


def evaluate(problem, placements):
    days = DayIndex(problem)
    for lid, pos in placements.items():
        days.update(problem.lessons[lid], pos, True)
    return days.metrics()


def penalty_breakdown(weights, metrics):
    return {name: weight * metrics[name] for name, weight in weights.items()}
