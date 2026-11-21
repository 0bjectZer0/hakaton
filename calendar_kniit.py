"""Календарь КНиИТ. Каждая альтернатива рассчитывается для всего факультета."""
import argparse
from collections import defaultdict
from html import escape
import json
import re
import webbrowser

from planner.optimization import Config, generate_variants
from planner.sgu import load_sgu
from raspisanie_sgu import ROOT, faculty_modules, read_json


def calendar_data():
    problem, info = load_sgu(ROOT, faculty_modules, read_json)
    plan = read_json(ROOT / "КНиИТ" / "semester.json")
    groups = sorted(problem.groups)
    indices = {name: i for i, name in enumerate(groups)}
    lessons = {lid: dict(subject=l.subject, teacher=l.teacher, kind=info.kinds[lid],
                         groups=[indices[g] for g in l.groups], weeks=l.weeks)
               for lid, l in problem.lessons.items()}
    variants = []
    for result in generate_variants(problem, Config(**read_json(ROOT / "search_config.json"))):
        events = []
        for lid, p in result.placements.items():
            lesson = problem.lessons[lid]
            bells = problem.bells[lesson.bell]
            events.append(dict(id=lid, day=p.day, slot=p.period, start=bells[p.period][0],
                               end=bells[p.period + lesson.duration - 1][1], room=info.room_names[p.room]))
        variants.append(dict(profile=result.profile, events=events, missing=result.missing))
    if not variants:
        raise ValueError("В отведённое время не удалось получить вариант расписания.")
    names = [g.split(" / ", 1)[1] for g in groups]
    return dict(groups=names, programs=[plan["group_programs"].get(g) or "Направление не указано" for g in names],
                lessons=lessons, variants=variants)


def group_label(group):
    form, _, number = group.partition("/")
    forms = {"do": "дневная", "zo": "заочная"}
    return f"{number} · {forms[form]}" if number and form in forms else group


def lesson_fields(kind):
    name, _, note = kind.strip().partition(" ")
    if name.lower() not in ("лекция", "практика", "лабораторная"):
        return {"type": kind or "Занятие", "note": "", "subgroup": ""}
    note = note.strip()
    subgroup = ""
    match = re.search(r"(?<!\w)(\d+(?:\s*(?:и|,)\s*\d+)*)\s*под(?:гр(?:упп[аы]?)?)?\.?$", note, re.I)
    if match:
        numbers = match[1]
        label = "Подгруппа" if numbers.isdigit() else "Подгруппы"
        subgroup = f"{label} {numbers}"
        note = note[:match.start()].rstrip()
    return {"type": name.capitalize(), "note": note, "subgroup": subgroup}


def static_view(data):
    profiles = {"comfort": "Комфорт студентов", "compact": "Компактность",
                "balance": "Баланс", "compromise": "Компромисс"}
    days = "Понедельник Вторник Среда Четверг Пятница Суббота Воскресенье".split()

    def clock(minutes):
        return f"{minutes // 60:02}:{minutes % 60:02}"

    parts = []
    for number, variant in enumerate(data["variants"], 1):
        rows, missing = defaultdict(list), defaultdict(list)
        for event in sorted(variant["events"], key=lambda e: e["start"]):
            lesson = data["lessons"][event["id"]]
            kind = escape(lesson["type"])
            note = f'<small>{escape(lesson["note"])}</small>' if lesson["note"] else ""
            subgroup = f'<small class="subgroup">{escape(lesson["subgroup"])}</small>' if lesson["subgroup"] else ""
            line = (f'<article class="card" data-kind="{kind}"><div class="card-head">'
                    f'<strong>{clock(event["start"])}–{clock(event["end"])}</strong><span>{kind}</span></div>'
                    f'<b class="subject">{escape(lesson["subject"])}</b>{subgroup}{note}<small>{escape(lesson["teacher"])}</small>'
                    f'<small class="room">{escape(event["room"])}</small></article>')
            for group in lesson["groups"]:
                for parity in lesson["weeks"]:
                    rows[group, parity, event["day"]].append(line)
        for lid in variant["missing"]:
            lesson = data["lessons"][lid]
            fields = [escape(lesson["subject"]), escape(lesson["type"])]
            if lesson["subgroup"]:
                fields.append(f'<span class="subgroup">{escape(lesson["subgroup"])}</span>')
            if lesson["note"]:
                fields.append(escape(lesson["note"]))
            fields.append(escape(lesson["teacher"]))
            description = " · ".join(fields)
            for group in lesson["groups"]:
                for parity in lesson["weeks"]:
                    missing[group, parity].append(description)
        parts.append(f'<details name="variants"{" open" if number == 1 else ""}><summary>Вариант {number} · '
                     f'{profiles[variant["profile"]]}</summary>')
        for program in sorted(set(data["programs"])):
            parts.append(f'<details name="programs-{number}"><summary>Направление {escape(program)}</summary>')
            for i, group in enumerate(data["groupLabels"]):
                if data["programs"][i] != program:
                    continue
                parts.append(f'<details name="groups-{number}"><summary>Группа {escape(group)}</summary>')
                for parity in (0, 1):
                    parts.append(f'<section data-parity="{parity}">')
                    for d, day in enumerate(days):
                        parts.append(f"<h3>{day}</h3>")
                        parts.extend(rows.get((i, parity, d), ["<p>В этот день пар нету</p>"]))
                    if missing[i, parity]:
                        parts.append("<p><b>Неразмещённые занятия</b><br>" + "<br>".join(missing[i, parity]) + "</p>")
                    parts.append("</section>")
                parts.append("</details>")
            parts.append("</details>")
        parts.append("</details>")
    return "".join(parts)


def render_calendar(data):
    data = dict(data, groupLabels=[group_label(g) for g in data["groups"]],
                lessons={lid: {**lesson, **lesson_fields(lesson["kind"])} for lid, lesson in data["lessons"].items()})
    template = (ROOT / "calendar.tmpl").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return template.replace("__STATIC_VIEW__", static_view(data)).replace("__CALENDAR_DATA__", payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-open", action="store_true", help="Сохранить календарь без запуска браузера")
    args = parser.parse_args()
    print("Рассчитываю расписание всех групп КНиИТ…", flush=True)
    data = calendar_data()
    path = ROOT / "Календарь КНиИТ.html"
    path.write_text(render_calendar(data), encoding="utf-8")
    print(f"Групп: {len(data['groups'])}. Вариантов: {len(data['variants'])}. {path}")
    if not args.no_open:
        webbrowser.open(path.as_uri())


if __name__ == "__main__":
    main()
