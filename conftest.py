"""Shared pytest fixtures.

The ZY Demo Store is started in-process once per test session, so tests need
no external site and run the same way locally and in CI.
"""
import pytest
import requests

from app.server import STORE, start_server

VALID_USER = {"username": "standard_user", "password": "secret123"}


@pytest.fixture(scope="session")
def app_url():
    server, url = start_server()
    yield url
    server.shutdown()


@pytest.fixture(autouse=True)
def clean_store():
    """Every test starts with no orders and no sessions (test isolation)."""
    STORE.reset()
    yield


@pytest.fixture
def api(app_url):
    """A requests session pointed at the API, plus the base URL."""
    session = requests.Session()
    session.base = app_url + "/api"
    yield session
    session.close()


@pytest.fixture
def auth_api(api):
    """An API session that is already logged in as the standard user."""
    res = api.post(f"{api.base}/login", json=VALID_USER)
    assert res.status_code == 200, res.text
    api.headers["Authorization"] = f"Bearer {res.json()['token']}"
    return api


@pytest.fixture
def logged_in_page(page, app_url):
    """A browser page that has already signed in through the UI."""
    from pages.login_page import LoginPage

    LoginPage(page, app_url).open().login(**VALID_USER)
    page.wait_for_url("**/inventory.html")
    return page
