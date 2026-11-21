"""Парное сравнение фиксированных и адаптивных весов на одном наборе JSON."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from statistics import mean
from time import perf_counter

from planner.constraints import validate
from planner.loader import load_problem
from planner.optimization import Config, generate_variants

ROOT = Path(__file__).resolve().parent
INPUT_FILES = ("groups.json", "teachers.json", "rooms.json", "subjects.json", "lessons.json")


def dataset_hash(folder):
    digest = sha256()
    for name in INPUT_FILES:
        content = (folder / name).read_bytes()
        digest.update(name.encode("ascii") + b"\0" + len(content).to_bytes(8, "big") + content)
    return digest.hexdigest()


def summary(rows):
    stats = {}
    for name in rows[0]["metrics"]:
        values = [row["metrics"][name] for row in rows]
        stats[name] = {"min": min(values), "mean": mean(values), "max": max(values)}
    complete = [row for row in rows if row["valid_complete"]]
    scores = [row["common_penalty"] for row in complete]
    return {
        "runs": len(rows),
        "complete_runs": len(complete),
        "complete_penalty": {"best": min(scores), "mean": mean(scores), "worst": max(scores)} if scores else None,
        "mean_runtime_seconds": mean(row["runtime_seconds"] for row in rows),
        "hard_conflicts_total": sum(row["hard_conflicts"] for row in rows),
        "unscheduled_total": sum(row["unscheduled"] for row in rows),
        "metrics_all_runs": stats,
    }


def compare(folder, seeds, settings):
    problem = load_problem(folder)
    grouped = {"fixed": [], "adaptive": []}
    for index, seed in enumerate(seeds):
        # Чередуем порядок, чтобы преимущество первого/второго запуска не закрепить за режимом.
        modes = tuple(grouped) if index % 2 == 0 else tuple(reversed(grouped))
        for mode in modes:
            config = Config(seed=seed, adaptive=mode == "adaptive", variants=1, **settings)
            start = perf_counter()
            variants = generate_variants(problem, config)
            elapsed = perf_counter() - start
            if not variants:
                raise RuntimeError(f"Для seed={seed} генератор не вернул результат")
            result = variants[0]
            violations = validate(problem, result.placements, require_complete=False)
            missing = len(problem.lessons.keys() - result.placements.keys())
            grouped[mode].append({
                "seed": seed,
                "profile": result.profile,
                "runtime_seconds": elapsed,
                "hard_conflicts": len(violations),
                "unscheduled": missing,
                "valid_complete": not violations and not missing,
                "common_penalty": result.baseline_score,
                "metrics": dict(result.metrics),
                "iterations": result.iterations,
                "attempts": result.attempts,
                "timed_out": result.timed_out,
                "final_weights": dict(result.adaptive_weights),
            })
    differences = [
        adaptive["common_penalty"] - fixed["common_penalty"]
        for fixed, adaptive in zip(grouped["fixed"], grouped["adaptive"])
        if fixed["valid_complete"] and adaptive["valid_complete"]
    ]
    return {
        "dataset_sha256": dataset_hash(folder),
        "dataset": folder.name,
        "size": {name: len(getattr(problem, name)) for name in ("groups", "teachers", "rooms", "lessons")},
        "config": {**settings, "variants": 1},
        "seeds": list(seeds),
        "score_definition": "Сумма штрафов с одинаковыми компромиссными весами. Меньше — лучше. "
                            "Лучший, средний и худший баллы считаются только для полных допустимых решений.",
        "hard_definition": "Конфликты размещённых занятий проверены отдельно от числа неразмещённых заданий.",
        "summary": {mode: summary(rows) for mode, rows in grouped.items()},
        "matched_complete_pairs": len(differences),
        "paired_adaptive_minus_fixed": differences,
        "runs": grouped,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "examples")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--seed", type=int, default=41)
    parser.add_argument("--iterations", type=int, default=450)
    parser.add_argument("--seconds", type=float, default=20)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--randomness", type=float, default=0.45)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.runs < 2:
        parser.error("--runs должно быть не меньше двух")
    seeds = range(args.seed, args.seed + args.runs)
    config = dict(max_iterations=args.iterations, time_limit=args.seconds,
                  attempts=args.attempts, randomness=args.randomness)
    report = compare(args.data, seeds, config)
    for mode, entry in report["summary"].items():
        print(f"{mode}: полных {entry['complete_runs']}/{entry['runs']}, "
              f"среднее время {entry['mean_runtime_seconds']:.4f} с, "
              f"конфликтов {entry['hard_conflicts_total']}, пропусков {entry['unscheduled_total']}")
        if entry["complete_penalty"]:
            score = entry["complete_penalty"]
            print(f"  Общая шкала штрафов: лучший {score['best']:.2f}, "
                  f"средний {score['mean']:.2f}, худший {score['worst']:.2f}")
        for name, values in entry["metrics_all_runs"].items():
            print(f"  {name}: {values['mean']:.2f} в среднем")
    print(f"Сопоставимых полных пар запусков: {report['matched_complete_pairs']}")
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
