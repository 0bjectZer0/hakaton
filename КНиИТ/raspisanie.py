"""Расписание одного семестра. Запуск примера: python raspisanie.py"""

from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta
from itertools import combinations


@dataclass(frozen=True, order=True)
class Slot:
    day: date
    period: int  # Номер пары по единой сетке звонков факультета


@dataclass(frozen=True)
class Course:
    subject: str
    kind: str
    tracks: tuple[str, ...]  # Кто приходит на одно и то же занятие
    hours: int  # Академические контактные часы для каждого участника

    rooms: tuple[str, ...] = ()
    weeks: frozenset[str] = frozenset(("Ч", "З"))


@dataclass
class Teacher:
    name: str
    available: set[Slot]  # Свободные пары на конкретные даты семестра
    courses: list[Course]


@dataclass(frozen=True)
class Lesson:
    slot: Slot
    teacher: str
    course: Course
    room: str = ""


def schedule(teachers, tracks, hours_per_pair=2, group_busy=None, allocator=None, teacher_bookings=None):
    """Вернуть занятия и остаток свободных пар. Исходные данные сохраняются."""
    tracks = tuple(tracks)
    if not tracks or len(set(tracks)) != len(tracks):
        raise ValueError("Укажите уникальные идентификаторы групп.")
    if type(hours_per_pair) is not int or hours_per_pair < 1:
        raise ValueError("Длительность пары должна быть положительным целым.")
    free = {}
    occupied = {track: set((group_busy or {}).get(track, ())) for track in tracks}
    daily_counts = Counter({key: len(intervals) for key, intervals in (teacher_bookings or {}).items()})
    pending = []
    lessons = []
    for teacher in teachers:
        if teacher.name in free:
            raise ValueError(f"Повторяется идентификатор преподавателя: {teacher.name}")
        free[teacher.name] = set(teacher.available)
        for course in teacher.courses:
            if not course.tracks or not set(course.tracks) <= set(tracks):
                raise ValueError(f"Проверьте направления: {course.subject}")
            if type(course.hours) is not int or course.hours < 0 or course.hours % hours_per_pair:
                raise ValueError(f"{course.subject}: часы должны задавать целое число пар.")
            if course.hours:
                pending.append((teacher.name, course))
        required = sum(c.hours // hours_per_pair for c in teacher.courses)
        if required > len(free[teacher.name]):
            raise ValueError(f"{teacher.name}: требуется {required} пар, доступно {len(free[teacher.name])}.")

    pending.sort(key=lambda item: (len(free[item[0]]), -len(item[1].tracks)))
    stack = []
    index = 0
    while index < len(pending):
        name, course = pending[index]
        if len(stack) == index:
            options = free[name].difference(*(occupied[t] for t in course.tracks))
            if len(course.weeks) < 2:
                from rooms import week_type
                options = {s for s in options if week_type(s.day) in course.weeks}
            limit = {s.day: 5 - daily_counts[name, s.day] for s in options}
            order = {4: 0, 3: 1, 2: 2, 1: 3, 5: 4}  # Сначала дополняем день с одной или двумя парами.
            candidates = sorted((s for s in options if limit[s.day] > 0),
                                key=lambda s: (order[limit[s.day]], s))
            count = course.hours // hours_per_pair
            if allocator is None:
                choices = (tuple((s, "") for s in slots)
                           for slots in combinations(candidates, count)
                           if count == 1 or all(n <= limit[d] for d, n in Counter(s.day for s in slots).items()))
            else:
                choices = allocator.choices(candidates, count, course.rooms, limit)
            stack.append([choices, ()])
        choices, previous = stack[index]
        if previous:
            if allocator:
                allocator.mark(previous, False)
            previous = tuple(s for s, _ in previous)
            for slot in previous:
                daily_counts[name, slot.day] -= 1
            free[name].update(previous)
            for track in course.tracks:
                occupied[track].difference_update(previous)
        slots = next(choices, None)
        if slots is None:
            stack.pop()
            index -= 1
            if index < 0:
                raise ValueError("Нагрузку невозможно разместить в заданных окнах.")
            continue
        assignment = slots
        if allocator:
            allocator.mark(assignment, True)
        slots = tuple(s for s, _ in assignment)
        for slot in slots:
            daily_counts[name, slot.day] += 1
        free[name].difference_update(slots)
        for track in course.tracks:
            occupied[track].update(slots)
        stack[index][1] = assignment
        index += 1
    for (name, course), (_, slots) in zip(pending, stack):
        lessons.extend(Lesson(slot, name, course, room) for slot, room in slots)
    return sorted(lessons, key=lambda lesson: (lesson.slot, lesson.teacher)), free


def example():
    # Источник ФИО, дисциплин и занятых пар группы 321 (обновление 24.09.2026):
    # https://www.sgu.ru/schedule/knt/do/321
    # Часы, объединение направлений и доступные интервалы — учебный пример.
    tracks = tuple(f"Н{i}" for i in range(1, 7))
    wed = date(2026, 11, 25)
    thu = wed + timedelta(days=1)
    def windows(wednesday, thursday):
        return {Slot(day, p) for day, periods in ((wed, wednesday), (thu, thursday))
                for p in periods}

    tyapaev = "Тяпаев Ливат Борисович"
    dmitriev = "Дмитриев Павел Олегович"
    timofeeva = "Тимофеева Надежда Евгеньевна"
    # Занятость именно у группы 321 в среду и четверг, номера пар с единицы.
    busy_321 = {
        tyapaev: windows([], []),
        dmitriev: windows([2, 3], [3, 4]),
        timofeeva: windows([], [1, 2, 3, 4, 5]),
    }
    teachers = [
        Teacher(tyapaev, windows([1, 2, 3], [1, 2]) - busy_321[tyapaev], [
            Course("Теория автоматов", "Лекция", tracks, 4),
            Course("Теория автоматов", "Практика", (tracks[0],), 2),
        ]),
        Teacher(dmitriev, windows([1, 2, 4], [1, 2, 3]) - busy_321[dmitriev], [
            Course("Сети и телекоммуникации", "Практика", (tracks[1],), 2),
            Course("Робототехника", "Практика", (tracks[2],), 2),
            Course("Проектная практика", "Практика", (tracks[3],), 2),
        ]),
        Teacher(timofeeva, windows([2, 3, 4], [5, 6, 7]) - busy_321[timofeeva], [
            Course("Организация ЭВМ и систем", "Практика", (tracks[4],), 2),
            Course("Робототехника", "Практика", (tracks[5],), 2),
        ]),
    ]
    lessons, free = schedule(teachers, tracks)
    print("Учебный расчёт для шести условных направлений, 25–26 ноября 2026 г.")
    print("Учтены опубликованные пары группы 321: https://www.sgu.ru/schedule/knt/do/321")
    print("Доступность вне этих пар и нагрузка заданы для примера.")
    for lesson in lessons:
        c = lesson.course
        print(f"{lesson.slot.day:%d.%m}  пара {lesson.slot.period}  {lesson.teacher}  "
              f"{c.kind}: {c.subject}  ({', '.join(c.tracks)})")
    for name, slots in free.items():
        windows = ", ".join(f"{s.day:%d.%m} пара {s.period}" for s in sorted(slots))
        print(f"{name} — свободно: {windows or 'нет свободных пар'}")


if __name__ == "__main__":
    from faculty import main
    main()
