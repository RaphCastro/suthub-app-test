# queue/redis.py
import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "enrollments")

redis_client = redis.from_url(REDIS_URI)


def enqueue_enrollment(enrollment_data):
    redis_client.rpush(REDIS_QUEUE, enrollment_data)
