"""CSV-file implementation of the RunRepository port."""
import csv
import os

from runlog.adapters.run_serializer import FIELDS, from_row, to_row
from runlog.domain.run import Run


class CsvRunRepository:
    """Stores runs in a CSV file with a header row.

    The file is created on the first `add` if it does not exist yet.
    """

    def __init__(self, path: str):
        self._path = path

    def add(self, run: Run) -> None:
        row = to_row(run)
        with open(self._path, "a", newline="", encoding="utf-8") as f:
            if not os.path.exists(self._path):
                f.write(",".join(FIELDS) + "\n")
            f.write(",".join(row[field] for field in FIELDS) + "\n")

    def all(self) -> list[Run]:
        if not os.path.exists(self._path):
            return []
        with open(self._path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, [])
            return [from_row(dict(zip(header, values, strict=True))) for values in reader]
