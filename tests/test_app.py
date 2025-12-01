from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # check a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure email not present initially
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    participants = activities[activity]["participants"]
    if email in participants:
        # cleanup if someone left a leftover from previous runs
        client.delete(f"/activities/{activity}/unregister?email={email}")

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    result = resp.json()
    assert "Signed up" in result.get("message", "")

    # Verify participant added
    resp = client.get("/activities")
    activities = resp.json()
    assert email in activities[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    result = resp.json()
    assert "Unregistered" in result.get("message", "")

    # Verify participant removed
    resp = client.get("/activities")
    activities = resp.json()
    assert email not in activities[activity]["participants"]
