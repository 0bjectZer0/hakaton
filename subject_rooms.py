"""Поиск кабинетов по опубликованным занятиям факультета."""
from collections import Counter, defaultdict
import re


def key(text):
    return " ".join(text.casefold().replace("ё", "е").split())


def location(raw):
    if "стадион локомотив" in key(raw).replace("«", "").replace("»", ""):
        return "Стадион «Локомотив»"
    if raw.startswith("Дистанционно"):
        return "Дистанционно"
    building, sep, place = raw.partition(", ")
    if not sep or "корпус" not in building.lower() or raw.startswith("Место"):
        return None
    number = re.match(r"([\w()./-]+) комната", place)
    return building + ", " + (number[1].lower() if number else place.split(" (")[0].strip())


class SubjectRooms:
    def __init__(self, data):
        self.entries = defaultdict(list)
        self.weeks = defaultdict(set)
        for group, info in data["groups"].items():
            for row in info["weekly"]:
                identity = (group, row["teacher"], key(row["subject"]), key(row["kind"]), key(row["note"]))
                week = row["week"]
                self.weeks[identity].update((week,) if week in ("Ч", "З") else ("Ч", "З"))
            for row in info["weekly"] + info["dated"]:
                self.entries[key(row["subject"]), key(row["kind"])].append(
                    (group, row["teacher"], location(row["room"]), row["room"]))

    def course_weeks(self, row, teacher, groups):
        override = row.get("week")
        if override is not None:
            if override not in ("Ч", "З", "обе"):
                raise ValueError(f"Поле week для {row['subject']} должно быть Ч, З или обе.")
            return frozenset(("Ч", "З") if override == "обе" else (override,))
        available = {"Ч", "З"}
        suffix = (teacher, key(row["subject"]), key(row["kind"]), key(row.get("note", "")))
        for group in groups:
            available.intersection_update(self.weeks.get((group, *suffix), ("Ч", "З")))
        if not available:
            raise ValueError(f"Группам занятия {row['subject']} нужны разные типы недель. Проверьте состав потока.")
        return frozenset(available)

    def candidates(self, subject, kind, teacher, groups):
        entries = self.entries.get((key(subject), key(kind)), ())
        ranks = [Counter() for _ in range(4)]
        for group, name, room, _ in entries:
            if room:
                rank = (0 if name == teacher else 2) + (0 if group in groups else 1)
                ranks[rank][room] += 1
        result = []
        for counts in ranks:
            for room in sorted(counts, key=lambda r: (-counts[r], r)):
                if room not in result:
                    result.append(room)
        # Формат занятия задаётся ближайшими по преподавателю и группе записями.
        first = next((counts for counts in ranks if counts), {})
        if set(first) == {"Дистанционно"}:
            return ("Дистанционно",)
        return tuple(r for r in result if r != "Дистанционно")

    def describe(self, subject):
        for (name, kind), rows in sorted(self.entries.items()):
            if name == key(subject):
                locations = defaultdict(set)
                for group, _, room, raw in rows:
                    locations[room or raw or "Место не назначено"].add(group)
                for room, groups in sorted(locations.items()):
                    yield f"{kind.capitalize()} | {room} | {', '.join(sorted(groups))}"
