import aioredis
from contextlib import asynccontextmanager
from .config import settings

redis = None


async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url(settings.redis_url)  # Create Redis connection
    try:
        yield redis
    finally:
        await redis.close()  # Redis will be closed when FastAPI shuts down, no need to close it per request
