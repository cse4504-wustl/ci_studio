# runlog — a running log for the command line

Track your runs, see weekly totals, and find your personal bests.

**This code has 4 bugs in it.** Two of them can be caught by unit tests.
The other two will only show up in integration tests. Your job in the
studio is to write tests that find all four.

## Setup

Requires Python 3.10+. Run these from the `running_log` folder.

**1. Create a virtual environment** (once). It keeps this project's packages
separate from everything else on your computer.

```
python -m venv .venv
```

On some Macs and Linux machines the command is `python3` instead of `python`.

**2. Activate it** (every time you open a new terminal):

| System | Command |
|---|---|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (Command Prompt) | `.venv\Scripts\activate.bat` |

Your prompt now starts with `(.venv)`. If PowerShell refuses to run the
script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

**3. Install the dependencies and run the tests:**

```
python -m pip install -r requirements.txt
python -m pytest
```

The last line of the test output should say **6 passed, 8 skipped**.

When you're done, `deactivate` leaves the virtual environment.

**Using an IDE?** In VS Code or PyCharm, select `.venv` as the project's
Python interpreter so its test runner uses the same packages.

## Using the app

Start the app. It uses `runs.csv` in the current folder unless you pass `--file`:

```
python -m runlog --file sample_data/runs.csv
```

It shows a numbered menu. Options that need more information ask for it one
question at a time, with an example of the format:

```
==== runlog ====
1) Log a run
2) List runs
3) Weekly summary
4) Personal bests
5) Quit
Choose an option (1-5): 1
Date (YYYY-MM-DD, e.g. 2026-10-21): 2026-10-21
Distance in km (e.g. 5.2): 5.2
Duration (mm:ss or h:mm:ss, e.g. 27:45 or 1:05:30): 27:45
Notes (optional, e.g. easy recovery run; press Enter to skip): easy
```

| Option | What it does |
|---|---|
| 1 Log a run | Asks for date, distance, duration and optional notes, then saves the run |
| 2 List runs | All runs, oldest first, with pace |
| 3 Weekly summary | Asks for any day in a week; totals for that Monday–Sunday week (Enter = this week) |
| 4 Personal bests | 1K, 5K, 10K and half marathon, from any run at least that long |
| 5 Quit | Exit |

If an answer doesn't match the format, the app asks again.

## Architecture

The code follows clean architecture. Two pictures help: who **imports** whom,
and who **calls** whom while the app runs.

**Who imports whom.** Every arrow points inward, toward the domain:

```
                    cli.py
           menu, keyboard input, wiring
              │                  │
              ▼                  ▼
          adapters/          use_cases/
              │                  │
              └───────┬──────────┘
                      ▼
                   domain/
```

`adapters/` and `use_cases/` sit side by side: neither imports the other.

| Layer | Files | What's in it |
|---|---|---|
| `domain/` | `run.py`, `records.py` | `Run` and its rules; weekly summaries and personal bests. No I/O. |
| `use_cases/` | `training.py`, `ports.py` | `LogRun`, `ListRuns`, `WeeklySummary`, `PersonalBests`; the `RunRepository` interface they need |
| `adapters/` | `csv_repository.py`, `run_serializer.py`, `presenter.py` | Storing runs in a CSV file; formatting text for the screen |
| `cli.py` | | The menu. Creates a `CsvRunRepository` and hands it to the use cases |

**Who calls whom.** When you log a run:

```
cli.log_run ──► LogRun.execute ──► repo.add(run) ──► CsvRunRepository.add ──► runs.csv
```

At runtime the use case *does* call into the adapter, but it never names it.
`LogRun` only knows it has "some `RunRepository`" (the interface in
`use_cases/ports.py`). `cli.py` decides which one to hand it: a
`CsvRunRepository` in the app, or `tests/fakes.py`'s `InMemoryRunRepository`
in unit tests, so no files are touched. That's why you can unit test a use
case without the file system, and why you need integration tests to check
that it works with the real one.

## Testing

- `tests/test_example.py` shows a domain unit test and a use-case unit test. Copy its style.
- `tests/test_run_validation.py` (unit) and `tests/test_use_cases_with_csv.py` (integration) are **guided exercises**.
  Tests marked `pytest.skip("TODO ...")` are yours to finish; that's why they show as "skipped".
- For the bugs you hunt on your own, create new files: `tests/test_<something>.py`.
- **Unit tests**: domain, use cases (with the fake repository), serializer, presenter. No files.
- **Integration tests**: the use cases running on the real `CsvRunRepository` with a real file
  (e.g. log a run with `LogRun`, then read it back with `ListRuns` through a new repository),
  and optionally the menu end to end.
  Use pytest's `tmp_path` fixture for a throwaway folder and `capsys` to capture printed output.
  To "type" into the menu, pass `scripted_input(...)` from `tests/fakes.py` as `input_fn`;
  each argument is one answer, in order. When the answers run out, the menu exits.

