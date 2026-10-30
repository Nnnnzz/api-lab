import pytest

# Boundary values: 0 and 6 are refused; 1 and 5 are saved.
@pytest.mark.parametrize(
    ("stars", "expected_status"),
    [(0, 400), (1, 200), (5, 200), (6, 400)],
)
def test_update_rating_boundary_values(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status

    read_back = api.get(path, headers=auth)
    assert read_back.status_code == 200
    expected_stars = stars if expected_status == 200 else 3
    assert read_back.json()["stars"] == expected_stars
