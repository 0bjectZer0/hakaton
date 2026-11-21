"""Раскладка двух повторяющихся недель по общей сетке ресурсов СГУ."""
from collections import Counter, defaultdict
from datetime import date, timedelta
from functools import lru_cache

from rooms import REMOTE, ROOMS, booking_session, minutes, week_type
from subject_rooms import SubjectRooms, location


def semester(folder, load_modules, read_json):
    with load_modules(folder) as (faculty, profiles):
        plan = read_json(folder / "semester.json")
        data = read_json(faculty.DATA)
        people = plan["teachers"] if "teachers" in plan else profiles.teacher_data()
        bell = tuple(zip(faculty.TIMES, faculty.ENDS))
        first, last = map(date.fromisoformat, (plan["start"], plan["end"]))
        days = recurring_dates(first, last)
        slots = {faculty.Slot(day, period) for dates in days.values() for day in dates
                 for period in range(1, len(bell) + 1)}
        group_busy, teacher_busy = faculty.published_busy(data, slots)
        return plan, data, people, bell, days, group_busy, teacher_busy


def recurring_dates(first, last):
    days = defaultdict(list)
    for offset in range((last - first).days + 1):
        day = first + timedelta(days=offset)
        days[day.weekday(), week_type(day)].append(day)
    return days


def shared_classes(data):
    meetings = defaultdict(set)
    for group, info in data["groups"].items():
        for row in info["weekly"]:
            kind = " ".join(filter(None, (row["kind"], row["note"])))
            key = group, row["teacher"], kind, row["subject"]
            meetings[key].add((row["day"], row["time"], row["week"], row["room"]))
    return meetings


def available_slots(person, days, bell):
    exact = {(date.fromisoformat(d), p) for d, p in person.get("available", ())}
    options = []
    for weekday, name in enumerate(("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")):
        for period, (start, end) in enumerate(bell, 1):
            weeks = set()
            for parity in ("Ч", "З"):
                dates = days[weekday, parity]
                if not dates:
                    continue
                if "available" in person:
                    valid = all((d, period) in exact for d in dates)
                else:
                    weekly = person["weekly_available"].get(name, ())
                    overrides = person.get("date_overrides", {})
                    valid = all(period in overrides.get(d.isoformat(), weekly) for d in dates)
                if valid:
                    weeks.add(parity)
            if weeks:
                options.append((weekday, start, end, weeks))
    return options


def prepare(root, load_modules, read_json):
    groups, dates_by_department = {}, {}
    requests, bells = [], {}
    bounds = set()
    for path in sorted(root.glob("*/faculty.py")):
        department = path.parent.name
        plan, data, people, bell, days, group_busy, teacher_busy = semester(path.parent, load_modules, read_json)
        bells[department] = bell
        first, last = map(date.fromisoformat, (plan["start"], plan["end"]))
        if last - first < timedelta(days=13):
            raise ValueError(f"Для двухнедельной сетки нужен период от 14 дней: {department}")
        bounds.add((first, last))
        dates_by_department[department] = days
        groups[department] = {gid: group.get("course") for gid, group in data["groups"].items()}
        catalog = SubjectRooms(data)
        meetings = shared_classes(data)
        shared = {}
        periods = {start: p for p, (start, _) in enumerate(bell, 1)}
        unavailable = {
            resource: {(s.day.weekday(), week_type(s.day), s.period) for s in slots}
            for resource, slots in (*group_busy.items(), *teacher_busy.items())
        }
        for person in people:
            name = person["name"]
            slots = available_slots(person, days, bell) if person["courses"] else []
            for course in person["courses"]:
                hours = course["hours"]
                if hours == 0:
                    continue
                targets = tuple(course.get("groups", ()))
                if "program" in course:
                    targets = tuple(gid for gid, group in data["groups"].items()
                                    if plan["group_programs"].get(gid) == course["program"]
                                    and group["course"] == course["year"] and gid.split("/")[0] == course["form"])
                if not targets or not set(targets) <= groups[department].keys():
                    raise ValueError(f"Проверьте группы для {course['subject']} ({department}).")
                kind = " ".join(filter(None, (course["kind"], course.get("note"))))
                row = (department, targets, name, kind, course["subject"])
                rooms = course.get("rooms")
                if rooms is None:
                    rooms = catalog.candidates(course["subject"], course["kind"], name, targets)
                if not isinstance(rooms, (list, tuple)) or any(room != REMOTE and room not in ROOMS for room in rooms):
                    raise ValueError(f"Проверьте список аудиторий для {course['subject']}.")
                if hours is not None and (type(hours) is not int or hours < 0 or hours % 2):
                    raise ValueError(f"Укажите чётное число академических часов для {course['subject']}.")
                weeks = catalog.course_weeks(course, name, targets)
                options = [(weekday, start, end,
                            sum(len(days[weekday, week]) for week in weeks))
                           for weekday, start, end, available in slots if weeks <= available
                           and not any((weekday, week, periods[start]) in unavailable.get(resource, ())
                                       for resource in (name, *targets) for week in weeks)]
                # Одна пара преподавателя в одной аудитории может быть опубликована
                # в нескольких группах. Резервируем её один раз для всего потока.
                signatures = {frozenset(meetings[g, name, kind, course["subject"]]) for g in targets}
                signature = next(iter(signatures)) if len(signatures) == 1 else ()
                if any(location(place) not in ROOMS for _, _, _, place in signature):
                    signature = ()
                joint = (name, kind, course["subject"], weeks, hours, tuple(rooms), signature)
                if signature and joint in shared:
                    i = shared[joint]
                    old, _, _, old_options, _ = requests[i]
                    row = (department, tuple(sorted(set(old[1]) | set(targets))), name, kind, course["subject"])
                    options = sorted(set(old_options).intersection(options))
                    requests[i] = (row, weeks, rooms, options, hours)
                else:
                    if signature:
                        shared[joint] = len(requests)
                    requests.append((row, weeks, rooms, options, hours))

    if len(bounds) != 1:
        raise ValueError("Для общей двухнедельной сетки даты семестра должны совпадать у всех подразделений.")
    first, _ = bounds.pop()
    monday = first - timedelta(days=first.weekday())
    return monday, requests, groups, dates_by_department, bells


def generate(root, load_modules, read_json):
    monday, requests, groups, dates_by_department, _ = prepare(root, load_modules, read_json)
    missing, assumed = [], Counter()
    total_by_teacher = Counter(row[2] for row, *_ in requests)
    requests.sort(key=lambda r: (-len(r[1]), len(r[3]), len(r[2]), -len(r[0][1]), -total_by_teacher[r[0][2]]))
    occupancy = defaultdict(list)
    daily_load = Counter()
    placed = []

    @lru_cache(maxsize=16384)
    def day_cost(intervals):
        # Целевая нагрузка — 2–3 пары. Окна от часа учитываются отдельно от обычных перемен.
        load_cost = (0, 8, 1, 2, 6, 15)[len(intervals)]
        return load_cost + sum(4 + (b[0] - a[1]) // 60 for a, b in zip(intervals, intervals[1:])
                               if b[0] - a[1] >= 60)

    with booking_session() as (calendar, _):
        @lru_cache(maxsize=None)
        def room_available(room, department, weekday, week, start, end):
            return not any(ROOMS[room].is_busy(calendar, day, start, end)
                           for day in dates_by_department[department][weekday, week])

        def free(resources, weekday, weeks, start, end):
            return all(not any(a < end and start < b for a, b in occupancy[resource, weekday, week])
                       for resource in resources for week in weeks)

        def reserve(resources, weeks, day, start, end, add):
            for resource in resources:
                for week in weeks:
                    intervals = occupancy[resource, day, week]
                    if add:
                        intervals.append((start, end))
                    else:
                        intervals.remove((start, end))

        def added_cost(resources, weeks, day, interval):
            total = 0
            for resource in resources:
                for week in weeks:
                    current = tuple(sorted(occupancy[resource, day, week]))
                    total += day_cost(tuple(sorted((*current, interval)))) - day_cost(current)
            return total

        for row, weeks, rooms, options, hours in requests:
            if not rooms:
                missing.append((*row, "Требуется аудитория"))
                continue
            department, targets, name, _, _ = row
            teacher = ("teacher", name)
            resources = (teacher, *((department, group) for group in targets))
            remaining = hours // 2 if hours is not None else 1
            # Одна ячейка шаблона даёт столько пар, сколько раз этот день встречается в семестре.
            while remaining:
                def day_priority(day):
                    loads = [daily_load[resource, day, week] for resource in resources for week in weeks]
                    return (max(loads) >= 5, -loads.count(1), loads.count(0), max(loads))

                priorities = {day: day_priority(day) for day in {item[0] for item in options}}
                options = sorted(options, key=lambda item: (priorities[item[0]], item[1], item[0]))
                match = None
                for weekday, start, end, repeats in options:
                    if hours is not None and repeats > remaining:
                        continue
                    begin, finish = minutes(start), minutes(end)
                    if priorities[weekday][0]:
                        continue
                    if not free(resources, weekday, weeks, begin, finish):
                        continue
                    for room in rooms:
                        keys = tuple(("room", key) for key in ROOMS[room].keys) if room != REMOTE else ()
                        if keys and (not free(keys, weekday, weeks, begin, finish) or not all(
                                room_available(room, department, weekday, week, begin, finish) for week in weeks)):
                            continue
                        match = weekday, start, end, repeats, room, keys
                        break
                    if match:
                        break
                if not match:
                    reason = "Нет общего свободного окна для повторения"
                    if hours is not None:
                        reason += f" · осталось {remaining * 2} акад. ч."
                    missing.append((*row, reason))
                    break
                weekday, start, end, repeats, room, keys = match
                reserve(resources + keys, weeks, weekday, minutes(start), minutes(end), True)
                for week in weeks:
                    for resource in resources:
                        daily_load[resource, weekday, week] += 1
                placed.append((row, weeks, rooms, options, resources, hours, match))
                if hours is None:
                    assumed[department, targets] += 1
                remaining -= repeats if hours is not None else 1
        # Переносим целиком повторяющееся занятие и сохраняем число назначенных часов.
        for _ in range(2):
            for i, (row, weeks, rooms, options, resources, hours, original) in enumerate(placed):
                department = row[0]
                day, start, end, repeats, room, keys = original
                reserve(resources + keys, weeks, day, minutes(start), minutes(end), False)
                best = original
                score = added_cost(resources, weeks, day, (minutes(start), minutes(end)))
                for weekday, start, end, count in options:
                    if hours is not None and count != repeats:
                        continue
                    begin, finish = minutes(start), minutes(end)
                    if any(len(occupancy[r, weekday, w]) >= 5 for r in resources for w in weeks):
                        continue
                    if not free(resources, weekday, weeks, begin, finish):
                        continue
                    cost = added_cost(resources, weeks, weekday, (begin, finish))
                    if cost >= score:
                        continue
                    for candidate in rooms:
                        keys = tuple(("room", k) for k in ROOMS[candidate].keys) if candidate != REMOTE else ()
                        if keys and (not free(keys, weekday, weeks, begin, finish) or not all(
                                room_available(candidate, department, weekday, w, begin, finish) for w in weeks)):
                            continue
                        best = weekday, start, end, count, candidate, keys
                        score = cost
                        break
                day, start, end, _, _, keys = best
                reserve(resources + keys, weeks, day, minutes(start), minutes(end), True)
                placed[i] = row, weeks, rooms, options, resources, hours, best

    output = []
    for row, weeks, _, _, _, _, (weekday, start, end, _, room, _) in placed:
        for offset in (0, 7):
            day = monday + timedelta(days=offset + weekday)
            if week_type(day) in weeks:
                output.append((day, start, end, *row, room))
    return monday, sorted(output), missing, assumed, {dept: set(gs) for dept, gs in groups.items()}
