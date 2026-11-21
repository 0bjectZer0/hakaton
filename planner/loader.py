"""Чтение пяти UTF-8 JSON-файлов. Сообщения об ошибках содержат имя файла и путь поля."""
import json
import re
from pathlib import Path

from .models import Group, Lesson, Problem, Room, Subject, Teacher


def read_file(folder, name):
    path = Path(folder) / (name + ".json")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: ошибка чтения JSON ({exc})") from exc


def integer(value, path, low, high=None):
    if type(value) is not int or value < low or high is not None and value > high:
        limit = f"от {low} до {high}" if high is not None else f"не меньше {low}"
        raise ValueError(f"{path}: ожидается целое число {limit}")
    return value


def identifier(value, path):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f"{path}: ожидается непустая строка без краевых пробелов")
    return value


def records(rows, path):
    if not isinstance(rows, list):
        raise ValueError(f"{path}: ожидается список записей")
    seen = set()
    for index, row in enumerate(rows):
        where = f"{path}[{index}]"
        if not isinstance(row, dict):
            raise ValueError(f"{where}: ожидается объект")
        ident = identifier(row.get("id"), where + ".id")
        if ident in seen:
            raise ValueError(f"{where}.id: повторяется {ident}")
        seen.add(ident)
        yield ident, row, where


def identifiers(value, path, allow_empty=True, refs=None):
    if not isinstance(value, list) or not allow_empty and not value:
        raise ValueError(f"{path}: ожидается {'список' if allow_empty else 'непустой список'} идентификаторов")
    ids = tuple(identifier(v, path) for v in value)
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path}: идентификаторы должны быть уникальны")
    if refs is not None:
        unknown = [v for v in ids if v not in refs]
        if unknown:
            raise ValueError(f"{path}: неизвестный идентификатор {unknown[0]}")
    return ids


def clock(value, path):
    if not isinstance(value, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
        raise ValueError(f"{path}: ожидается время в формате ЧЧ:ММ")
    return int(value[:2]) * 60 + int(value[3:])


def read_bells(raw):
    path = "lessons.json.bells"
    if not isinstance(raw, dict) or not raw:
        raise ValueError(f"{path}: требуется хотя бы одна сетка звонков")
    result = {}
    for name, rows in raw.items():
        identifier(name, path)
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"{path}.{name}: ожидается непустой список пар")
        grid = []
        for i, row in enumerate(rows):
            field = f"{path}.{name}[{i}]"
            if not isinstance(row, list) or len(row) != 2:
                raise ValueError(f"{field}: укажите начало и конец пары")
            start, end = (clock(value, field) for value in row)
            if start >= end or grid and start < grid[-1][1]:
                raise ValueError(f"{field}: занятия пересекаются или идут в неверном порядке")
            grid.append((start, end))
        result[name] = tuple(grid)
    return result


def availability(value, path, days, periods):
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError(f"{path}: требуется список троек [неделя, день, пара]")
    slots = set()
    for i, row in enumerate(value):
        where = f"{path}[{i}]"
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"{where}: ожидается [неделя, день, пара], индексы с нуля")
        slot = tuple(integer(v, where, 0, high) for v, high in zip(row, (1, days - 1, periods - 1)))
        if slot in slots:
            raise ValueError(f"{where}: повтор окна доступности {slot}")
        slots.add(slot)
    return frozenset(slots)


def load_problem(folder):
    config = read_file(folder, "lessons")
    if not isinstance(config, dict):
        raise ValueError("lessons.json: ожидается объект с сетками звонков и занятиями")
    bells = read_bells(config.get("bells"))
    days = integer(config.get("days"), "lessons.json.days", 1, 7)
    periods = max(map(len, bells.values()))
    limit = integer(config.get("daily_limit", 5), "lessons.json.daily_limit", 1)
    groups = {}
    for k, row, path in records(read_file(folder, "groups"), "groups.json"):
        course = row.get("course")
        groups[k] = Group(k, integer(row.get("size"), path + ".size", 1),
                          integer(course, path + ".course", 1) if course is not None else None)
    subjects = {}
    for k, row, path in records(read_file(folder, "subjects"), "subjects.json"):
        subjects[k] = Subject(k, frozenset(identifiers(row.get("features", []), path + ".features")))
    teachers = {}
    for k, row, path in records(read_file(folder, "teachers"), "teachers.json"):
        teachers[k] = Teacher(k, availability(row.get("available"), path + ".available", days, periods))
    rooms = {}
    for k, row, path in records(read_file(folder, "rooms"), "rooms.json"):
        keys = identifiers(row.get("keys", []), path + ".keys")
        features = frozenset(identifiers(row.get("features", []), path + ".features"))
        virtual = row.get("virtual", False)
        if type(virtual) is not bool:
            raise ValueError(f"{path}.virtual: ожидается true или false")
        capacity = row.get("capacity")
        if capacity is not None:
            capacity = integer(capacity, path + ".capacity", 1)
        windows = availability(row.get("available"), path + ".available", days, periods)
        rooms[k] = Room(k, capacity, features, keys, windows, virtual)
    lessons = {}
    for k, row, path in records(config.get("lessons"), "lessons.json.lessons"):
        teacher = identifier(row.get("teacher"), path + ".teacher")
        subject = identifier(row.get("subject"), path + ".subject")
        bell = identifier(row.get("bell", "main"), path + ".bell")
        for field, value, known in (("teacher", teacher, teachers), ("subject", subject, subjects), ("bell", bell, bells)):
            if value not in known:
                raise ValueError(f"{path}.{field}: неизвестный идентификатор {value}")
        gs = identifiers(row.get("groups"), path + ".groups", allow_empty=False, refs=groups)
        allowed = identifiers(row.get("rooms"), path + ".rooms", refs=rooms)
        weeks = row.get("weeks", [0, 1])
        if not isinstance(weeks, list) or not weeks:
            raise ValueError(f"{path}.weeks: ожидается непустой список недель 0 (Ч) и/или 1 (З)")
        weeks = tuple(integer(w, path + ".weeks", 0, 1) for w in weeks)
        if len(weeks) != len(set(weeks)):
            raise ValueError(f"{path}.weeks: повтор типа недели")
        duration = integer(row.get("duration", 1), path + ".duration", 1, len(bells[bell]))
        windows = availability(row.get("available"), path + ".available", days, len(bells[bell]))
        lessons[k] = Lesson(k, subject, teacher, gs, allowed, weeks, duration, bell, windows)
    return Problem(groups, teachers, rooms, subjects, lessons, days, periods, limit, bells)
