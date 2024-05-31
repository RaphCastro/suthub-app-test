import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_enrollment():
    return {"name": "John Doe", "age": 25, "cpf": "123456789"}


def test_create_enrollment(mock_enrollment):
    response = client.post("/enrollments/", json=mock_enrollment)
    assert response.status_code == 200
    assert response.json() == {"message": "Enrollment added to the queue"}


def test_get_all_enrollments():
    response = client.get("/enrollments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_enrollment(mock_enrollment):
    create_response = client.post("/enrollments/", json=mock_enrollment)
    enrollment_id = create_response.json()["id"]
    updated_enrollment = {"name": "Jane Doe", "age": 30, "cpf": "987654321"}
    response = client.put(f"/enrollments/{enrollment_id}/", json=updated_enrollment)
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Enrollment {enrollment_id} updated successfully"
    }


def test_delete_enrollment(mock_enrollment):
    create_response = client.post("/enrollments/", json=mock_enrollment)
    enrollment_id = create_response.json()["id"]
    response = client.delete(f"/enrollments/{enrollment_id}/")
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Enrollment {enrollment_id} deleted successfully"
    }
