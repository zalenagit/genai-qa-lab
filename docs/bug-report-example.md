# Example: AI-drafted bug report (after human review)

*Drafted by `python -m ai.bug_reports_from_failures` from a failing test, then verified and edited by the tester.*

**Title:** Order total shows $139.84 instead of $139.85 for headset + dock

**Severity:** High. Customers are charged an incorrect amount.

**Environment:** ZY Demo Store build `main@a1b2c3d`, Chromium 1xx, Ubuntu (GitHub Actions)

**Steps to reproduce:**
1. Sign in as `standard_user`.
2. Add Noise-Cancelling Headset ($79.99) and USB-C Charging Dock ($49.50) to the cart.
3. Check out with Aisha / Rahman / 75201.

**Expected result:** Total = $129.49 + 8% tax ($10.36) = **$139.85**

**Actual result:** Total shows **$139.84**

**Suspected area:** Tax rounding in the order API (truncating instead of rounding to cents)

**Classification:** Product bug. The API response total is wrong, and the UI shows exactly what the API returns.

**Evidence:** `reports/report.html`, failing test `tests/web/test_checkout.py::test_checkout_form[CHK-01]`, API response JSON

> This example illustrates the workflow. It was created by temporarily introducing a rounding defect.
