import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import db
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)

BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")


def get_auth_headers(username, password):
    from base64 import b64encode

    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode("utf-8")
    return {"Authorization": f"Basic {encoded_credentials}"}


@pytest.fixture(autouse=True)
async def setup():
    await db.age_groups.delete_many({})


@pytest.mark.asyncio
async def test_create_age_group():
    age_group_data = {"min_age": 20, "max_age": 30}
    response = client.post(
        "/age-groups/",
        json=age_group_data,
        headers=get_auth_headers(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Age group created successfully"}
    age_group = await db.age_groups.find_one(age_group_data)
    assert age_group is not None


@pytest.mark.asyncio
async def test_update_age_group():
    age_group_data = {"min_age": 20, "max_age": 30}
    response = client.post(
        "/age-groups/",
        json=age_group_data,
        headers=get_auth_headers(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
    )
    assert response.status_code == 200
    age_group = await db.age_groups.find_one(age_group_data)
    age_group_id = str(age_group["_id"])
    new_age_group_data = {"min_age": 25, "max_age": 35}
    response = client.put(
        f"/age-groups/{age_group_id}/",
        json=new_age_group_data,
        headers=get_auth_headers(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Age group updated successfully"}

    updated_age_group = await db.age_groups.find_one({"_id": ObjectId(age_group_id)})
    assert updated_age_group["min_age"] == new_age_group_data["min_age"]
    assert updated_age_group["max_age"] == new_age_group_data["max_age"]


@pytest.mark.asyncio
async def test_delete_age_group():
    age_group_data = {"min_age": 20, "max_age": 30}
    response = client.post(
        "/age-groups/",
        json=age_group_data,
        headers=get_auth_headers(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
    )
    assert response.status_code == 200
    age_group = await db.age_groups.find_one(age_group_data)
    age_group_id = str(age_group["_id"])
    response = client.delete(
        f"/age-groups/{age_group_id}/",
        headers=get_auth_headers(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Age group deleted successfully"}
    deleted_age_group = await db.age_groups.find_one({"_id": ObjectId(age_group_id)})
    assert deleted_age_group is None


@pytest.mark.asyncio
async def test_get_all_age_groups():
    age_groups_data = [
        {"min_age": 20, "max_age": 30},
        {"min_age": 30, "max_age": 40},
        {"min_age": 40, "max_age": 50},
    ]
    for age_group_data in age_groups_data:
        await db.age_groups.insert_one(age_group_data)

    response = client.get(
        "/age-groups/",
        headers=get_auth_headers(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD),
    )
    assert response.status_code == 200

    returned_age_groups = response.json()
    assert len(returned_age_groups) == len(age_groups_data)
    for age_group_data in age_groups_data:
        for group in returned_age_groups:
            group["_id"] = str(group["_id"])
        assert any(
            group["min_age"] == age_group_data["min_age"]
            and group["max_age"] == age_group_data["max_age"]
            for group in returned_age_groups
        )
