# AI-generated test cases: Checkout (reviewed)

**Source:** `docs/user-stories/checkout.md` → `python -m ai.generate_test_cases docs/user-stories/checkout.md`
**Review notes:** The AI draft had 18 cases. I removed 3 duplicates and corrected 2 expected results (the AI assumed ZIP+4 was valid). I also added the cart-empty-after-order case, which the AI missed. The cases below are the reviewed set, and the Automated column links each one to its test.

| ID | Title | Test Data | Expected Result | Priority | Type | Automated |
| --- | --- | --- | --- | --- | --- | --- |
| TC-01 | Place order with valid details | Aisha / Rahman / 75201 | Confirmation, order number, total $139.85 | High | Functional | CHK-01 |
| TC-02 | Accented and hyphenated names accepted | José / García-López / 10001 | Order succeeds | Medium | Functional | CHK-02 |
| TC-03 | First name missing | "" / Tan / 75201 | "first_name is required" | High | Negative | CHK-03 |
| TC-04 | Last name missing | Mei / "" / 75201 | "last_name is required" | High | Negative | CHK-04 |
| TC-05 | ZIP missing | Ravi / Kumar / "" | "zip is required" | High | Negative | CHK-05 |
| TC-06 | ZIP 4 digits (below boundary) | 7520 | "zip must be 5 digits" | High | Boundary | CHK-06 |
| TC-07 | ZIP 6 digits (above boundary) | 752011 | "zip must be 5 digits" | High | Boundary | CHK-07 |
| TC-08 | ZIP with letters | ABCDE | "zip must be 5 digits" | Medium | Negative | CHK-08 |
| TC-09 | ZIP+4 format rejected | 75201-1234 | "zip must be 5 digits" | Low | Boundary | API test |
| TC-10 | Whitespace-only last name | "   " | "last_name is required" | Medium | Negative | API test |
| TC-11 | Cart is empty after an order | Any valid order | Cart shows "Your cart is empty." | High | Functional | smoke test |
| TC-12 | Checkout without signing in | Open checkout.html signed out | Redirect to login | High | Security | login test |

## Questions raised for the product owner

1. Should ZIP+4 (12345-6789) be accepted? The current rule says no.
2. Is there a maximum name length? It's not stated in the story.
3. Should tax depend on the shipping state instead of a flat 8%?
