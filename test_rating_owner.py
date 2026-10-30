# A different user cannot read the owner's rating.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert res.status_code == 404
    owner_view = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert owner_view.status_code == 200
    assert owner_view.json() == rating


# A different user cannot update the owner's rating.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    res = api.put(
        f"/api/ratings/{rating['id']}", json={"stars": 1}, headers=other_auth
    )
    assert res.status_code == 400
    owner_view = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert owner_view.status_code == 200
    assert owner_view.json()["stars"] == 3


# A different user cannot delete the owner's rating.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert res.status_code == 400
    owner_view = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert owner_view.status_code == 200
    assert owner_view.json() == rating
