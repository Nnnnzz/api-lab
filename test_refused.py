import uuid

# A second attempt to create the same username is refused with 400.
def test_duplicate_username_is_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    first = api.post("/api/users", json=user)
    assert first.status_code == 201
    second = api.post("/api/users", json=user)
    assert second.status_code == 400
    assert second.json() == {"error": "username already taken"}


# Logging in with a wrong password is refused with 401.
def test_wrong_password_is_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    created = api.post("/api/users", json=user)
    assert created.status_code == 201
    wrong = api.post(
        "/api/users/token/login",
        json={"username": name, "password": "NotTheRightPassword"},
    )
    assert wrong.status_code == 401
    assert wrong.json() == {"error": "authentication failed"}


# An empty username is refused with 400.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
