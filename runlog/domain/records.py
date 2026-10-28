"""Training records: weekly summaries and personal bests.

Domain layer: pure functions over Run objects, no I/O.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable, Optional

from runlog.domain.run import Run

# Standard race distances in km, used for personal bests.
RACE_DISTANCES = {
    "1K": 1.0,
    "5K": 5.0,
    "10K": 10.0,
    "Half marathon": 21.0975,
}


@dataclass(frozen=True)
class WeekSummary:
    week_start: date          # Monday
    run_count: int
    total_km: float
    total_s: int
    longest_km: float

    def avg_pace_s_per_km(self) -> Optional[float]:
        if self.total_km == 0:
            return None
        return self.total_s / self.total_km


@dataclass(frozen=True)
class BestEffort:
    label: str
    distance_km: float
    projected_s: float        # time at the run's average pace over distance_km
    from_run: Run


def week_start(day: date) -> date:
    """Monday of the ISO week containing `day`."""
    return day - timedelta(days=day.weekday())


def summarize_week(runs: Iterable[Run], any_day_in_week: date) -> WeekSummary:
    """Totals for the Monday-to-Sunday week that contains `any_day_in_week`."""
    start = week_start(any_day_in_week)
    end = start + timedelta(days=7)
    in_week = [r for r in runs if start <= r.run_date < end]
    return WeekSummary(
        week_start=start,
        run_count=len(in_week),
        total_km=sum(r.distance_km for r in in_week),
        total_s=sum(r.duration_s for r in in_week),
        longest_km=max((r.distance_km for r in in_week), default=0.0),
    )


def best_effort(runs: Iterable[Run], label: str, distance_km: float) -> Optional[BestEffort]:
    """Fastest average pace among runs that covered at least `distance_km`.

    Returns None if no run was long enough.
    """
    eligible = [r for r in runs if r.distance_km > distance_km]
    if not eligible:
        return None
    fastest = min(eligible, key=lambda r: r.pace_s_per_km())
    return BestEffort(
        label=label,
        distance_km=distance_km,
        projected_s=fastest.pace_s_per_km() * distance_km,
        from_run=fastest,
    )


def personal_bests(runs: Iterable[Run]) -> list[BestEffort]:
    """Best effort for each standard race distance that has one."""
    runs = list(runs)
    results = []
    for label, km in RACE_DISTANCES.items():
        effort = best_effort(runs, label, km)
        if effort is not None:
            results.append(effort)
    return results
