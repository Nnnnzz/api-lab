import pytest

# A pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Scissors"],
        ["Knife", "Scissors"],
    ],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    res = api.post("/api/pizza", json={"excludedTools": excluded}, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Excluding all three tools should be a client error with a JSON message, not a 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools returns 500 with an empty body instead of 400 JSON",
    strict=True,
)
def test_all_tools_excluded_is_a_client_error(api, auth):
    res = api.post(
        "/api/pizza",
        json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]},
        headers=auth,
    )
    assert res.status_code == 400
    assert res.text.strip() != ""
    body = res.json()
    assert isinstance(body, dict) and "error" in body
