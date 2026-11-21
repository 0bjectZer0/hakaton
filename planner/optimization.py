"""Многократный запуск с бюджетами, разными критериями и проверкой разнообразия."""
from dataclasses import dataclass, field
from math import isfinite
from random import Random
from secrets import randbits
from time import perf_counter

from .constraints import validate
from .evaluation import interval_tokens, jaccard, penalty_breakdown
from .generation import Domains, Search
from .models import Placement
from .weights import PROFILES, adapt_weights


@dataclass(frozen=True)
class Config:
    seed: int = field(default_factory=lambda: randbits(64))
    max_iterations: int = 1000
    time_limit: float = 120.0
    attempts: int = 2
    variants: int = 4
    randomness: float = .25
    adaptive: bool = False

    def __post_init__(self):
        for name, lower in (("attempts", 1), ("variants", 1), ("max_iterations", 0)):
            value = getattr(self, name)
            if type(value) is not int or value < lower:
                raise ValueError(f"{name}: укажите целое число от {lower}")
        if type(self.seed) is not int or type(self.adaptive) is not bool:
            raise ValueError("seed должен быть целым числом, adaptive — true или false")
        if type(self.time_limit) not in (int, float) or not isfinite(self.time_limit) or self.time_limit <= 0:
            raise ValueError("time_limit: укажите положительное конечное число секунд")
        if type(self.randomness) not in (int, float) or not isfinite(self.randomness) or not 0 <= self.randomness <= 1:
            raise ValueError("randomness: укажите число от 0 до 1")


@dataclass
class Result:
    profile: str
    placements: dict[str, Placement]
    metrics: dict
    penalties: dict
    score: float
    baseline_score: float
    missing: tuple
    violations: tuple
    elapsed: float
    iterations: int
    attempts: int
    similarities: tuple
    weights: dict
    adaptive_weights: dict
    timed_out: bool


def different_times(a, b):
    """Замена кабинета или одно лишь удаление занятий не образуют новую альтернативу."""
    return any((p.day, p.period) != (b[k].day, b[k].period) for k, p in a.items() if k in b)


def generate_variants(problem, config=None):
    config = config or Config()
    start = perf_counter()
    deadline = start + config.time_limit
    domains = Domains(problem)
    results, prior_tokens = [], []
    profiles = tuple(PROFILES)
    for index in range(config.variants):
        now = perf_counter()
        if now >= deadline and results:
            break
        # Деление оставшегося времени оставляет бюджет для последующих профилей.
        profile_end = now + max(0, deadline - now) / (config.variants - index)
        name = profiles[index % len(profiles)]
        base = PROFILES[name]
        best = None
        best_key = None
        visits = starts = 0
        hit_deadline = False
        for attempt in range(config.attempts):
            now_attempt = perf_counter()
            if now_attempt >= profile_end and (starts or results):
                break
            attempt_end = now_attempt + max(0, profile_end-now_attempt) / (config.attempts-attempt)
            rng = Random(config.seed + index * 1000003 + attempt)
            search = Search(domains, rng, config.randomness, [r.placements for r in results])
            search.set_weights(base)
            search.construct(attempt_end)
            active_weights = dict(base)
            if config.adaptive:
                active_weights = adapt_weights(base, search.days.metrics())
                search.set_weights(active_weights)
            search.improve(config.max_iterations, attempt_end)
            starts += 1
            visits += search.iterations
            hit_deadline |= perf_counter() >= attempt_end
            placements = search.state.placements
            tokens = interval_tokens(problem, placements)
            similarities = tuple(jaccard(tokens, earlier) for earlier in prior_tokens)
            if any(value > .98 or not different_times(placements, previous.placements)
                   for value, previous in zip(similarities, results)):
                continue
            metrics = search.days.metrics()
            penalties = penalty_breakdown(base, metrics)
            score = sum(penalties.values())
            missing = tuple(k for k in problem.lessons if k not in placements)
            # Сначала полнота, затем качество по фиксированному профилю.
            key = len(missing), score, max(similarities, default=0)
            if best_key is None or key < best_key:
                best_key = key
                best = Result(name, placements, metrics, penalties, score,
                              sum(penalty_breakdown(PROFILES["compromise"], metrics).values()),
                              missing, (), 0., 0, 0, similarities, dict(base), active_weights, False)
        if best is not None:
            best.violations = tuple(validate(problem, best.placements, require_complete=False))
            if best.violations:
                raise RuntimeError("Ошибка проверки назначений: " + "; ".join(best.violations[:3]))
            best.elapsed = perf_counter() - (start if index == 0 else now)
            best.iterations, best.attempts, best.timed_out = visits, starts, hit_deadline
            prior_tokens.append(interval_tokens(problem, best.placements))
            results.append(best)
        if perf_counter() >= deadline:
            break
    return results
