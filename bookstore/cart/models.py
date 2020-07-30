from django.db import models
from wishlist.models import WishListsManager


class CartManager:
    
    @staticmethod
    def all(params=None):
        query = 'select * from cart where user_id = %s'
        return WishListsManager.all(query,(params,), CartModel)
        

    @staticmethod
    def get(id, user_id):
        pass

    @staticmethod
    def insert(obj):
        pass

    @staticmethod
    def delete(id):
        pass

    @staticmethod
    def update(id):
        pass

class CartModel:
    objects = CartManager()

    def __init__(self, id=None, user_id=None, product_id=None, total=None):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.total = total
