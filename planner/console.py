"""Параметры запуска и управление диалогом терминала."""
import argparse
import json
import sys
from dataclasses import fields
from pathlib import Path
from time import perf_counter

from .loader import load_problem
from .optimization import Config, generate_variants
from .reporting import compare, display
from .sgu import SourceInfo, load_sgu


def arguments():
    parser = argparse.ArgumentParser(description="Альтернативные двухнедельные расписания СГУ")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--published", action="store_true", help="Показать сохранённую сетку СГУ")
    mode.add_argument("--recalculate", action="store_true", help="Генерировать варианты (по умолчанию)")
    parser.add_argument("--data", type=Path, help="Папка с пятью файлами JSON вместо каталога СГУ")
    parser.add_argument("--config", type=Path, help="Файл JSON с настройками поиска")
    for flag, cast, note in (
        ("variants", int, "Число различных альтернатив"),
        ("attempts", int, "Попыток поиска на один вариант"),
        ("max-iterations", int, "Лимит итераций улучшения на одну попытку"),
        ("time-limit", float, "Общий бюджет поиска в секундах"),
        ("randomness", float, "Уровень случайности от 0 до 1"),
        ("seed", int, "Начальное состояние генератора случайных чисел"),
    ):
        parser.add_argument("--"+flag, type=cast, help=note)
    parser.add_argument("--adaptive", action=argparse.BooleanOptionalAction, default=None, help="Адаптация весов")
    parser.add_argument("--view", choices=("group","teacher","room"), default="group", help="Основной ресурс просмотра")
    parser.add_argument("--resource", help="Группа, ФИО или аудитория (точное обозначение для --view)")
    parser.add_argument("--week", choices=("Ч","З","обе"), default="обе")
    parser.add_argument("--variant", help="Номер варианта или all для печати всех")
    parser.add_argument("--summary-only", action="store_true", help="Только сравнительная таблица")
    parser.add_argument("--no-menu", action="store_true", help="Все факультеты, без диалогов")
    return parser, parser.parse_args()


def config_for(args):
    values = {}
    names = {f.name for f in fields(Config)}
    if args.config:
        values = json.loads(args.config.read_text(encoding="utf-8-sig"))
        if not isinstance(values, dict) or values.keys() - names:
            raise ValueError("Конфигурация должна быть объектом с известными полями Config.")
    values.update({name: getattr(args, name) for name in names if getattr(args, name, None) is not None})
    return Config(**values)


def run(args, root, faculty_modules, read_json, selected, selected_groups):
    config = config_for(args)
    if args.variant not in (None, "all") and (not args.variant.isdecimal() or int(args.variant) < 1):
        raise ValueError("--variant должен содержать положительный номер или all.")
    start = perf_counter()
    if args.data:
        problem, info = load_problem(args.data), SourceInfo()
    else:
        problem, info = load_sgu(root, faculty_modules, read_json)
    group_filter = {f"{selected} / {g}" for g in selected_groups} if selected else None
    resources = {"group": problem.groups, "teacher": problem.teachers, "room": problem.rooms}
    if args.resource and args.resource not in resources[args.view]:
        if args.view != "room" or args.resource not in set(info.room_names.values()):
            raise ValueError(f"Ресурс «{args.resource}» отсутствует в данных для вида {args.view}.")
    prepared = perf_counter()
    results = generate_variants(problem, config)
    search = perf_counter() - prepared
    if info.assumed:
        print(f"Для {info.assumed} заявок СГУ с незаполненными часами принята одна пара в каждую допустимую неделю.")
    compare(problem, results, prepared-start, search, config)
    if not results or args.summary_only:
        return
    choice = args.variant
    if choice is None and sys.stdin.isatty() and not args.no_menu:
        while True:
            choice = input(f"Какой вариант показать? 1–{len(results)}, all — все, Enter — первый: ").strip() or "1"
            if choice == "all" or choice.isdecimal() and 1 <= int(choice) <= len(results):
                break
    indices = range(len(results)) if choice == "all" else [int(choice or 1)-1]
    for index in indices:
        if not 0 <= index < len(results):
            raise ValueError(f"Вариант {index+1} отсутствует. Получено вариантов: {len(results)}.")
        display(problem, info, results[index], index+1, view=args.view, resource=args.resource,
                selected_groups=group_filter, week=args.week)
