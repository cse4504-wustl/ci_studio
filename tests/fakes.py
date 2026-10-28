"""Test doubles for unit testing use cases without the file system."""
from runlog.domain.run import Run


class InMemoryRunRepository:
    """Implements the RunRepository port with a plain list."""

    def __init__(self, runs: list[Run] | None = None):
        self.runs = list(runs or [])

    def add(self, run: Run) -> None:
        self.runs.append(run)

    def all(self) -> list[Run]:
        return list(self.runs)


def scripted_input(*answers: str):
    """Fake `input()` for testing the menu: returns the answers in order.

    Pass it to runlog.cli.main(..., input_fn=scripted_input("2", "5")).
    When the answers run out it raises EOFError, which makes the menu exit.
    """
    remaining = list(answers)

    def fake_input(prompt: str = "") -> str:
        if not remaining:
            raise EOFError
        return remaining.pop(0)

    return fake_input
