"""Ports: interfaces the use cases need from the outside world.

Adapters (e.g. CsvRunRepository) implement these. Tests can implement
them too, with an in-memory fake.
"""
from typing import Protocol

from runlog.domain.run import Run


class RunRepository(Protocol):
    def add(self, run: Run) -> None:
        """Persist one run."""
        ...

    def all(self) -> list[Run]:
        """Every stored run, in the order they were added."""
        ...
