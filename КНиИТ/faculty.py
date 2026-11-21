"""Каталог КНиИТ, подготовка нагрузки и расчёт новых занятий."""
import argparse
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from rooms import ROOMS, REMOTE, RoomAllocator, booking_session, minutes, save_bookings, week_type
from room_choices import LOCAL_ROOMS
from subject_rooms import SubjectRooms
from raspisanie import Course, Teacher, Slot, schedule

DATA = Path(__file__).with_name("kniit.json")
START = date(2026, 9, 1)
END = date(2027, 1, 3)
TIMES = "08:20 10:00 12:05 13:50 15:35 17:20 18:45 20:10".split()
ENDS = "09:50 11:35 13:40 15:25 17:10 18:40 20:05 21:30".split()
MONTHS = "января февраля марта апреля мая июня июля августа сентября октября ноября декабря".split()
DAYS = "Пн Вт Ср Чт Пт Сб Вс".split()
PROGRAMS = {
    "Бакалавриат": {
        "02.03.02": "Фундаментальная информатика и информационные технологии",
        "02.03.03": "Математическое обеспечение и администрирование информационных систем",
        "09.03.01": "Информатика и вычислительная техника",
        "09.03.04": "Программная инженерия",
        "27.03.03": "Системный анализ и управление"},
    "Специалитет": {"10.05.01": "Компьютерная безопасность"},
    "Магистратура": {
        "02.04.03": "Математическое обеспечение и администрирование информационных систем",
        "09.04.01": "Информатика и вычислительная техника"},
    "Аспирантура": {
        "1.2.2": "Математическое моделирование, численные методы и комплексы программ",
        "1.2.3": "Теоретическая информатика, кибернетика",
        "1.1.5": "Математическая логика, алгебра, теория чисел и дискретная математика",
        "2.3.1": "Системный анализ, управление и обработка информации, статистика"},
}


def dated_time(text):
    day, month, year, _, time = text.split()
    return date(int(year), MONTHS.index(month) + 1, int(day)), time


def current_weekly(group):
    stamp = group["updated"]
    if stamp == "Не":
        return False
    d, m, y = map(int, stamp.split("."))
    return START <= date(y, m, d) <= END


def template(data):
    # Совпадающие потоковые лекции объединяем по времени, преподавателю и аудитории.
    streams = defaultdict(set)
    courses = defaultdict(set)
    for gid, group in data["groups"].items():
        for row in group["weekly"] if current_weekly(group) else []:
            name, kind, subject, note = (row[k] for k in ("teacher", "kind", "subject", "note"))
            if "*" in name or subject.lower().startswith("самостоятельная работа"):
                continue
            if kind == "ЛЕКЦИЯ" and not note and row["room"] and name in data["teachers"]:
                key = name, subject, row["day"], row["time"], row["week"], row["room"]
                streams[key].add(gid)
            else:
                courses[name].add((subject, kind, (gid,), note))
        for row in group["dated"]:
            day, _ = dated_time(row["date"])
            if START <= day <= END and row["kind"].lower() in {"лекция", "практика", "лабораторная"}:
                courses[row["teacher"]].add((row["subject"], row["kind"].upper(), (gid,), ""))
    for (name, subject, *_), gids in streams.items():
        courses[name].add((subject, "ЛЕКЦИЯ", tuple(sorted(gids)), ""))
    # Рабочее соответствие по серии номера очной группы. Его можно исправить в плане.
    series = {"1": "02.03.02", "2": "09.03.01", "3": "10.05.01",
              "4": "02.03.03", "5": "09.03.04", "8": "27.03.03"}
    mapping = {gid: series.get(gid.split("/")[1][1]) for gid in data["groups"]}
    return {"start": "2027-02-01", "end": "2027-05-31",
            "group_programs": mapping, "teachers": [
        {"name": name, "available": [], "courses": [
            dict(subject=s, kind=k, groups=list(gs), note=n, hours=None)
            for s, k, gs, n in sorted(rows)]}
        for name, rows in sorted(courses.items())]}


def published_busy(data, slots):
    group_busy, teacher_busy = defaultdict(set), defaultdict(set)
    positions = defaultdict(set)
    by_date = defaultdict(set)
    for slot in slots:
        by_date[slot.day].add(slot)
        if START <= slot.day <= END:
            parity = week_type(slot.day)
            for week in ("обе", parity):
                positions[slot.day.isoweekday(), TIMES[slot.period - 1], week].add(slot)
    for name, teacher in data["teachers"].items():
        for day, time, week in teacher["occupied"]:
            teacher_busy[name].update(positions[day, time, week])
    for gid, group in data["groups"].items():
        for row in group["weekly"] if current_weekly(group) else []:
            busy = positions[row["day"], row["time"], row["week"]]
            group_busy[gid].update(busy)
            teacher_busy[row["teacher"]].update(busy)
        for row in group["dated"]:
            day, time = dated_time(row["date"])
            # Нестандартное начало: резервируем пары, пересекающие 95 минут занятия.
            h, m = map(int, time.split(":"))
            end_minutes = h * 60 + m + 95
            for slot in by_date[day]:
                sh, sm = map(int, TIMES[slot.period - 1].split(":"))
                if sh * 60 + sm < end_minutes and ENDS[slot.period - 1] > time:
                    group_busy[gid].add(slot)
                    teacher_busy[row["teacher"]].add(slot)
    return group_busy, teacher_busy


def calculate(data, plan, calendar=None, teacher_bookings=None):
    start, end = map(date.fromisoformat, (plan["start"], plan["end"]))
    if end < start:
        raise ValueError("Проверьте границы семестра.")
    catalog = SubjectRooms(data)
    teachers = []
    for person in plan["teachers"]:
        if "available" in person:
            slots = {Slot(date.fromisoformat(d), p) for d, p in person["available"]}
        else:
            slots = set()
            for offset in range((end-start).days + 1):
                day = start + timedelta(days=offset)
                periods = person.get("date_overrides", {}).get(
                    day.isoformat(), person["weekly_available"].get(DAYS[day.weekday()], []))
                slots.update(Slot(day, p) for p in periods)
        if any(not start <= s.day <= end or not 1 <= s.period <= len(TIMES) for s in slots):
            raise ValueError(f"Проверьте дату и номер пары: {person['name']}")
        if teacher_bookings:
            slots = {slot for slot in slots
                     if not any(start < minutes(ENDS[slot.period-1]) and minutes(TIMES[slot.period-1]) < end
                                for start, end in teacher_bookings.get((person["name"], slot.day), ()))}
        courses = []
        for row in person["courses"]:
            if row["hours"] is None:
                raise ValueError(f"Укажите часы: {person['name']}, {row['subject']}")
            kind = " ".join(filter(None, (row["kind"], row.get("note"))))
            targets = tuple(row.get("groups", ()))
            if "program" in row:
                if targets:
                    raise ValueError("Укажите либо группы, либо направление с курсом и формой.")
                targets = tuple(gid for gid, group in data["groups"].items()
                                if plan["group_programs"].get(gid) == row["program"]
                                and group["course"] == row["year"]
                                and gid.split("/")[0] == row["form"])
            allowed = row.get("rooms")
            if allowed is None:
                allowed = catalog.candidates(row["subject"], row["kind"], person["name"], targets)
            if not isinstance(allowed, (list, tuple)) or any(r not in ROOMS and r != REMOTE for r in allowed):
                raise ValueError(f"Проверьте список аудиторий для {row['subject']}")
            if not allowed and row["hours"]:
                raise ValueError(f"Укажите rooms для {row['subject']} ({kind}, {person['name']}): в расписании нет подходящего кабинета.")
            weeks = catalog.course_weeks(row, person["name"], targets) if row["hours"] else frozenset()
            courses.append(Course(row["subject"], kind, targets, row["hours"], tuple(allowed), weeks))
        teachers.append(Teacher(person["name"], slots, courses))
    slots = {slot for teacher in teachers for slot in teacher.available}
    group_busy, teacher_busy = published_busy(data, slots)
    for teacher in teachers:
        teacher.available.difference_update(teacher_busy[teacher.name])
    if calendar is None:
        with booking_session() as (snapshot, _):
            allocator = RoomAllocator(snapshot, TIMES, ENDS)
    else:
        allocator = RoomAllocator(calendar, TIMES, ENDS)
    return schedule(teachers, data["groups"], group_busy=group_busy, allocator=allocator,
                    teacher_bookings=teacher_bookings)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--programs", action="store_true", help="Справочник направлений и специальностей")
    actions.add_argument("--group", help="Например, do/321 или zo/151")
    actions.add_argument("--template", metavar="JSON", help="Создать заготовку нагрузки")
    actions.add_argument("--plan", metavar="JSON", help="Распределить введённые часы по окнам")
    actions.add_argument("--demo", action="store_true", help="Рассчитать пример для факультета")
    actions.add_argument("--rooms", nargs=2, metavar=("ДАТА", "ПАРА"), help="Занятость аудиторий подразделения")
    actions.add_argument("--subject", help="Кабинеты и группы по названию предмета")
    args = parser.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    groups = data["groups"]
    if args.subject:
        print("\n".join(SubjectRooms(data).describe(args.subject)) or "Предмет отсутствует в расписании подразделения.")
    elif args.rooms:
        try:
            day = date.fromisoformat(args.rooms[0])
            period = int(args.rooms[1])
            if not 1 <= period <= len(TIMES):
                raise ValueError
        except ValueError:
            parser.error("Введите дату ГГГГ-ММ-ДД и номер пары по сетке подразделения.")
        with booking_session() as (calendar, _):
            for name in LOCAL_ROOMS:
                busy = ROOMS[name].is_busy(calendar, day, minutes(TIMES[period-1]), minutes(ENDS[period-1]))
                print(name, "— занята" if busy else "— свободна")
    elif args.programs:
        for level, programs in PROGRAMS.items():
            print(level)
            for code, title in programs.items():
                print(" ", code, title)
    elif args.group:
        if args.group not in groups:
            parser.error("Группа отсутствует в каталоге КНиИТ.")
        g = groups[args.group]
        print(g["url"], "Обновление:", g["updated"] if g["updated"] != "Не" else "не указано")
        for r in g["weekly"]:
            print(DAYS[r["day"]-1], r["time"], r["week"], r["kind"], r["note"], r["subject"], r["teacher"], r["room"])
        for r in g["dated"]:
            print(r["date"], r["kind"], r["subject"], r["teacher"], r["room"])
        if not g["weekly"] and not g["dated"]:
            print("Расписание занятий не заполнено.")
    elif args.template:
        plan = json.loads(DATA.with_name("semester.json").read_text(encoding="utf-8"))
        with open(args.template, "x", encoding="utf-8") as file:
            json.dump(plan, file, ensure_ascii=False, indent=2)
    elif args.plan or args.demo:
        path = DATA.with_name("semester.json") if args.demo else Path(args.plan)
        plan = json.loads(path.read_text(encoding="utf-8-sig"))
        if "teachers" not in plan:
            from teachers import teacher_data
            plan["teachers"] = teacher_data()
        if args.demo:
            print("Модель: для незаполненной нагрузки принято 2 академических часа.")
            catalog = SubjectRooms(data)
            for person in plan["teachers"]:
                for row in person["courses"]:
                    if "rooms" not in row and not catalog.candidates(row["subject"], row["kind"], person["name"], row.get("groups", ())):
                        print("Требуется кабинет:", person["name"], row["subject"], row["kind"], ", ".join(row.get("groups", ())))
                        row["hours"] = 0
                    if row["hours"] is None:
                        row["hours"] = 2
        try:
            owner = data["source"] if args.plan else None
            with booking_session(owner, plan["start"], plan["end"]) as (calendar, db):
                lessons, free = calculate(data, plan, calendar)
                if owner:
                    save_bookings(db, owner, lessons, TIMES, ENDS)
        except ValueError as exc:
            parser.exit(1, str(exc) + "\n")
        for lesson in lessons:
            print(lesson.slot.day, TIMES[lesson.slot.period-1], lesson.teacher, lesson.course.kind,
                  lesson.course.subject, ", ".join(lesson.course.tracks), lesson.room, sep=" | ")
        print("Назначено пар:", len(lessons))
        if args.plan:
            for name, slots in free.items():
                print(name, "— свободно:", ", ".join(f"{s.day} {TIMES[s.period-1]}" for s in sorted(slots)))
    else:
        for gid, group in groups.items():
            print(gid, group["level"], f'{group["course"]} курс',
                  f'записей в сетке: {len(group["weekly"])}, по датам: {len(group["dated"])}')
        print("Подробнее: --group do/321 | --demo | --template plan.json | --plan plan.json")
