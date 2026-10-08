"""Draft bug reports for failed tests using an LLM.

Run the tests first (they write reports/junit.xml), then:

    python -m ai.bug_reports_from_failures

Drafts are saved to reports/bug-drafts/. A human must review them before filing.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

from ai.llm_client import ask_llm, load_prompt

JUNIT = Path("reports/junit.xml")
OUT = Path("reports/bug-drafts")


def failures(junit_path=JUNIT):
    root = ET.parse(junit_path).getroot()
    for case in root.iter("testcase"):
        for tag in ("failure", "error"):
            node = case.find(tag)
            if node is not None:
                name = f"{case.get('classname')}::{case.get('name')}"
                text = (node.get("message") or "") + "\n" + (node.text or "")
                yield name, text[-4000:]  # keep the prompt small


def main():
    if not JUNIT.exists():
        raise SystemExit("reports/junit.xml not found. Run pytest first.")
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for name, text in failures():
        report = ask_llm(load_prompt("bug_report", test_name=name, failure=text))
        safe = name.replace("/", "_").replace("::", "__").replace("[", "_").replace("]", "")
        (OUT / f"{safe}.md").write_text(report, encoding="utf-8")
        count += 1
        print(f"Drafted bug report for {name}")
    print(f"{count} draft(s) saved to {OUT}/" if count else "No failures. Nothing to report.")


if __name__ == "__main__":
    main()
