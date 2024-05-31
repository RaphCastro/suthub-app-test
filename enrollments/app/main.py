import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from bson import ObjectId
from database.database import enrollments_collection, age_groups_collection
from authentication.auth import get_current_user
from models.enrollment import Enrollment, EnrollmentInDB
from config.redis import redis_client

load_dotenv()
app = FastAPI()


async def is_age_within_age_groups(age: int) -> bool:
    age_groups = await age_groups_collection.find().to_list(None)
    for age_group in age_groups:
        if age_group["min_age"] <= age <= age_group["max_age"]:
            return True
    return False


@app.post(
    "/enrollments/",
    response_description="Add new enrollment",
    response_model=EnrollmentInDB,
)
async def create_enrollment(
    enrollment: Enrollment, username: str = Depends(get_current_user)
):
    if not await is_age_within_age_groups(enrollment.age):
        raise HTTPException(
            status_code=400,
            detail=f"User {username}: Age is not within any registered age groups",
        )

    enrollment_dict = enrollment.dict()
    redis_client.lpush("enrollments", json.dumps(enrollment_dict))
    return {"message": "Enrollment added to the queue"}


@app.get(
    "/enrollments/",
    response_description="List all enrollments",
    response_model=list[EnrollmentInDB],
)
async def list_enrollments(username: str = Depends(get_current_user)):
    enrollments = await enrollments_collection.find().to_list(None)
    for enrollment in enrollments:
        enrollment["id"] = str(enrollment["_id"])
    return {
        f"User {username}": [EnrollmentInDB(**enrollment) for enrollment in enrollments]
    }


@app.put(
    "/enrollments/{id}/",
    response_description="Update an enrollment",
    response_model=EnrollmentInDB,
)
async def update_enrollment(
    id: str, enrollment: Enrollment, username: str = Depends(get_current_user)
):
    updated_enrollment = await enrollments_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": enrollment.dict()}, return_document=True
    )
    if updated_enrollment:
        updated_enrollment["id"] = str(updated_enrollment["_id"])
        return {f"User {username}": EnrollmentInDB(**updated_enrollment)}
    raise HTTPException(status_code=404, detail=f"Enrollment {id} not found")


@app.delete("/enrollments/{id}/", response_description="Delete an enrollment")
async def delete_enrollment(id: str, username: str = Depends(get_current_user)):
    delete_result = await enrollments_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {f"User {username}: ": f"Enrollment {id} deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f"User {username}: Enrollment {id} not found"
    )


@app.delete("/enrollments/clear", response_description="Delete all enrollments")
async def delete_all_enrollments(username: str = Depends(get_current_user)):
    result = await enrollments_collection.delete_many({})
    return {
        "message": f"User {username}: {result.deleted_count} enrollments deleted successfully"
    }
