# Test strategy: ZY Demo Store

*Drafted with AI assistance, then reviewed and edited by the tester.*

## 1. Scope

| In scope | Out of scope |
| --- | --- |
| Login, product list, cart, checkout (web UI) | Real payment processing |
| REST API: auth, products, orders | Performance at production scale |
| Data validation and error messages | Browsers other than Chromium (planned) |
| Basic security: auth required, no password leakage | Penetration testing |

## 2. Approach by level

| Level | Tool | What it covers | Runs |
| --- | --- | --- | --- |
| API | pytest + requests | Status codes, response shape, business rules, auth, validation | Every push |
| Web UI | Playwright (Python) + Page Object Model | Critical user journeys end to end | Every push |
| Data-driven | JSON and CSV files in `data/` | Many input combinations through one test | Every push |
| Smoke | `pytest -m smoke` | Fast critical-path check before full regression | First CI step |
| AI-assisted | `ai/` scripts | Draft test cases, test data and bug reports for human review | On demand |

Most checks live at the API level because they are fast and stable. UI tests cover the journeys a real shopper takes.

## 3. Test design techniques

- **Equivalence partitioning:** valid, invalid and locked users; valid and invalid ZIP codes
- **Boundary values:** quantity 0, 1, 10, 11; ZIP of 4, 5 and 6+ characters
- **State transitions:** order created, read, deleted, then not found
- **Negative testing:** missing token, bad token, malformed JSON, unknown product

## 4. Entry and exit criteria

- **Entry:** the app starts and the `/api/health` check returns `ok`
- **Exit:** 100% of smoke tests pass, at least 95% of the full suite passes, and there are no open Critical or High defects

## 5. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Wrong tax or total calculation | Exact-value assertions in API and UI tests |
| Users see other users' orders | Orders are scoped to the token's user; covered by an auth test |
| Flaky UI tests | Web-first assertions (auto-wait), no fixed sleeps, isolated state per test |
| AI-generated tests or data are wrong | Human review; generated data is re-checked against business rules |

## 6. Reporting

Each run produces `reports/report.html` (readable report) and `reports/junit.xml` (for CI and for AI bug-report drafts).
