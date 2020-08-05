from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models, connection
from response_codes import get_response_code
from bookstore.utility import DataBaseOperations as db


class WishListsManager:
    
    @staticmethod
    def get(id, user_id, query='select * from wishlists where product_id=%s and user_id = %s', model=None):
        params = (id, user_id)
        if not model:
            model = WishListModel
        return WishListsManager.all(query, params, model)[0]

    @staticmethod
    def insert(obj):
        query = 'insert into wishlists(user_id, product_id) values(%s,%s)'
        params = (obj.user_id, obj.product_id)
        db.execute_sql(query, params)
        return get_response_code('added_to_wishlist')

    @staticmethod
    def delete(id, user_id, query='delete from wishlists where product_id=%s and user_id=%s'):
        return db.execute_sql( query,(id, user_id))
        
    

    @staticmethod
    def all(query=None,params=None, model=None):
        objects = []
        if query == None:
            query = 'select * from wishlists where user_id = %s' 
            params = (params,)
            model = WishListModel
        wishlists = db.execute_sql(query, params, True)
        if wishlists:
            for row in wishlists:
                wishlist_object = model()
                wishlist_object.user_id = row[1]
                wishlist_object.product_id = row[2]
                objects.append(wishlist_object)
        return objects
        

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


    