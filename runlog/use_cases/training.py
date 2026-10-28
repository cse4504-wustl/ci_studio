"""Use cases: what a user can do with the running log.

Each use case receives its repository through the constructor
(dependency injection), so it never knows whether runs live in a CSV
file, a database, or a list in a test.
"""
from datetime import date

from runlog.domain.records import BestEffort, WeekSummary, personal_bests, summarize_week
from runlog.domain.run import Run
from runlog.use_cases.ports import RunRepository


class LogRun:
    def __init__(self, repo: RunRepository):
        self._repo = repo

    def execute(self, run_date: date, distance_km: float, duration_s: int, notes: str = "") -> Run:
        run = Run(run_date=run_date, distance_km=distance_km, duration_s=duration_s, notes=notes)
        self._repo.add(run)
        return run


class ListRuns:
    def __init__(self, repo: RunRepository):
        self._repo = repo

    def execute(self) -> list[Run]:
        return sorted(self._repo.all(), key=lambda r: r.run_date)


class WeeklySummary:
    def __init__(self, repo: RunRepository):
        self._repo = repo

    def execute(self, any_day_in_week: date) -> WeekSummary:
        return summarize_week(self._repo.all(), any_day_in_week)


class PersonalBests:
    def __init__(self, repo: RunRepository):
        self._repo = repo

    def execute(self) -> list[BestEffort]:
        return personal_bests(self._repo.all())
