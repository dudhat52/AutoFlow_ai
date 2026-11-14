
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def sample_event(code="FILE_LOCKED"):
    return {
        "event_id": "evt_test",
        "platform": "power_automate",
        "workflow_name": "Test Workflow",
        "execution_id": "run_test",
        "status": "failed",
        "error_code": code,
        "error_message": "Synthetic test failure",
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200



def test_file_locked():
    response = client.post(
        "/api/v1/incidents",
        json=sample_event("FILE_LOCKED"),
    )

    print("\nHTTP Status:", response.status_code)
    print("Validation Details:", response.json())

    assert response.status_code == 200

    result = response.json()
    assert result["category"] == "TRANSIENT"
    assert result["recommended_action"] == "RETRY_CANDIDATE"



def test_missing_column():
    response = client.post(
        "/api/v1/incidents",
        json=sample_event("MISSING_COLUMN"),
    )
    assert response.status_code == 200
    assert response.json()["category"] == "DATA_ERROR"
    assert response.json()["recommended_action"] == "HUMAN_REVIEW"


def test_unknown_error():
    response = client.post(
        "/api/v1/incidents",
        json=sample_event("UNKNOWN_FAILURE"),
    )
    assert response.status_code == 200
    assert response.json()["category"] == "UNKNOWN"


def test_missing_field():
    event = sample_event()
    del event["execution_id"]

    response = client.post(
        "/api/v1/incidents",
        json=event,
    )
    assert response.status_code == 422
