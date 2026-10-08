import pytest

from tests.api.schemas import PRODUCT, assert_matches

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_health_check(api):
    res = api.get(f"{api.base}/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@pytest.mark.smoke
def test_list_products_returns_valid_products(api):
    res = api.get(f"{api.base}/products")
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    products = res.json()
    assert len(products) == 4
    for p in products:
        assert_matches(p, PRODUCT)
        assert p["price"] > 0
    assert len({p["id"] for p in products}) == len(products), "product ids must be unique"


def test_get_single_product(api):
    res = api.get(f"{api.base}/products/3")
    assert res.status_code == 200
    assert res.json()["name"] == "Mechanical Keyboard"


@pytest.mark.parametrize("product_id", [0, 99, 999999])
def test_unknown_product_returns_404(api, product_id):
    res = api.get(f"{api.base}/products/{product_id}")
    assert res.status_code == 404
    assert res.json() == {"error": "Product not found"}
