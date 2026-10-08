"""Tiny response-shape checker (no extra dependency).

Each schema maps a field name to its expected Python type(s).
"""

PRODUCT = {"id": int, "name": str, "price": (int, float)}
ORDER = {"id": int, "username": str, "items": list, "customer": dict,
         "subtotal": (int, float), "tax": (int, float), "total": (int, float), "status": str}


def assert_matches(obj, schema):
    missing = set(schema) - set(obj)
    assert not missing, f"missing fields: {missing}"
    for field, expected_type in schema.items():
        assert isinstance(obj[field], expected_type), (
            f"{field} should be {expected_type}, got {type(obj[field]).__name__}")
