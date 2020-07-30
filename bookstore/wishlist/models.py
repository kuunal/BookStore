from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models, connection

class WishListsManager:
    
    @staticmethod
    def get(id, user_id):
        query=f'select * from wishlists where product_id=%s and user_id = %s'
        params = (id, user_id)
        return WishListsManager.all(query, params)[0]

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
    def delete(id, user_id):
        try:
            cursor = connection.cursor()
            cursor.execute('delete from wishlists where product_id=%s and user_id=%s' ,(id, user_id))
        finally:
            cursor.close()

    @staticmethod
    def all(query=None,params=None):
        try:
            cursor = connection.cursor()
            objects = []
            if query == None:
                query = 'select * from wishlists where user_id = %s' 
                params = (params,)
            cursor.execute(query, params)
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

    def __init__(self, id=None, user_id=None, product_id=None ):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id

    def save(self):

        if self.id is None:
            self.objects.insert(self)
        else:
            self.objects.update(self)


    