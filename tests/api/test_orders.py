import pytest

from tests.api.schemas import ORDER, assert_matches

pytestmark = pytest.mark.api

CUSTOMER = {"first_name": "Zalina", "last_name": "Yusop", "zip": "75201"}


def new_order(session, items=None, customer=None):
    return session.post(f"{session.base}/orders", json={
        "items": items if items is not None else [{"product_id": 1, "qty": 2}],
        "customer": customer if customer is not None else CUSTOMER,
    })


@pytest.mark.smoke
def test_create_order_calculates_tax_and_total(auth_api):
    res = new_order(auth_api, items=[{"product_id": 1, "qty": 2}, {"product_id": 2, "qty": 1}])
    assert res.status_code == 201, res.text
    order = res.json()
    assert_matches(order, ORDER)
    assert order["subtotal"] == 209.48          # 2 x 79.99 + 49.50
    assert order["tax"] == 16.76                # 8% rounded to cents
    assert order["total"] == 226.24
    assert order["status"] == "created"


def test_order_lifecycle_create_read_delete(auth_api):
    order_id = new_order(auth_api).json()["id"]

    got = auth_api.get(f"{auth_api.base}/orders/{order_id}")
    assert got.status_code == 200
    assert got.json()["id"] == order_id

    assert auth_api.delete(f"{auth_api.base}/orders/{order_id}").status_code == 204
    assert auth_api.get(f"{auth_api.base}/orders/{order_id}").status_code == 404


def test_order_ids_are_sequential(auth_api):
    first = new_order(auth_api).json()["id"]
    second = new_order(auth_api).json()["id"]
    assert second == first + 1


@pytest.mark.parametrize("method, path", [
    ("post", "/orders"), ("get", "/orders/1001"), ("delete", "/orders/1001")])
def test_orders_require_authentication(api, method, path):
    res = getattr(api, method)(f"{api.base}{path}", json={})
    assert res.status_code == 401
    assert res.json() == {"error": "Authentication required"}


def test_invalid_token_is_rejected(api):
    api.headers["Authorization"] = "Bearer not-a-real-token"
    assert new_order(api).status_code == 401


@pytest.mark.parametrize("items, error", [
    ([], "At least one item is required"),
    ([{"product_id": 99, "qty": 1}], "Unknown product_id 99"),
    ([{"product_id": 1, "qty": 0}], "qty must be an integer from 1 to 10"),
    ([{"product_id": 1, "qty": 11}], "qty must be an integer from 1 to 10"),
    ([{"product_id": 1, "qty": "2"}], "qty must be an integer from 1 to 10"),
], ids=["empty-cart", "unknown-product", "qty-zero", "qty-above-max", "qty-as-string"])
def test_order_item_validation(auth_api, items, error):
    res = new_order(auth_api, items=items)
    assert res.status_code == 400
    assert res.json() == {"error": error}


@pytest.mark.parametrize("field, value, error", [
    ("first_name", "", "first_name is required"),
    ("last_name", "   ", "last_name is required"),
    ("zip", "7520", "zip must be 5 digits"),
    ("zip", "75201-1234", "zip must be 5 digits"),
])
def test_order_customer_validation(auth_api, field, value, error):
    customer = {**CUSTOMER, field: value}
    res = new_order(auth_api, customer=customer)
    assert res.status_code == 400
    assert res.json() == {"error": error}


def test_boundary_quantities_are_accepted(auth_api):
    assert new_order(auth_api, items=[{"product_id": 4, "qty": 1}]).status_code == 201
    assert new_order(auth_api, items=[{"product_id": 4, "qty": 10}]).status_code == 201
