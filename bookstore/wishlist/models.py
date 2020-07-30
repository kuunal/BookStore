from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models, connection
from response_codes import get_response_code

class WishListsManager:
    
    @staticmethod
    def get(id, user_id, table="wishlists"):
        query=f'select * from '+table+' where product_id=%s and user_id = %s'
        params = ( id, user_id)
        return WishListsManager.all(query, params)[0]

    @staticmethod
    def insert(obj, table="wishlists"):
        try:
            cursor = connection.cursor()
            result = cursor.execute('insert into '+table+'(user_id, product_id) values(%s, %s)',(obj.user_id, obj.product_id))
        except IntegrityError as e:
            raise ValidationError(str(e))
        finally:
            cursor.close()
    
    @staticmethod
    def delete(id, user_id, table="wishlists"):
        try:
            cursor = connection.cursor()
            result = cursor.execute('delete from '+table+' where product_id=%s and user_id=%s' ,(id, user_id))
            return result
        finally:
            cursor.close()

    @staticmethod
    def all(query=None,params=None, table="wishlists"):
        try:
            cursor = connection.cursor()
            objects = []
            if query == None:
                query = 'select * from '+table+' where user_id = %s' 
                params = ( params,)
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


    