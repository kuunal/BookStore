from django.db import models
from wishlist.models import WishListsManager


class CartManager:
    
    @staticmethod
    def all(params=None):
        query = 'select * from cart where user_id = %s'
        return WishListsManager.all(query,(params,), CartModel)
        

    @staticmethod
    def get(id, user_id):
        query = 'select * from cart where id = %s and user_id =%s'
        model = CartModel
        return WishListsManager.get(id, user_id, query, model)

    @staticmethod
    def insert(obj):
        query = 'insert into cart(user_id, product_id) values(%s, %s)'
        return WishListsManager.insert(obj, query)

    @staticmethod
    def delete(id, user_id):
        query = 'delete from cart where product_id = %s and user_id = %s'
        return WishListsManager.delete(id, user_id, query)

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

    def save(self):
        if self.id:
            self.objects.update(self)
        else:
            self.objects.insert(self)
