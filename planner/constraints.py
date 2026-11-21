"""Жёсткие ограничения, индекс поиска и независимая проверка готового варианта."""
from collections import Counter, defaultdict
from functools import lru_cache


def people(lesson):
    return (("teacher", lesson.teacher), *(("group", group) for group in lesson.groups))


def seats_needed(problem, lesson):
    sizes = [problem.groups[group].size for group in lesson.groups]
    return None if None in sizes else sum(sizes)


def fits(problem, lesson, room, seats):
    return (problem.subjects[lesson.subject].features <= room.features
            and (room.capacity is None or seats is not None and seats <= room.capacity))


def time_allowed(availability, weeks, day, period, duration):
    if availability is None:
        return True
    return all((week, day, p) in availability for week in weeks for p in range(period, period + duration))


def in_bounds(problem, lesson, p):
    return (type(p.day) is int and 0 <= p.day < problem.days
            and type(p.period) is int and 0 <= p.period
            and p.period + lesson.duration <= len(problem.bells[lesson.bell]))


def span(problem, lesson, p):
    bells = problem.bells[lesson.bell]
    return bells[p.period][0], bells[p.period + lesson.duration - 1][1]


@lru_cache(maxsize=4096)
def minute_mask(start, end):
    """Полуоткрытый интервал целых минут, общий для всех сеток звонков."""
    return ((1 << (end - start)) - 1) << start


class State:
    """Хранит занятые минуты и число пар по ресурсам. add/remove используют проверенные ходы."""

    def __init__(self, problem):
        self.problem = problem
        self.placements = {}
        self._busy = {}
        self._daily = Counter()
        self._subgroups = {}
        self._people = {k: people(lesson) for k, lesson in problem.lessons.items()}
        self._room_keys = {k: tuple(("room", atom) for atom in room.physical_keys)
                           for k, room in problem.rooms.items()}
        self._eligible_rooms = {}
        for lesson in problem.lessons.values():
            seats = seats_needed(problem, lesson)
            self._eligible_rooms[lesson.id] = frozenset(
                k for k in lesson.rooms if fits(problem, lesson, problem.rooms[k], seats))

    def statically_allowed(self, lesson, p):
        return (in_bounds(self.problem, lesson, p) and p.room in self._eligible_rooms[lesson.id]
                and all(time_allowed(a, lesson.weeks, p.day, p.period, lesson.duration)
                        for a in (lesson.available, self.problem.teachers[lesson.teacher].available,
                                  self.problem.rooms[p.room].available)))

    def can_place(self, lesson, p):
        return self.statically_allowed(lesson, p) and self.can_place_known(lesson, p)

    def can_place_known(self, lesson, p):
        """Только динамические ограничения для предварительно проверенного домена."""
        if lesson.id in self.placements:
            return False
        mask = minute_mask(*span(self.problem, lesson, p))
        attendees = self._people[lesson.id]
        limit = self.problem.daily_limit - lesson.duration
        for week in lesson.weeks:
            if any(self._busy.get((r, week, p.day), 0) & mask for r in self._room_keys[p.room]):
                return False
            for r in attendees:
                key = r, week, p.day
                if self._busy.get(key, 0) & mask:
                    occupants = self._subgroups.get((key, mask, lesson.subject, lesson.duration))
                    if not occupants or not lesson.subgroup or lesson.subgroup in occupants:
                        return False
                elif self._daily[key] > limit:
                    return False
        return True

    def add(self, lesson, p):
        if not self.can_place(lesson, p):
            raise ValueError(f"{lesson.id}: недопустимое назначение {p}")
        self._update(lesson, p, 1)
        self.placements[lesson.id] = p

    def remove(self, lesson, p):
        if self.placements.get(lesson.id) != p:
            raise ValueError(f"{lesson.id}: назначение для отмены не найдено")
        self._update(lesson, p, -1)
        del self.placements[lesson.id]

    def _update(self, lesson, p, sign):
        mask = minute_mask(*span(self.problem, lesson, p))
        attendees = self._people[lesson.id]
        for week in lesson.weeks:
            for resource in attendees + self._room_keys[p.room]:
                key = resource, week, p.day
                if resource[0] == "group" and lesson.subgroup:
                    bucket = key, mask, lesson.subject, lesson.duration
                    occupants = self._subgroups.setdefault(bucket, set())
                    if sign > 0:
                        occupants.add(lesson.subgroup)
                        if len(occupants) > 1:
                            continue
                    else:
                        occupants.remove(lesson.subgroup)
                        if occupants:
                            continue
                        del self._subgroups[bucket]
                self._busy[key] = self._busy.get(key, 0) ^ mask
                if resource[0] != "room":
                    self._daily[key] += sign * lesson.duration


def validate(problem, placements, require_complete=True):
    """Аудит итоговых назначений, включая все пересечения интервалов. Индекс State не используется."""
    errors = []
    if require_complete:
        errors.extend(f"{key}: занятие не размещено" for key in problem.lessons if key not in placements)
    intervals = defaultdict(list)
    day_load = Counter()
    counted_groups = set()
    for ident, p in placements.items():
        lesson = problem.lessons.get(ident)
        if lesson is None:
            errors.append(f"{ident}: неизвестное занятие")
            continue
        if not in_bounds(problem, lesson, p):
            errors.append(f"{ident}: день или блок пар выходит за сетку")
            continue
        room = problem.rooms.get(p.room)
        if room is None:
            errors.append(f"{ident}: неизвестная аудитория {p.room}")
            continue
        if p.room not in lesson.rooms or not fits(problem, lesson, room, seats_needed(problem, lesson)):
            errors.append(f"{ident}: аудитория {p.room} не подходит по списку, оборудованию или вместимости")
        for label, availability in (("занятие", lesson.available), ("преподаватель", problem.teachers[lesson.teacher].available),
                                    ("аудитория", room.available)):
            if not time_allowed(availability, lesson.weeks, p.day, p.period, lesson.duration):
                errors.append(f"{ident}: {label} недоступно в выбранное время")
        start, end = span(problem, lesson, p)
        attendees = people(lesson)
        for week in lesson.weeks:
            for resource in attendees:
                if resource[0] == "group":
                    slot = resource, week, p.day, start, end
                    if slot in counted_groups:
                        continue
                    counted_groups.add(slot)
                day_load[resource, week, p.day] += lesson.duration
            for resource in (*attendees, *(("room", k) for k in room.physical_keys)):
                intervals[resource, week, p.day].append((start, end, ident))
    for resource, count in day_load.items():
        if count > problem.daily_limit:
            errors.append(f"{resource}: {count} пар при лимите {problem.daily_limit}")
    for resource, values in intervals.items():
        active = []
        for start, end, ident in sorted(values):
            active = [(stop, key) for stop, key in active if stop > start]
            for _, key in active:
                first, second = problem.lessons[key], problem.lessons[ident]
                if (resource[0][0] == "group" and first.subject == second.subject
                        and first.subgroup and second.subgroup and first.subgroup != second.subgroup
                        and first.duration == second.duration and span(problem, first, placements[key]) == (start, end)):
                    continue
                errors.append(f"{resource}: пересечение {key} и {ident}")
            active.append((end, ident))
    return errors
