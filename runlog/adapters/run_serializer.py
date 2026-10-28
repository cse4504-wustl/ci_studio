"""Converts between Run objects and flat rows (dicts of strings).

Kept separate from the CSV file handling so it can be unit tested
without touching the file system.
"""
from datetime import date

from runlog.domain.run import Run

FIELDS = ["date", "distance_km", "duration_s", "notes"]


def to_row(run: Run) -> dict[str, str]:
    return {
        "date": run.run_date.isoformat(),
        "distance_km": f"{run.distance_km}",
        "duration_s": str(run.duration_s),
        "notes": run.notes,
    }


def from_row(row: dict[str, str]) -> Run:
    return Run(
        run_date=date.fromisoformat(row["date"]),
        distance_km=float(row["distance_km"]),
        duration_s=int(row["duration_s"]),
        notes=row.get("notes", "") or "",
    )
