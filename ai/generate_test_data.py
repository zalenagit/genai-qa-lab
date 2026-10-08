"""Ask an LLM for new checkout test data, validate it, and save it as a CSV.

    python -m ai.generate_test_data --count 20

Rows are checked against the real business rules before saving, so a wrong
AI-generated expectation is caught instead of becoming a wrong test.
"""
import argparse
import csv
import io
import re
from pathlib import Path

from ai.llm_client import ask_llm, load_prompt

HEADER = ["id", "first_name", "last_name", "zip", "expected"]


def expected_result(row):
    """The same rules the app enforces: our 'oracle' for AI-generated rows."""
    if not row["first_name"].strip():
        return "first_name is required"
    if not row["last_name"].strip():
        return "last_name is required"
    if not row["zip"].strip():
        return "zip is required"
    if not re.fullmatch(r"\d{5}", row["zip"]):
        return "zip must be 5 digits"
    return "success"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--out", default="data/checkout_data_ai.csv")
    args = parser.parse_args()

    raw = ask_llm(load_prompt("test_data", count=args.count), temperature=0.7)
    raw = raw.strip().removeprefix("```csv").removeprefix("```").removesuffix("```").strip()
    rows = list(csv.DictReader(io.StringIO(raw)))

    good, fixed = [], 0
    for row in rows:
        if set(HEADER) - set(row):
            continue
        row = {k: (row[k] or "") for k in HEADER}
        truth = expected_result(row)
        if row["expected"] != truth:
            print(f"  corrected {row['id']}: AI said '{row['expected']}', rule says '{truth}'")
            row["expected"] = truth
            fixed += 1
        good.append(row)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(good)
    print(f"Saved {len(good)} rows to {args.out} ({fixed} AI expectations corrected).")


if __name__ == "__main__":
    main()
