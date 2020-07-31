from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models, connection

class WishListsManager:
    
    @staticmethod
    def get(id, user_id, query='select * from wishlists where product_id=%s and user_id = %s', model=None):
        params = (id, user_id)
        if not model:
            model = WishListModel
        return WishListsManager.all(query, params, model)[0]

    @staticmethod
    def insert(obj, query='insert into wishlists(user_id, product_id) values(%s, %s)'):
        try:
            cursor = connection.cursor()
            result = cursor.execute(query,(obj.user_id, obj.product_id))
        finally:
            cursor.close()
    
    @staticmethod
    def delete(id, user_id, query='delete from wishlists where product_id=%s and user_id=%s'):
        try:
            cursor = connection.cursor()
            result = cursor.execute( query,(id, user_id))
            return result
        finally:
            cursor.close()

    @staticmethod
    def all(query=None,params=None, model=None):
        try:
            cursor = connection.cursor()
            objects = []
            if query == None:
                query = 'select * from wishlists where user_id = %s' 
                params = (params,)
                model = WishListModel
            cursor.execute(query, params)
            wishlists = cursor.fetchall()
            for row in wishlists:
                wishlist_object = model()
                wishlist_object.user_id = row[1]
                wishlist_object.product_id = row[2]
                objects.append(wishlist_object)
            return objects
        finally:
            cursor.close()


class WishListModel:
    objects = WishListsManager()

    def __init__(self, id=None, user_id=None, product_id=None ):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id

    def save(self):

        if self.id is None:
            self.objects.insert(self)
        else:
            self.objects.update(self)


    