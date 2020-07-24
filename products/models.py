from django.db import models
from django.db import connection 

# Create your models here.
class Product:
    objects = ProductManager()

    def __init__(self):
        self.id = None
        self.author = None
        self.title = None
        self.image = None
        self.price = None
        self.quantity = None
        self.description = None

   
    
class ProductManager():

    @staticmethod
    def isnull(value):
        return True if value else False
    
    @staticmethod
    def is_integer(value):
        return True if type(value) == int else False

    @staticmethod
    def all(query="select * from product"):
        cursor = connection.cursor(query)
        cursor.execute()
        objects = []
        for row in cursor.fetchall():
            product_object = Product()
            product_object.author = row[7]
            product_object.title = row[2]
            product_object.image = row[3]
            product_object.quantity = row[4]
            product_object.price = row[5]
            product_object.description = row[6]
            objects.append(product_object)

        return objects

    @staticmethod
    def get(id):
        query = f'select * from product where id = {id}';
        return ProductManager.all(query)
