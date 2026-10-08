# GenAI for QA Lab

![tests](https://github.com/zalenagit/genai-qa-lab/actions/workflows/tests.yml/badge.svg)

A hands-on portfolio project that applies **generative AI to QA and test automation**: AI-assisted test design, a Playwright web automation framework, REST API automation, data-driven testing, AI-drafted bug reports, and a private offline LLM option. All of it runs in CI on GitHub Actions.

It tests **ZY Demo Store**, a small web shop plus REST API included in this repo. The tests run offline, without depending on public demo sites that change or go down.

> Built while studying the *GenAI for QA – Masterclass in Testing & Automation* course (Packt, via O'Reilly). The code and documents here are my own implementation of those ideas, not course material.

## What this project shows

| Skill | Where to look |
| --- | --- |
| AI-assisted test strategy and test cases (human-reviewed) | `docs/test-strategy.md`, `docs/ai-generated-test-cases.md` |
| Prompt engineering for QA | `ai/prompts/` |
| Web automation framework with the Page Object Model (Playwright, Python) | `pages/`, `tests/web/` |
| REST API automation: status codes, schema, auth, validation | `tests/api/` |
| Data-driven tests from JSON and CSV | `data/`, `tests/data_loader.py` |
| AI-generated test data, validated against business rules | `ai/generate_test_data.py` |
| Retry of failed tests plus HTML and JUnit reporting | `pytest.ini`, `reports/` |
| AI-drafted bug reports from test failures | `ai/bug_reports_from_failures.py`, `docs/bug-report-example.md` |
| Mobile test cases written with AI | `docs/mobile-test-cases.md` |
| Private offline LLM for confidential testing | `docs/private-llm-setup.md` |
| AI-first, plain-English testing compared with code | `docs/testrigor-plain-english.md` |
| CI pipeline: smoke tests first, then full regression | `.github/workflows/tests.yml` |

## Course topics → this repo

| Course chapter | Implemented as |
| --- | --- |
| Setting up AI assistants | `ai/llm_client.py`: one wrapper for Gemini (cloud) or Ollama (local) |
| Prompt engineering principles | Role + context + task + format templates in `ai/prompts/` |
| Functional testing with AI (strategy, API cases, mobile cases, test data, bug reports) | `docs/` + `ai/` scripts |
| Building web automation frameworks with AI | Playwright + POM, data-driven tests, retries, HTML report |
| API automation with AI | pytest + requests API suite (the course uses Java Rest Assured; I implemented the same ideas in Python) |
| Pair programming with AI tools | Page objects and tests drafted with AI coding assistants, then reviewed and refactored |
| Private offline AI assistants | `LLM_PROVIDER=ollama` |
| AI-first automation and self-healing | `docs/testrigor-plain-english.md` |

## Quick start

```bash
git clone https://github.com/zalenagit/genai-qa-lab.git
cd genai-qa-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium

pytest -m smoke        # fast critical checks
pytest                 # full suite → reports/report.html
pytest -m api          # API tests only
pytest -m web --headed # watch the browser run
```

Try the app yourself with `python -m app.server`, then open http://127.0.0.1:8000. Sign in as `standard_user` / `secret123`.

## AI helpers

```bash
cp .env.example .env   # add your Gemini key, or set LLM_PROVIDER=ollama

python -m ai.generate_test_cases docs/user-stories/checkout.md   # draft test cases
python -m ai.generate_test_data --count 20                       # draft + validate test data
pytest; python -m ai.bug_reports_from_failures                   # draft bug reports for failures
```

**My rule for AI in testing:** AI drafts and I decide. Every generated test case, data row and bug report is reviewed before it enters the suite. The test-data generator re-checks each AI-written expectation against the real business rules and corrects the ones that are wrong.

## Project structure

```
app/            ZY Demo Store: web pages + REST API (Python standard library only)
pages/          Page Object Model classes
tests/web/      Playwright UI tests (login, cart, checkout)
tests/api/      REST API tests (products, auth, orders)
data/           Data-driven test inputs (JSON, CSV)
ai/             LLM client, prompt templates, AI helper scripts
docs/           Test strategy, reviewed AI test cases, mobile cases, guides
.github/        CI workflow
```

## Test coverage summary

- **Web:** login (8 data-driven cases plus a redirect check), product list, cart badge, quantities and subtotal, remove item, checkout (8 data-driven cases), cart cleared after an order
- **API:** health, product list and schema, 404s, login status codes, malformed JSON, unique tokens, order create/read/delete lifecycle, tax and total math, auth required, quantity and customer validation, boundary quantities

## Author

**Zalina M. Yusop**, AI-QA Engineering Analyst · [LinkedIn](https://www.linkedin.com/in/zalina-yusop-b2624b211/)
