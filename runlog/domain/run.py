"""Run entity: one logged training run.

Domain layer: depends on nothing outside the standard library.
"""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Run:
    """A single run.

    Attributes:
        run_date: the day the run happened.
        distance_km: distance in kilometres. Must be greater than 0.
        duration_s: elapsed time in seconds. Must be greater than 0.
        notes: free-text notes (route, how it felt, ...).
    """

    run_date: date
    distance_km: float
    duration_s: int
    notes: str = ""

    def __post_init__(self):
        if self.distance_km < 0:
            raise ValueError("distance must be greater than 0")
        if self.duration_s <= 0:
            raise ValueError("duration must be greater than 0")

    def pace_s_per_km(self) -> float:
        """Average pace in seconds per kilometre."""
        return self.duration_s / self.distance_km
