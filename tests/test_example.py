"""Example tests to copy from. Add your own tests in new files: tests/test_<something>.py"""
from datetime import date

import pytest

from runlog.domain.run import Run
from runlog.use_cases.training import LogRun
from tests.fakes import InMemoryRunRepository


# ---------- Unit test of a domain entity ----------

def test_pace_is_seconds_per_km():
    # Arrange
    run = Run(run_date=date(2026, 10, 1), distance_km=5.0, duration_s=1500)
    # Act
    pace = run.pace_s_per_km()
    # Assert
    assert pace == 300


# ---------- Unit test of a use case, using a fake repository ----------

@pytest.fixture
def repo():
    return InMemoryRunRepository()


def test_log_run_stores_the_run(repo):
    # Arrange
    log_run = LogRun(repo)
    # Act
    log_run.execute(date(2026, 10, 1), distance_km=5.0, duration_s=1500)
    # Assert
    assert len(repo.all()) == 1
    assert repo.all()[0].distance_km == 5.0
