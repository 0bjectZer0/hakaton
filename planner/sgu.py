"""Преобразование нагрузки СГУ в независимую от CLI модель двух недель."""
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
import re

from fortnight import prepare
from rooms import REMOTE, ROOMS, booking_session, minutes
from .models import Group, Teacher, Room, Subject, Lesson, Problem


@dataclass
class SourceInfo:
    monday: date | None = None
    # lesson id -> вид занятия. Для пользовательского JSON вид может входить в название.
    kinds: dict = field(default_factory=dict)
    room_names: dict = field(default_factory=dict)
    issues: dict = field(default_factory=dict)
    assumed: int = 0


def recurrence_counts(hours, options):
    """Подобрать кратности дней, точно покрывающие заданные часы. Одно занятие = 2 часа."""
    if hours is None:
        return [None]
    pairs = hours // 2
    counts = Counter(opt[3] for opt in options if opt[3] > 0)
    if pairs > sum(opt[3] for opt in options):
        return []
    paths = {0: ()}
    for count, available in sorted(counts.items(), reverse=True):
        for total, path in list(paths.items()):
            for copies in range(1, 1 + min(available, (pairs-total)//count)):
                target = total + count * copies
                if target not in paths or len(path) + copies < len(paths[target]):
                    paths[target] = path + (count,) * copies
    return paths.get(pairs, ())


def load_sgu(root, load_modules, read_json):
    monday, requests, catalog, dates, grids = prepare(root, load_modules, read_json)
    info = SourceInfo(monday)
    groups = {f"{dept} / {g}": Group(f"{dept} / {g}", None, course)
              for dept, gs in catalog.items() for g, course in gs.items()}
    teachers, subjects, lessons, rooms, bells = {}, {}, {}, {}, {}
    grid_ids, grid_for, period_for = {}, {}, {}
    for dept, grid in grids.items():
        idx = grid_ids.setdefault(grid, str(len(grid_ids) + 1))
        grid_for[dept] = idx
        bells[idx] = tuple((minutes(a), minutes(b)) for a, b in grid)
        period_for[dept] = {a: i for i, (a, _) in enumerate(grid)}

    availability_sets = {}
    with booking_session() as (calendar, _):
        for request_id, (row, weeks, candidates, options, hours) in enumerate(requests, 1):
            dept, targets, teacher, kind, subject = row
            grid_id = grid_for[dept]
            teachers.setdefault(teacher, Teacher(teacher))
            subjects.setdefault(subject, Subject(subject))
            room_ids = []
            for name in candidates:
                # Номер пары зависит от сетки звонков; общий физический ключ связывает две сетки.
                room_id = f"{name} @{grid_id}"
                if name == REMOTE:
                    room_ids.append(room_id)
                    info.room_names[room_id] = name
                    rooms[room_id] = Room(room_id, virtual=True)
                    continue
                room_cls = ROOMS[name]
                # Параллельные занятия занимают независимые места с одним названием аудитории.
                for seat in range(room_cls.parallel_classes):
                    rid = f"{room_id} #{seat + 1}" if seat else room_id
                    room_ids.append(rid)
                    if rid in rooms:
                        continue
                    info.room_names[rid] = name
                    allowed = frozenset((w, d, p) for w, week in enumerate(("Ч", "З"))
                                        for d in range(7) for p, (start, end) in enumerate(bells[grid_id])
                                        if all(calendar.free_count(k, day, start, end) > seat
                                               for day in dates[dept][d, week] for k in room_cls.keys))
                    keys = tuple(f"{k} #{seat + 1}" for k in room_cls.keys) if seat else room_cls.keys
                    rooms[rid] = Room(rid, keys=keys, available=allowed)
            week_ids = tuple(i for i, week in enumerate(("Ч", "З")) if week in weeks)
            parts = recurrence_counts(hours, options)
            # Сохраняем и заведомо неразмещаемый спрос для отчёта о полноте.
            for part_id, count in enumerate(parts or [None], 1):
                lid = f"{request_id}.{part_id}"
                slots = frozenset((week, d, period_for[dept][start]) for d, start, _, n in options
                                  if parts and (count is None or count == n) for week in week_ids)
                if not room_ids:
                    info.issues[lid] = "Требуется аудитория"
                elif not slots:
                    info.issues[lid] = "Нет окон, совместимых с часами, доступностью и типом недели"
                subgroup = re.search(r"\s([1-9]\d*)\s+под\.?$", kind, re.IGNORECASE)
                lessons[lid] = Lesson(lid, subject, teacher, tuple(f"{dept} / {g}" for g in targets),
                                      tuple(room_ids), week_ids, 1, grid_id, availability_sets.setdefault(slots, slots),
                                      int(subgroup[1]) if subgroup else None)
                info.kinds[lid] = kind
                info.assumed += hours is None
    return Problem(groups, teachers, rooms, subjects, lessons, 7, max(map(len, bells.values())), 5, bells), info
