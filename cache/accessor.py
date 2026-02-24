import redis

from settings import Setting




def get_redis_connection() -> redis.Redis:
    settings = Setting()
    return redis.Redis(
        host=settings.CACHE_HOSTNAME,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB
    )