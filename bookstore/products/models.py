from django.db import models
from django.db import connection 
    

class ProductManager():

    @staticmethod
    def all(query="select * from product"):
        cursor = connection.cursor()
        cursor.execute(query)
        objects = []
        for row in cursor.fetchall():
            product_object = Product()
            product_object.author = row[6]
            product_object.title = row[1]
            product_object.image = row[2]
            product_object.quantity = row[3]
            product_object.price = row[4]
            product_object.description = row[5]
            objects.append(product_object)

        return objects

    @staticmethod
    def get(id):
        if id.isnumeric():
            query = f'select * from product where id = {id}';
        else:
            id = id+"%"
            query = f'select * from product where LOWER(title) like "{id}" or LOWER(author) LIKE "{id}"';
        return ProductManager.all(query)
        

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