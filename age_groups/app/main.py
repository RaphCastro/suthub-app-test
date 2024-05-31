from fastapi import FastAPI, Depends, HTTPException
from bson import ObjectId
from dotenv import load_dotenv
from database.database import age_groups_collection
from authentication.auth import get_current_user
from models.models import AgeGroup


load_dotenv()
app = FastAPI()


@app.post("/age-groups/", response_description="Add new age group")
async def create_age_group(
    age_group: AgeGroup, username: str = Depends(get_current_user)
):
    existing_group = await age_groups_collection.find_one(
        {"min_age": age_group.min_age, "max_age": age_group.max_age}
    )
    if existing_group:
        raise HTTPException(
            status_code=400, detail=f"User {username}: Age group already exists"
        )

    age_group_dict = age_group.dict()
    new_age_group = await age_groups_collection.insert_one(age_group_dict)
    created_age_group = await age_groups_collection.find_one(
        {"_id": new_age_group.inserted_id}
    )
    created_age_group["_id"] = str(created_age_group["_id"])
    return created_age_group


@app.get("/age-groups/", response_description="List all age groups")
async def get_all_age_groups(username: str = Depends(get_current_user)):
    age_groups = await age_groups_collection.find().to_list(None)
    for age_group in age_groups:
        age_group["_id"] = str(age_group["_id"])
    return age_groups


@app.put("/age-groups/{id}/", response_description="Update an age group")
async def update_age_group(
    id: str, age_group: AgeGroup, username: str = Depends(get_current_user)
):
    updated_age_group = await age_groups_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": age_group.dict()}, return_document=True
    )
    if updated_age_group:
        updated_age_group["_id"] = str(updated_age_group["_id"])
        return updated_age_group
    raise HTTPException(
        status_code=404, detail=f"User {username}: Age group {id} not found"
    )


@app.delete("/age-groups/{id}/", response_description="Delete an age group")
async def delete_age_group(id: str, username: str = Depends(get_current_user)):
    delete_result = await age_groups_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": f"User {username}: Age group {id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Age group {id} not found")


@app.delete("/age-groups/clear", response_description="Delete all age groups")
async def delete_all_age_groups(username: str = Depends(get_current_user)):
    result = await age_groups_collection.delete_many({})
    return {
        "message": f"User {username}: {result.deleted_count} age groups deleted successfully"
    }
