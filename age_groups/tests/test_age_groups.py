import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from app.main import app

load_dotenv()
client = TestClient(app)


@pytest.fixture
def mock_age_group():
    return {"min_age": 18, "max_age": 25}


def test_create_age_group(mock_age_group):
    response = client.post("/age-groups/", json=mock_age_group)
    assert response.status_code == 200
    assert response.json() == mock_age_group


def test_get_all_age_groups():
    response = client.get("/age-groups/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_age_group_by_id(mock_age_group):
    create_response = client.post("/age-groups/", json=mock_age_group)
    age_group_id = create_response.json()["id"]
    response = client.get(f"/age-groups/{age_group_id}/")
    assert response.status_code == 200
    assert response.json() == mock_age_group


def test_update_age_group(mock_age_group):
    create_response = client.post("/age-groups/", json=mock_age_group)
    age_group_id = create_response.json()["id"]
    updated_age_group = {"min_age": 20, "max_age": 30}
    response = client.put(f"/age-groups/{age_group_id}/", json=updated_age_group)
    assert response.status_code == 200
    assert response.json() == updated_age_group


def test_delete_age_group(mock_age_group):
    create_response = client.post("/age-groups/", json=mock_age_group)
    age_group_id = create_response.json()["id"]
    response = client.delete(f"/age-groups/{age_group_id}/")
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Age group {age_group_id} deleted successfully"
    }
