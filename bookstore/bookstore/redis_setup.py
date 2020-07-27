import redis
from . import settings 

def get_redis_instance():
    return redis.StrictRedis(host = settings.REDIS_HOST,
                             port = settings.REDIS_PORT, db = 0)