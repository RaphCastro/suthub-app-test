import os
import redis
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")
REDIS_URI = os.getenv("REDIS_URI")

redis_client = redis.StrictRedis.from_url(REDIS_URI)
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.mydb
enrollments_collection = db.enrollments
