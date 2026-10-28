"""GUIDED EXERCISE (Part A, step 1): unit testing Run's validation.

Run(run_date, distance_km, duration_s) should refuse to create a run whose
distance or duration makes no sense. Read the docstring in
runlog/domain/run.py: it is the specification you are testing against.

Equivalence classes for distance_km
-----------------------------------
| Class              | Example input | Expected result    |
|--------------------|---------------|--------------------|
| negative           | -1.0          | ValueError         |
| zero (boundary)    | TODO          | TODO               |
| small positive     | 0.1           | Run is created     |
| typical            | 5.0           | Run is created     |

TODO 1: Fill in the zero row above. What does the docstring say?
TODO 2: Write the same kind of table for duration_s (below), then
        finish the tests marked with pytest.skip(...).

Equivalence classes for duration_s
----------------------------------
| Class              | Example input | Expected result    |
|--------------------|---------------|--------------------|
|                    |               |                    |

How to finish a test: delete its pytest.skip(...) line and fill in the
Arrange / Act / Assert steps. Run `python -m pytest -v` after each one.

If a finished test FAILS, stop and ask: is my test wrong, or is the code
wrong? Compare with the docstring. If the code is wrong, you found a bug:
fill in the next bug in tests/BUGS.md. Don't fix the code.
"""
from datetime import date

import pytest

from runlog.domain.run import Run

A_DAY = date(2026, 10, 1)


# ---------- distance_km: two finished examples ----------

def test_typical_distance_is_accepted():
    # Arrange + Act
    run = Run(run_date=A_DAY, distance_km=5.0, duration_s=1500)
    # Assert
    assert run.distance_km == 5.0


def test_negative_distance_is_rejected():
    # Arrange + Act + Assert: pytest.raises checks that the code inside
    # the `with` block raises ValueError. The test fails if it doesn't.
    with pytest.raises(ValueError):
        Run(run_date=A_DAY, distance_km=-1.0, duration_s=1500)


# ---------- distance_km: finish these ----------

def test_small_positive_distance_is_accepted():
    pytest.skip("TODO: finish this test")
    # Arrange + Act: create a Run with distance_km=0.1
    # Assert: the run was created with that distance


def test_zero_distance_is_rejected():
    pytest.skip("TODO: finish this test")
    # Arrange + Act + Assert: like test_negative_distance_is_rejected,
    # but with the zero example from your table


# ---------- duration_s: one test per row of your duration table ----------

def test_typical_duration_is_accepted():
    pytest.skip("TODO: finish this test")


def test_zero_duration_is_rejected():
    pytest.skip("TODO: finish this test")


def test_negative_duration_is_rejected():
    pytest.skip("TODO: finish this test")
