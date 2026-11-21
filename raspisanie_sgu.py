"""Общий расчёт для подразделений СГУ с выводом в терминал."""
import importlib
import json
import sys
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path

from planner import console
from rooms import REMOTE, ROOMS, week_type

ROOT = Path(__file__).resolve().parent
WEEKDAYS = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")


@contextmanager
def faculty_modules(folder):
    names = ("faculty", "teachers", "raspisanie", "room_choices")
    original_path = sys.path[:]
    sys.path.insert(0, str(folder))
    try:
        yield importlib.import_module("faculty"), importlib.import_module("teachers")
    finally:
        for name in names:
            sys.modules.pop(name, None)
        sys.path[:] = original_path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def published_fortnight(departments):
    rows, groups = [], {}
    monday = None
    for department in departments:
        folder = ROOT / department
        with faculty_modules(folder) as (faculty, _):
            data = read_json(faculty.DATA)
            start = date.fromisoformat(read_json(folder / "semester.json")["start"])
            start -= timedelta(days=start.weekday())
            if monday is not None and monday != start:
                raise ValueError("Для общего вывода настройте одну начальную неделю семестра.")
            monday = start
            ends = dict(zip(faculty.TIMES, faculty.ENDS))
        groups[department] = set(data["groups"])
        for group, info in data["groups"].items():
            for lesson in info["weekly"]:
                day = monday + timedelta(days=lesson["day"] - 1)
                kind = " ".join(filter(None, (lesson["kind"], lesson["note"])))
                for offset in (0, 7):
                    current = day + timedelta(days=offset)
                    if lesson["week"] in ("обе", week_type(current)):
                        rows.append((current, lesson["time"], ends.get(lesson["time"]), department, (group,),
                                     lesson["teacher"], kind, lesson["subject"], lesson["room"]))
    return monday, sorted(rows), groups


def verify(rows):
    ends = {}
    daily = Counter()
    for day, start, end, dept, groups, teacher, _, _, room in rows:
        resources = [("преподаватель", teacher), *((dept, g) for g in groups)]
        for resource in resources:
            daily[resource, day] += 1
            if daily[resource, day] > 5:
                raise ValueError(f"Больше пяти пар за день: {resource}, {day}")
        if room != REMOTE:
            resources.extend(("аудитория", key) for key in ROOMS[room].keys)
        for resource in resources:
            if ends.get((day, resource), "") > start:
                raise ValueError(f"Пересечение: {day} {start} {resource}")
            ends[day, resource] = end


def choose(prompt, all_label, options):
    print(prompt, file=sys.stderr)
    print(f" 0. {all_label}", file=sys.stderr)
    for number, label in enumerate(options.values(), 1):
        print(f"{number:2}. {label}", file=sys.stderr)
    while True:
        print("Введите номер: ", end="", file=sys.stderr, flush=True)
        try:
            choice = input().strip()
        except EOFError:
            return None  # Запуск без ввода сохраняет прежний полный вывод.
        if choice == "0":
            return None
        for number, (name, label) in enumerate(options.items(), 1):
            if choice == str(number) or choice.casefold() in (name.casefold(), label.casefold()):
                return name
        print(f"Введите 0 или номер от 1 до {len(options)}.", file=sys.stderr)


def choose_groups(department):
    folder = ROOT / department
    with faculty_modules(folder) as (faculty, _):
        groups = json.loads(faculty.DATA.read_text(encoding="utf-8"))["groups"]
        plan = json.loads((folder / "semester.json").read_text(encoding="utf-8-sig"))
        program_titles = {code: title for level in getattr(faculty, "PROGRAMS", {}).values()
                          for code, title in level.items()}
    mapping = plan.get("group_programs", {})
    codes = sorted({mapping[g] for g in groups if mapping.get(g)})
    program = None
    if codes:
        programs = {code: f"{code} — {program_titles[code]}" if code in program_titles else code
                    for code in codes}
        program = choose("Выберите направление", "Все направления и группы", programs)
    else:
        print("Для этого факультета доступны группы по номерам. Коды направлений задаются в semester.json.",
              file=sys.stderr)
    eligible = {g: g for g in sorted(groups) if program is None or mapping.get(g) == program}
    group = choose("Выберите группу", "Все группы", eligible) if eligible else None
    label = department
    if program:
        label += f" · {programs[program]}"
    if group:
        label += f" · {group}"
    return label, {group} if group else set(eligible)


def main():
    parser, args = console.arguments()
    if args.published and (args.data or args.config or args.view != "group" or args.resource
                           or args.week != "обе" or args.variant or args.summary_only
                           or any(getattr(args, key) is not None for key in
                                  ("adaptive", "variants", "attempts", "seed", "time_limit", "randomness", "max_iterations"))):
        parser.error("--published показывает сетку СГУ. Параметры генератора и его отчётов применяются при расчёте.")
    departments = ["КНиИТ"]
    selected, selected_groups = None, None
    if not (args.no_menu or args.data or args.summary_only or args.resource):
        selected = departments[0]
    label = "КНиИТ"
    if selected:
        label, selected_groups = choose_groups(selected)
    if not args.published:
        try:
            console.run(args, ROOT, faculty_modules, read_json, selected, selected_groups)
        except (OSError, ValueError, TypeError) as exc:
            parser.exit(2, f"Ошибка расчёта: {exc}\n")
        return
    monday, rows, groups = published_fortnight([selected] if selected else departments)
    if selected:
        groups = {selected: selected_groups}
    rows = [row for row in rows if groups.get(row[3], set()).intersection(row[4])]
    print(f"Двухнедельный шаблон из сохранённого расписания СГУ: {label}.")
    print("Даты взяты из настроек семестра, время и состав пар — из недельной сетки СГУ.")
    covered = defaultdict(set)
    by_day = defaultdict(list)
    for row in rows:
        by_day[row[0]].append(row[1:])
    for offset in (0, 7):
        week_start = monday + timedelta(days=offset)
        week_end = week_start + timedelta(days=6)
        parity = "числитель" if week_type(week_start) == "Ч" else "знаменатель"
        print(f"\nНеделя {week_start:%d.%m.%Y} — {week_end:%d.%m.%Y} · {parity}")
        if not any(by_day.get(week_start + timedelta(days=n)) for n in range(7)):
            print("На эту неделю в выбранных данных нет пар недельной сетки.")
        for weekday, name in enumerate(WEEKDAYS):
            day = week_start + timedelta(days=weekday)
            print(f"\n{name}  {day:%d.%m.%Y}")
            if not by_day.get(day):
                print("В этот день пар нету")
                continue
            print("Время | Подразделение | Группы | Преподаватель | Вид | Предмет | Место")
            for start, end, dept, targets, teacher, kind, subject, room in by_day[day]:
                time = f"{start}–{end}" if end else start
                print(time, dept, ", ".join(targets), teacher, kind, subject, room, sep=" | ")
                covered[dept].update(groups[dept].intersection(targets))
    print("\nИтоги по подразделениям")
    counts = Counter(r[3] for r in rows)
    for dept in groups:
        print(f"{dept}: {counts[dept]} пар, групп {len(covered[dept])} из {len(groups[dept])}")
    print(f"Подразделений: {len(groups)}. Записей о парах за две недели: {len(rows)}.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        from calendar_kniit import main as calendar_main
        calendar_main()
    else:
        main()
