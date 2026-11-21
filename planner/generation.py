"""Построение допустимой части расписания и локальное перемещение занятий."""
from functools import lru_cache
from math import log2
from time import perf_counter

from .constraints import State, fits, seats_needed, time_allowed
from .evaluation import DayIndex, day_features
from .models import Placement
from .weights import KEYS


class Domains:
    """Хранит общие статические окна, без декартова произведения времени на кабинеты."""

    def __init__(self, problem):
        self.problem = problem
        self.slots = {}
        self.rooms = {}

        @lru_cache(maxsize=8192)
        def times(teacher, available, weeks, duration, periods):
            return tuple((d, p) for p in range(periods-duration+1) for d in range(problem.days)
                         if time_allowed(teacher, weeks, d, p, duration)
                         and time_allowed(available, weeks, d, p, duration))

        for lesson in problem.lessons.values():
            self.slots[lesson.id] = times(problem.teachers[lesson.teacher].available, lesson.available,
                                          lesson.weeks, lesson.duration, len(problem.bells[lesson.bell]))
            seats = seats_needed(problem, lesson)
            self.rooms[lesson.id] = tuple(r for r in lesson.rooms
                                          if fits(problem, lesson, problem.rooms[r], seats))


class Search:
    def __init__(self, domains, rng, randomness, previous):
        self.domains = domains
        self.problem = domains.problem
        self.rng = rng
        self.randomness = randomness
        self.previous = previous
        self.state = State(self.problem)
        self.days = DayIndex(self.problem)
        self.iterations = 0

    def set_weights(self, weights):
        self.span_weight = weights.get("start_spread_hours", 0)
        self.course_weight = weights.get("course_time", 0)
        group = tuple(weights[k] for k in KEYS[:5])
        teacher = tuple(weights[k] for k in KEYS[5:])

        @lru_cache(maxsize=32768)
        def cost(intervals, role):
            coefficients = group if role == "group" else teacher
            score = sum(x * y for x, y in zip(day_features(intervals), coefficients))
            if role == "group" and weights.get("gap_hours"):
                score += weights["gap_hours"] * sum((b[0]-a[1])/60 for a, b in zip(intervals, intervals[1:])
                                                    if b[0]-a[1] >= 60)
            return score

        self.day_cost = cost
        self.bounds = lru_cache(maxsize=512)(self.days.start_bounds)

    def add(self, lesson, p):
        self.state.add(lesson, p)
        self.days.update(lesson, p, True)
        self.bounds.cache_clear()

    def remove(self, lesson, p):
        self.state.remove(lesson, p)
        self.days.update(lesson, p, False)
        self.bounds.cache_clear()

    def delta(self, lesson, day, period):
        interval = self.days.interval(lesson, period)
        total = self.course_weight * self.days.course_costs[lesson.id][period]
        for resource in self.days.resources(lesson):
            for week in lesson.weeks:
                old = self.days.entries.get((resource, week, day), ())
                if resource[0] == "group" and interval in old:
                    continue
                new = tuple(sorted((*old, interval)))
                total += self.day_cost(new, resource[0]) - self.day_cost(old, resource[0])
                if self.span_weight and resource[0] == "group":
                    bounds = self.bounds(resource[1], week, day)
                    if bounds:
                        lo, hi = bounds
                        before = max(0, lo-old[0][0], old[0][0]-hi) if old else 0
                        after = max(0, lo-new[0][0], new[0][0]-hi)
                        total += self.span_weight * (after-before) / 60
        # Штраф относится только к поиску. Итоговая оценка сравнима между запусками.
        for variant in self.previous:
            other = variant.get(lesson.id)
            if other and (day, period) == (other.day, other.period):
                total += 8 * len(lesson.weeks)
        return total

    def choose(self, lesson, deadline, original=None):
        times = self.domains.slots[lesson.id]
        rooms = self.domains.rooms[lesson.id]
        if not rooms or not times:
            return original
        if self.randomness:
            times = list(times)
            self.rng.shuffle(times)
        best = original
        threshold = self.delta(lesson, original.day, original.period) if original else float("inf")
        feasible = 0
        # В больших задачах достаточно сравнить несколько допустимых времён.
        # Для отсутствующего назначения продолжаем поиск до конца домена.
        sample = 5 if len(self.problem.lessons) > 1000 else 16
        for day, period in times:
            if perf_counter() >= deadline:
                break
            if original and (day, period) == (original.day, original.period):
                continue
            for room in rooms:
                p = Placement(day, period, room)
                if not time_allowed(self.problem.rooms[room].available, lesson.weeks, day, period, lesson.duration):
                    continue
                if self.state.can_place_known(lesson, p):
                    score = self.delta(lesson, day, period) + self.randomness * self.rng.random()
                    if score < threshold:
                        threshold, best = score, p
                    feasible += 1
                    break
            if feasible >= sample:
                break
        return best

    def construct(self, deadline):
        def priority(lesson):
            size = len(self.domains.slots[lesson.id]) * len(self.domains.rooms[lesson.id])
            # Сначала малая область и максимальная совокупная нагрузка на ресурсы.
            constraint = log2(1 + size) - log2(len(lesson.weeks)*lesson.duration*len(lesson.groups))
            return constraint + self.randomness * 1.5 * self.rng.random()

        for lesson in sorted(self.problem.lessons.values(), key=priority):
            if perf_counter() >= deadline:
                break
            p = self.choose(lesson, deadline)
            if p is not None:
                self.add(lesson, p)

    def improve(self, limit, deadline):
        lessons = list(self.problem.lessons.values())
        while self.iterations < limit and perf_counter() < deadline and lessons:
            if self.randomness:
                self.rng.shuffle(lessons)
            changed = False
            for lesson in lessons:
                if self.iterations >= limit or perf_counter() >= deadline:
                    return
                self.iterations += 1
                old = self.state.placements.get(lesson.id)
                if old is not None:
                    self.remove(lesson, old)
                new = self.choose(lesson, deadline, old)
                if new is not None:
                    self.add(lesson, new)
                changed |= old != new
            if not changed:
                return
