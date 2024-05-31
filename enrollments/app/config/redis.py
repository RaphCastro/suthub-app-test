import os
import redis


REDIS_URI = os.getenv("REDIS_URI")
print(REDIS_URI)
redis_client = redis.StrictRedis.from_url(REDIS_URI)
