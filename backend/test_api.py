from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_statistics():
    response = client.get("/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "total_events" in data
    assert "high_risk_users" in data
    assert "average_risk" in data

def test_get_events():
    response = client.get("/events?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_alerts():
    response = client.get("/alerts?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_analytics():
    response = client.get("/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "attack_distribution" in data
    assert "roc_curve" in data
    assert "pr_curve" in data
    assert "confusion_matrix" in data
    assert "shap_importance" in data

def test_ask_copilot():
    payload = {"question": "What is the status of the system?"}
    response = client.post("/copilot", json=payload)
    assert response.status_code == 200
    assert "answer" in response.json()

def test_predict_event():
    event_payload = {
        "event_id": "test_id",
        "user_id": 1,
        "device_id": 1,
        "timestamp": "2026-07-26T12:00:00Z",
        "action": "Login",
        "resource": "Payroll",
        "status": "Success",
        "bytes_transferred": 500,
        "ip_address": "192.168.1.1",
        "location": "USA",
        "session_duration": 120,
        "failed_attempts": 0,
        "login_status": "success",
        "country": "USA",
        "authentication_method": "Password"
    }
    # Using the 'with' block triggers the FastAPI lifespan events (loads ML models)
    with TestClient(app, raise_server_exceptions=True) as live_client:
        response = live_client.post("/predict", json={"event": event_payload})
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "risk_score" in data
        assert "risk_level" in data
        assert "execution_time_ms" in data
