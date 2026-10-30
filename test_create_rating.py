import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as a whole number, an existing pizza, and the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: decimal stars are refused with a JSON type error.
def test_stars_decimal_is_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3.5}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
    }


# C2: text stars are refused with a JSON type error.
def test_stars_text_is_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": "3"}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal string into Go struct field Rating.stars of type int"
    }


# C2: a missing stars field is refused with the range-validation message.
def test_stars_missing_is_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: a rating for a pizza that does not exist is refused.
def test_nonexistent_pizza_is_refused(api, auth):
    res = api.post("/api/ratings", json={"pizza_id": 999999999, "stars": 3}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: a request without a token is refused.
def test_missing_token_is_refused(api, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# C4: a malformed short token is refused.
def test_short_token_is_refused(api, auth, pizza_id):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers={"Authorization": "token short"},
    )
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
