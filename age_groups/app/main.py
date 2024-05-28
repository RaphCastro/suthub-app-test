from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from dotenv import load_dotenv
from app.database.database import db
from app.authentication.auth import get_current_user
from app.models.models import AgeGroup


load_dotenv()
app = FastAPI()


@app.post("/age-groups/", dependencies=[Depends(get_current_user)])
async def create_age_group(age_group: AgeGroup):
    existing_group = await db.age_groups.find_one(
        {"min_age": age_group.min_age, "max_age": age_group.max_age}
    )
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Age group already exists"
        )
    await db.age_groups.insert_one(age_group.dict())
    return {"message": "Age group created successfully"}


@app.get("/age-groups/", dependencies=[Depends(get_current_user)])
async def get_all_age_groups():
    age_groups = await db.age_groups.find().to_list(None)
    for age_group in age_groups:
        age_group["_id"] = str(age_group["_id"])
    return age_groups


@app.put("/age-groups/{group_id}/", dependencies=[Depends(get_current_user)])
async def update_age_group(group_id: str, age_group: AgeGroup):
    existing_group = await db.age_groups.find_one({"_id": ObjectId(group_id)})
    if existing_group is None:
        raise HTTPException(status_code=404, detail="Age group not found")
    await db.age_groups.update_one(
        {"_id": ObjectId(group_id)}, {"$set": age_group.dict()}
    )
    return {"message": "Age group updated successfully"}


@app.delete("/age-groups/{group_id}", dependencies=[Depends(get_current_user)])
async def delete_age_group(group_id: str):
    existing_group = await db.age_groups.find_one({"_id": ObjectId(group_id)})
    if existing_group is None:
        raise HTTPException(status_code=404, detail="Age group not found")
    await db.age_groups.delete_one({"_id": ObjectId(group_id)})
    return {"message": "Age group deleted successfully"}


@app.delete("/age-groups/clear", dependencies=[Depends(get_current_user)])
async def delete_all_age_groups():
    result = await db.age_groups.delete_many({})
    return {"message": f"{result.deleted_count} age groups deleted successfully"}
