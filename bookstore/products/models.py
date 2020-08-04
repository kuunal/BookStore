from django.db import models
from django.db import connection 
from bookstore.utility import DataBaseOperations as db 

class ProductManager():

    @staticmethod
    def all(query="select * from product", params=None):
        rows = db.execute_sql(query, params, True)
        objects = []
        for row in rows:
            product_object = Product()
            product_object.id = row[0]
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
            query = f'select * from product where id = %s'
            params = (id,)
        else:
            id = id+"%"
            query = 'select * from product where LOWER(title) like %s or LOWER(author) LIKE %s';
            params = (id,id)
        return ProductManager.all(query, params)
        
    @staticmethod
    def filter(objects):
        result = []
        for obj in objects:
            result.extend(ProductManager.get(str(obj.product_id))) 
        return result



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