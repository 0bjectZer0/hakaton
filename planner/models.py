"""Один повторяющийся двухнедельный цикл. Индексы недель, дней и пар начинаются с нуля."""
from dataclasses import dataclass


Availability = frozenset[tuple[int, int, int]]


@dataclass(frozen=True)
class Group:
    id: str
    size: int | None
    course: int | None = None


@dataclass(frozen=True)
class Teacher:
    id: str
    available: Availability | None = None


@dataclass(frozen=True)
class Room:
    id: str
    capacity: int | None = None
    features: frozenset[str] = frozenset()
    keys: tuple[str, ...] = ()
    available: Availability | None = None
    virtual: bool = False

    @property
    def physical_keys(self):
        if self.virtual:
            return ()
        return self.keys or (self.id,)


@dataclass(frozen=True)
class Subject:
    id: str
    features: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Lesson:
    id: str
    subject: str
    teacher: str
    groups: tuple[str, ...]
    rooms: tuple[str, ...]
    weeks: tuple[int, ...] = (0, 1)
    duration: int = 1
    bell: str = "main"
    available: Availability | None = None
    subgroup: int | None = None


@dataclass(frozen=True)
class Placement:
    day: int
    period: int
    room: str


@dataclass(frozen=True)
class Problem:
    groups: dict[str, Group]
    teachers: dict[str, Teacher]
    rooms: dict[str, Room]
    subjects: dict[str, Subject]
    lessons: dict[str, Lesson]
    days: int
    periods: int
    daily_limit: int
    bells: dict[str, tuple[tuple[int, int], ...]]
