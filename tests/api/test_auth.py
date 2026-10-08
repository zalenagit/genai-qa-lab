import pytest

from tests.data_loader import json_cases

pytestmark = pytest.mark.api

STATUS = {
    "success": 200,
    "Invalid username or password": 401,
    "This account is locked": 423,
    "Username is required": 400,
    "Password is required": 400,
}


@pytest.mark.parametrize("case", json_cases("login_users.json"))
def test_login_api(api, case):
    res = api.post(f"{api.base}/login",
                   json={"username": case["username"], "password": case["password"]})
    assert res.status_code == STATUS[case["expected"]], res.text
    body = res.json()
    if case["expected"] == "success":
        assert len(body["token"]) == 32
        assert "password" not in body, "API must never return the password"
    else:
        assert body == {"error": case["expected"]}


def test_malformed_json_body_returns_400(api):
    res = api.post(f"{api.base}/login", data="not json",
                   headers={"Content-Type": "application/json"})
    assert res.status_code == 400


def test_each_login_gets_a_new_token(api):
    creds = {"username": "standard_user", "password": "secret123"}
    first = api.post(f"{api.base}/login", json=creds).json()["token"]
    second = api.post(f"{api.base}/login", json=creds).json()["token"]
    assert first != second
