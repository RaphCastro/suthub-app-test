import json
from setup.config import redis_client, enrollments_collection


async def process_enrollment(enrollment):
    await enrollments_collection.insert_one(enrollment)


async def main():
    while True:
        _, message = redis_client.blpop("enrollments")
        enrollment = json.loads(message)
        await process_enrollment(enrollment)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
