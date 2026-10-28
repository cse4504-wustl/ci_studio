"""Formats domain objects as text for the terminal."""
from runlog.domain.records import BestEffort, WeekSummary
from runlog.domain.run import Run


def format_duration(seconds: float) -> str:
    """1530 -> '25:30', 3725 -> '1:02:05'."""
    total = int(round(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def format_pace(s_per_km: float) -> str:
    return f"{format_duration(s_per_km)} /km"


def format_run(run: Run) -> str:
    line = (f"{run.run_date.isoformat()}  {run.distance_km:6.2f} km  "
            f"{format_duration(run.duration_s):>8}  {format_pace(run.pace_s_per_km())}")
    return f"{line}  {run.notes}" if run.notes else line


def format_runs(runs: list[Run]) -> str:
    if not runs:
        return "No runs logged yet."
    return "\n".join(format_run(r) for r in runs)


def format_week(summary: WeekSummary) -> str:
    lines = [
        f"Week of {summary.week_start.isoformat()}",
        f"  Runs:     {summary.run_count}",
        f"  Distance: {summary.total_km:.2f} km",
        f"  Time:     {format_duration(summary.total_s)}",
        f"  Longest:  {summary.longest_km:.2f} km",
    ]
    pace = summary.avg_pace_s_per_km()
    if pace is not None:
        lines.append(f"  Avg pace: {format_pace(pace)}")
    return "\n".join(lines)


def format_bests(bests: list[BestEffort]) -> str:
    if not bests:
        return "No personal bests yet."
    return "\n".join(
        f"{b.label:<14} {format_duration(b.projected_s):>8}  "
        f"(from {b.from_run.run_date.isoformat()}, {b.from_run.distance_km:.2f} km)"
        for b in bests
    )
