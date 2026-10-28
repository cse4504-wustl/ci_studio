"""GUIDED EXERCISE (Part B, step 1): integration testing the use cases
with the real CsvRunRepository.

In Part A you unit tested pieces on their own, using InMemoryRunRepository
in place of real storage. Here the use cases run on top of the REAL
repository, which writes a REAL file. pytest's `tmp_path` fixture gives each
test its own empty folder, deleted afterwards, so your real files are safe.

    LogRun ──► CsvRunRepository ──► runs.csv ──► CsvRunRepository ──► ListRuns
                                   (real file)                         WeeklySummary
                                                                       PersonalBests

The pattern for every test here:
    Arrange: a file path in tmp_path (and maybe some file contents)
    Act:     run a use case that WRITES (LogRun) through one repository object
    Assert:  run a use case that READS (ListRuns, WeeklySummary, ...) through a
             NEW repository object on the same path, and check its result

Why a new repository object? It forces the data to go through the file,
like it does when the app is closed and opened again.

Equivalence classes for the file's state
----------------------------------------
| Class                          | Expected                                 |
|--------------------------------|------------------------------------------|
| file doesn't exist yet         | reads return nothing; LogRun creates it  |
| file exists, header only       | a logged run can be read back            |
| file exists with header + runs | reads return every run                   |

How to finish a test: delete its pytest.skip(...) line and fill in the
steps. Run `python -m pytest -v` after each one. If a finished test fails,
look at the file itself:  print((tmp_path / "runs.csv").read_text())
and run `python -m pytest -s` to see the print output. If the code is
wrong, fill in the next bug in tests/BUGS.md. Don't fix the code.
"""
from datetime import date

import pytest

from runlog.adapters.csv_repository import CsvRunRepository
from runlog.use_cases.training import ListRuns, LogRun, WeeklySummary

HEADER = "date,distance_km,duration_s,notes\n"


# ---------- two finished examples ----------

def test_list_runs_with_no_file_returns_nothing(tmp_path):
    # Arrange: a path inside the temp folder; we never create the file
    path = str(tmp_path / "runs.csv")
    # Act + Assert: the READ use case, through the real repository
    assert ListRuns(CsvRunRepository(path)).execute() == []


def test_weekly_summary_reads_existing_file(tmp_path):
    # Arrange: write a file by hand, exactly as the app's file looks
    path = tmp_path / "runs.csv"
    path.write_text(HEADER + "2026-10-01,5.0,1500,easy\n"
                             "2026-10-03,8.0,2700,tempo\n", encoding="utf-8")
    # Act
    summary = WeeklySummary(CsvRunRepository(str(path))).execute(date(2026, 10, 1))
    # Assert
    assert summary.run_count == 2
    assert summary.total_km == 13.0


# ---------- finish these ----------

def test_logged_run_is_listed_when_file_has_header(tmp_path):
    pytest.skip("TODO: finish this test")
    # Arrange: write a file that contains only HEADER
    # Act:     LogRun(CsvRunRepository(path)).execute(<date>, <km>, <seconds>, notes=...)
    # Assert:  ListRuns(CsvRunRepository(path)).execute() returns exactly the run
    #          that LogRun returned


def test_first_logged_run_is_listed_when_file_is_new(tmp_path):
    pytest.skip("TODO: finish this test")
    # Arrange: a path to a file that does NOT exist yet
    # Act:     log one run with LogRun
    # Assert:  ListRuns on a NEW repository returns exactly that run


def test_two_logged_runs_count_in_weekly_summary_when_file_is_new(tmp_path):
    pytest.skip("TODO: finish this test")
    # Arrange: a path to a file that does NOT exist yet
    # Act:     log two runs in the same week with LogRun
    # Assert:  WeeklySummary on a NEW repository counts both runs and their
    #          total distance
