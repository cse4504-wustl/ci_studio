"""Command-line interface: an interactive menu that wires the layers together.

This is the outermost layer. It is the only place that knows about
reading keyboard input, the concrete CsvRunRepository, and printing.

`main` takes an `input_fn` so tests can feed it answers instead of a
person typing them.
"""
import argparse
from datetime import date
from typing import Callable, Optional

from runlog.adapters import presenter
from runlog.adapters.csv_repository import CsvRunRepository
from runlog.use_cases.ports import RunRepository
from runlog.use_cases.training import ListRuns, LogRun, PersonalBests, WeeklySummary

DEFAULT_FILE = "runs.csv"

MENU = """
==== runlog ====
1) Log a run
2) List runs
3) Weekly summary
4) Personal bests
5) Quit"""

InputFn = Callable[[str], str]


# ---------- Parsing typed input ----------

def parse_duration(text: str) -> int:
    """'25:30' -> 1530, '1:02:05' -> 3725, '45' -> 2700 (minutes)."""
    parts = text.strip().split(":")
    if not 1 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"invalid duration '{text}'")
    nums = [int(p) for p in parts]
    if len(nums) == 1:
        return nums[0] * 60
    if len(nums) == 2:
        return nums[0] * 60 + nums[1]
    return nums[0] * 3600 + nums[1] * 60 + nums[2]


def parse_date(text: str) -> date:
    return date.fromisoformat(text.strip())


def parse_distance(text: str) -> float:
    return float(text.strip())


def ask(input_fn: InputFn, prompt: str, parse, default=None):
    """Ask until the answer parses. Blank answer returns `default` if one is given."""
    while True:
        answer = input_fn(prompt).strip()
        if answer == "" and default is not None:
            return default
        try:
            return parse(answer)
        except ValueError:
            print("  Sorry, that doesn't match the format. Try again.")


# ---------- Menu actions ----------

def log_run(repo: RunRepository, input_fn: InputFn) -> None:
    run_date = ask(input_fn, "Date (YYYY-MM-DD, e.g. 2026-10-21): ", parse_date)
    distance = ask(input_fn, "Distance in km (e.g. 5.2): ", parse_distance)
    duration = ask(input_fn, "Duration (mm:ss or h:mm:ss, e.g. 27:45 or 1:05:30): ", parse_duration)
    notes = input_fn("Notes (optional, e.g. easy recovery run; press Enter to skip): ").strip()
    run = LogRun(repo).execute(run_date, distance, duration, notes=notes)
    print("Logged: " + presenter.format_run(run))


def list_runs(repo: RunRepository, input_fn: InputFn) -> None:
    print(presenter.format_runs(ListRuns(repo).execute()))


def weekly_summary(repo: RunRepository, input_fn: InputFn) -> None:
    day = ask(input_fn, "Any day in the week (YYYY-MM-DD, e.g. 2026-10-21; press Enter for this week): ",
              parse_date, default=date.today())
    print(presenter.format_week(WeeklySummary(repo).execute(day)))


def personal_bests(repo: RunRepository, input_fn: InputFn) -> None:
    print(presenter.format_bests(PersonalBests(repo).execute()))


ACTIONS = {
    "1": log_run,
    "2": list_runs,
    "3": weekly_summary,
    "4": personal_bests,
}


# ---------- Entry point ----------

def main(argv: Optional[list[str]] = None, input_fn: InputFn = input) -> int:
    parser = argparse.ArgumentParser(prog="runlog", description="Track your running.")
    parser.add_argument("--file", default=DEFAULT_FILE, help="CSV file to use (default: runs.csv)")
    args = parser.parse_args(argv)
    repo = CsvRunRepository(args.file)

    while True:
        print(MENU)
        try:
            choice = input_fn("Choose an option (1-5): ").strip()
        except EOFError:
            return 0
        if choice == "5":
            print("Goodbye!")
            return 0
        action = ACTIONS.get(choice)
        if action is None:
            print("Please enter a number from 1 to 5.")
            continue
        try:
            action(repo, input_fn)
        except ValueError as e:
            print(f"Error: {e}")
        except EOFError:
            return 0
