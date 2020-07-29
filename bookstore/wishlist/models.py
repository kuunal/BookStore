from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models, connection
from .services import get_current_user

class WishListsManager:
    
    @staticmethod
    def get(id):
        query=f'select * from wishlists where product_id={id}'
        return WishListsManager.all(query)[0]

    @staticmethod
    def insert(obj):
        try:
            cursor = connection.cursor()
            result = cursor.execute('insert into wishlists(user_id, product_id) values(%s, %s)',(obj.user_id, obj.product_id))
        except IntegrityError as e:
            raise ValidationError(str(e))
        finally:
            cursor.close()

    @staticmethod
    def update(obj):
        try:
            cursor = connection.cursor()
            cursor.execute('update wishlists set values(%s,%s) where user_id=%s' ,(obj.user_id, obj.product_id, obj.id))
        finally:
            cursor.close()

    
    @staticmethod
    def delete(id):
        try:
            cursor = connection.cursor()
            cursor.execute('delete from wishlists where product_id=%s and user_id=%s' ,(id,get_current_user()))
        finally:
            cursor.close()

    @staticmethod
    def all(query='select * from wishlists'):
        try:
            cursor = connection.cursor()
            objects = []
            user_id = get_current_user()
            cursor.execute(query)
            wishlists = cursor.fetchall()
            for row in wishlists:
                wishlist_object = WishListModel()
                wishlist_object.user_id = row[1]
                wishlist_object.product_id = row[2]
                objects.append(wishlist_object)
            return objects
        finally:
            cursor.close()


class WishListModel:
    objects = WishListsManager()

    def __init__(self):
        self.id = None
        self.user_id = None
        self.product_id = None

    def save(self):

        if self.id is None:
            self.objects.insert(self)
        else:
            self.objects.update(self)


    