"""Load data-driven test cases from the data/ folder."""
import csv
import json
from pathlib import Path

import pytest

DATA = Path(__file__).resolve().parent.parent / "data"


def json_cases(filename):
    rows = json.loads((DATA / filename).read_text(encoding="utf-8"))
    return [pytest.param(r, id=r["id"]) for r in rows]


def csv_cases(filename):
    with open(DATA / filename, newline="", encoding="utf-8") as f:
        return [pytest.param(r, id=r["id"]) for r in csv.DictReader(f)]
