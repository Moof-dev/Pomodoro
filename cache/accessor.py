import redis

from settings import Setting

settings = Setting()


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=settings.CACHE_HOSTNAME,
        port=settings.CACHE_PORT,
        db=0,
        decode_responses=True
    )