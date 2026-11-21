"""Веса профилей и ограниченная обратная связь по измеренным штрафам."""
from math import sqrt

KEYS = ("gaps", "overloaded", "single", "active", "imbalance",
        "teacher_gaps", "teacher_overloaded", "teacher_single", "teacher_active", "teacher_imbalance")

PROFILES = {
    "comfort": dict(zip(KEYS, (12, 18, 12, 2, 1.0, 2, 3, 2, 1, .35))),
    "compact": dict(zip(KEYS, (18, 2, 8, 22, .35, 4, 2, 2, 4, .2)),
                    start_spread_hours=24, gap_hours=15),
    "balance": dict(zip(KEYS, (3, 15, 4, 1, 5, 2, 10, 3, 1, 2))),
    "compromise": dict(zip(KEYS, (8, 10, 7, 7, 2, 4, 5, 3, 3, 1))),
}
for weights in PROFILES.values():
    weights["course_time"] = 8


def adapt_weights(base, metrics):
    """Увеличить базовый вес на 0–60% пропорционально частоте нарушения."""
    result = {}
    for key, weight in base.items():
        prefix = "teacher_" if key.startswith("teacher_") else ""
        days = max(1, metrics.get(prefix + "active", 0) + metrics.get(prefix + "empty", 0))
        frequency = max(0, metrics.get(key, 0)) / days
        result[key] = weight * (1 + .6 * min(1, sqrt(frequency)))
    return result
