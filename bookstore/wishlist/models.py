from django.db import models, connection

class wishlistsModel:
    objects = wishlistsManager()

    def __init__(self):
        self.user_id = None
        self.product_id = None

    def save(self):

        if self.id is None:
            self.objects.insert(self)
        else:
            self.objects.update(self)

class wishlistsManager:
    
    @staticmethod
    def insert(obj):
        try:
            cursor = connection.cursor()
            cursor.execute('insert into wishlists values(%s, %s)',(obj.user_id, obj.product_id))
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
    def delete(obj):
        pass

    @staticmethod
    def all():
        try:
            cursor = connection.cursor()
            cursor.execute('select product_id from wishlists')
            objects = []
            





    