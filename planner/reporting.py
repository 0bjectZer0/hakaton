"""Консольное представление результатов. Вычислительные модули ничего не печатают."""
from collections import defaultdict
from datetime import timedelta

from rooms import week_type

DAYS = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")
PROFILES = {"comfort": "Комфорт студентов", "compact": "Компактность",
            "balance": "Баланс", "compromise": "Компромисс"}
LABELS = {"gaps": "окна групп", "overloaded": "перегруженные дни групп", "single": "дни групп с одной парой",
          "course_time": "отклонение от предпочтительного времени курса",
          "start_spread_hours": "разброс времени начала занятий", "gap_hours": "длительность окон групп",
          "empty": "пустые дни групп", "imbalance": "дисбаланс групп", "active": "учебные дни групп",
          "teacher_gaps": "окна преподавателей", "teacher_overloaded": "перегруженные дни преподавателей",
          "teacher_single": "дни преподавателей с одной парой", "teacher_active": "рабочие дни преподавателей",
          "teacher_imbalance": "дисбаланс преподавателей"}


def compare(problem, variants, preparation, search, config):
    print(f"Подготовка данных {preparation:.2f} с. Поиск вариантов {search:.2f} с. Seed {config.seed}.")
    print(f"Получено вариантов: {len(variants)} из {config.variants}. Заявок: {len(problem.lessons)}.")
    print("№ | Профиль | Полнота | Назначено | Пропущено | Нарушения назначений | Общий штраф | Окна групп | Дни с 1 парой | Перегрузки")
    for i, v in enumerate(variants, 1):
        print(i, PROFILES[v.profile], "частичное" if v.missing else "полное", len(v.placements), len(v.missing), len(v.violations),
              f"{v.baseline_score:.2f}", v.metrics["gaps"], v.metrics["single"], v.metrics["overloaded"], sep=" | ")
        print(f"  Штраф профиля {v.score:.2f}. Итераций {v.iterations}, попыток {v.attempts}, "
              f"время {v.elapsed:.2f} с." + (" Достигнут лимит времени." if v.timed_out else ""))
        print(f"  Для групп: учебных дней {v.metrics['active']}, пустых {v.metrics['empty']}, "
              f"дисбаланс {v.metrics['imbalance']:.2f}.")
        print("  Вклад критериев: " + ", ".join(f"{LABELS.get(k,k)} {value:.2f}" for k,value in v.penalties.items()))
        if v.similarities:
            print("  Сходство: " + ", ".join(f"с №{j} {value:.1%}" for j,value in enumerate(v.similarities, 1)))
    if len(variants) < config.variants:
        print("В пределах бюджета поиска получено меньше различных вариантов, чем запрошено.")


def display(problem, info, variant, number, *, view, resource, selected_groups, week):
    """Отбор меняет только представление. Оценки и допустимость относятся ко всему варианту."""
    label = PROFILES[variant.profile]
    status = "частичное расписание" if variant.missing else "полное расписание"
    print(f"\nВариант {number} · {label} · {status}")
    if variant.violations:
        raise ValueError(f"Вариант содержит нарушения: {variant.violations[:3]}")
    table = defaultdict(list)
    seen = 0
    for lid, placement in variant.placements.items():
        lesson = problem.lessons[lid]
        if selected_groups is not None and selected_groups.isdisjoint(lesson.groups):
            continue
        room = info.room_names.get(placement.room, placement.room)
        groups = ", ".join(lesson.groups)
        values = {"group": lesson.groups, "teacher": (lesson.teacher,), "room": (room, placement.room)}
        if resource is not None and resource not in values[view]:
            continue
        bell = problem.bells[lesson.bell]
        start, end = bell[placement.period][0], bell[placement.period+lesson.duration-1][1]
        subject = " ".join(filter(None, (info.kinds.get(lid), lesson.subject)))
        for w in lesson.weeks:
            if week == "обе" or week == ("Ч","З")[w]:
                table[w, placement.day].append((start, end, groups, lesson.teacher, room, subject))
                seen += 1
    first_week = int(info.monday is not None and week_type(info.monday) == "З")
    for offset, w in enumerate((first_week, 1-first_week)):
        if week != "обе" and week != ("Ч","З")[w]:
            continue
        monday = info.monday + timedelta(days=7*offset) if info.monday else None
        span = f"{monday:%d.%m.%Y} — {monday+timedelta(days=6):%d.%m.%Y} · " if monday else ""
        print(f"\nНеделя {span}{('числитель','знаменатель')[w]}")
        for day in range(problem.days):
            date_text = f"  {monday+timedelta(days=day):%d.%m.%Y}" if monday else ""
            print(f"\n{DAYS[day]}{date_text}")
            if not table[w, day]:
                print("В этот день пар нету")
                continue
            order = {"group": (2,3,4), "teacher": (3,2,4), "room": (4,2,3)}[view]
            labels = {2:"Группы",3:"Преподаватель",4:"Аудитория"}
            print("Время", *(labels[j] for j in order), "Занятие", sep=" | ")
            for row in sorted(table[w, day]):
                a,b = row[:2]
                print(f"{a//60:02}:{a%60:02}–{b//60:02}:{b%60:02}", *(row[j] for j in order), row[5], sep=" | ")
    print(f"\nПоказано занятий за выбранные недели: {seen}.")
    omitted = []
    for lid in variant.missing:
        lesson = problem.lessons[lid]
        if selected_groups is not None and selected_groups.isdisjoint(lesson.groups):
            continue
        if week != "обе" and ("Ч","З").index(week) not in lesson.weeks:
            continue
        possible = {"group":lesson.groups, "teacher":(lesson.teacher,),
                    "room":tuple(info.room_names.get(r,r) for r in lesson.rooms) + lesson.rooms}
        if resource and resource not in possible[view]:
            continue
        omitted.append((lid, lesson.subject, lesson.teacher, ", ".join(lesson.groups),
                        info.issues.get(lid, "Допустимое назначение в этом запуске не найдено")))
    if omitted:
        print("Неразмещённые заявки в выборке:")
        for entry in omitted:
            print(*entry, sep=" | ")
