import uuid

import pytest
import requests

SITE = "https://quickpizza.grafana.com"


class QuickPizza(requests.Session):
    """A session that puts the API site in front of each path."""

    def request(self, method, url, *args, **kwargs):
        if url.startswith("/"):
            url = SITE + url
        kwargs.setdefault("timeout", 20)
        return super().request(method, url, *args, **kwargs)


@pytest.fixture(scope="session")
def api():
    """One cookie-preserving session for the full test run."""
    with QuickPizza() as session:
        yield session


def log_in_new_user(api):
    """Create a user with a new name, log in, and return its Authorization header."""
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 201, f"create user failed: {res.status_code} {res.text}"
    res = api.post("/api/users/token/login", json=user)
    assert res.status_code == 200, f"login failed: {res.status_code} {res.text}"
    return {"Authorization": "token " + res.json()["token"]}


@pytest.fixture
def auth(api):
    """A fresh user and that user's own token for each test."""
    return log_in_new_user(api)


@pytest.fixture
def pizza_id(api, auth):
    """Create a pizza for this test and return its ID."""
    res = api.post("/api/pizza", json={}, headers=auth)
    assert res.status_code == 200, f"pizza request failed: {res.status_code} {res.text}"
    return res.json()["pizza"]["id"]


@pytest.fixture
def rating(api, auth, pizza_id):
    """Create a 3-star rating before the test and delete it afterwards."""
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201, f"create rating failed: {res.status_code} {res.text}"
    made = res.json()
    yield made
    cleanup = api.delete(f"/api/ratings/{made['id']}", headers=auth)
    # The delete-rating test already removed its fixture; QuickPizza reports that as 400.
    assert cleanup.status_code in (204, 400, 404), (
        f"rating cleanup failed: {cleanup.status_code} {cleanup.text}"
    )


@pytest.fixture
def other_auth(api):
    """A second fresh user for owner-access tests."""
    return log_in_new_user(api)
