from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "test.user@example.com"

    # Ensure email not already present
    participants = activities[activity]["participants"]
    if email in participants:
        participants.remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # Verify present
    resp = client.get("/activities")
    data = resp.json()
    assert email in data[activity]["participants"]

    # Remove via DELETE endpoint
    resp = client.delete(f"/activities/{activity}/remove?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Removed" in body.get("message", "")

    # Verify removed
    resp = client.get("/activities")
    data = resp.json()
    assert email not in data[activity]["participants"]
