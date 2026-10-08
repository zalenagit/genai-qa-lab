# AI-first testing: plain-English test examples

AI-first tools such as testRigor let you write tests as plain-English steps, and they find elements by what users see instead of by code locators. That reduces maintenance when the UI changes ("self-healing").
Below, the same journeys from this repo are written in that style for comparison.

```text
login as "standard_user" with password "secret123"
check that page contains "Products"
click "Add to cart" below "Noise-Cancelling Headset"
click "Add to cart" below "USB-C Charging Dock"
click "Cart"
click "Checkout"
enter "Aisha" into "First name"
enter "Rahman" into "Last name"
enter "75201" into "ZIP code"
click "Place order"
check that page contains "Thank you for your order!"
check that page contains "$139.85"
```

## Code-based vs AI-first: when to use which

| | Playwright (this repo) | AI-first tools |
| --- | --- | --- |
| Who writes tests | Engineers | Anyone on the team |
| Maintenance | Locators updated by hand (stable test IDs help) | Self-healing reduces upkeep |
| Control and debugging | Full code control | Less low-level control |
| Cost | Free, open source | Usually paid |
| Best for | Complex logic, API + UI, CI pipelines | Fast coverage of stable business flows |
