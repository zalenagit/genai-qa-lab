Generate synthetic test data for the checkout form of an online store.

Fields and rules:
- first_name: required, 1-50 characters, may include accents and hyphens
- last_name: required, 1-50 characters
- zip: required, exactly 5 digits

Generate {count} rows: about 60% valid, 20% boundary values, 20% invalid.
Include international names, very long names, whitespace-only values and special characters.
Use only fake data.

Return ONLY CSV (no code fences) with this exact header:
id,first_name,last_name,zip,expected
For valid rows, expected = success. For invalid rows, expected = the exact error message:
"first_name is required", "last_name is required", "zip is required" or "zip must be 5 digits".
Use ids AI-01, AI-02, and so on.
