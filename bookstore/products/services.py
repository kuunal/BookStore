import pickle
from bookstore.redis_setup import get_redis_instance

redis_instance = get_redis_instance()


def set_cache(obj):
    pickled_obj = pickle.dumps(obj)
    redis_instance.set("products", pickled_obj)


def get_cache_item():
    products = redis_instance.get("products")
    if products:
        products = pickle.loads(products)
        return products
    return None
