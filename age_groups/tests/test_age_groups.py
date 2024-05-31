import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_age_group():
    return {"min_age": 18, "max_age": 25}


def return_headers():
    correct_username = os.getenv("BASIC_AUTH_USERNAME")
    correct_password = os.getenv("BASIC_AUTH_PASSWORD")
    return f"Basic:{correct_username}:{correct_password}"

def test_create_age_group(mock_age_group):
    client.delete("/age-groups/clear")
    response = client.post("/age-groups/", json=mock_age_group, headers=return_headers())
    assert response.status_code == 200
    assert response.json() == mock_age_group


def test_get_all_age_groups():
    response = client.get("/age-groups/", headers=return_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_age_group(mock_age_group):
    create_response = client.post("/age-groups/", json=mock_age_group, headers=return_headers())
    age_group_id = create_response.json()
    updated_age_group = {"min_age": 20, "max_age": 30}
    response = client.put(f"/age-groups/{age_group_id}/", json=updated_age_group)
    assert response.status_code == 200
    assert response.json() == updated_age_group


def test_delete_age_group(mock_age_group):
    create_response = client.post("/age-groups/", json=mock_age_group, headers=return_headers())
    age_group_id = create_response.json()
    response = client.delete(f"/age-groups/{age_group_id}/")
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Age group {age_group_id} deleted successfully"
    }
