from django.db import models, connection
from wishlist.models import WishListsManager
from django.core.exceptions import ValidationError
from response_codes import get_response_code
from products.models import Product
from bookstore.utility import DataBaseOperations as db
from bookstore.book_store_exception import BookStoreError
class CartManager:

    @staticmethod
    def all(user_id=None, params=None, query=None):
        if not query:
            query = 'select p.*, c.quantity, c.user_id from cart c inner join product p on c.product_id = p.id where c.user_id = %s'
            params = (user_id,)
        result = db.execute_sql( query, params, many=True)
        objects = []
        if result:
            for row in result:
                obj = CartModel()
                obj.product_id = row[0]
                obj.title = row[1]
                obj.image = row[2]
                obj.quantity = row[7]
                obj.price = row[4]
                obj.description = row[5]
                obj.author = row[6]
                obj.quantity_in_cart = row[7]
                obj.user_id = row[8]

                objects.append(obj)
        return objects
        

    @staticmethod
    def get(id, user_id):
        query = 'select p.*, c.quantity, c.user_id from cart c inner join product p on c.product_id = p.id where c.user_id = %s and c.product_id=%s'
        params = (user_id, id)
        return CartManager.all(query=query,params=params)

    @staticmethod
    def insert(obj):
        total_quantity = db.execute_sql('select quantity from product where id = %s', (obj.product_id,), False)
        if total_quantity >= int(obj.quantity):
            count = db.execute_sql('select quantity from cart where product_id = %s and user_id = %s', (obj.product_id, obj.user_id), False)
            if count:
                result = db.execute_sql('update cart set quantity = %s where  product_id = %s and user_id = %s', (int(obj.quantity), obj.product_id, obj.user_id))
                return get_response_code('updated_quantity')
            query = 'insert into cart(user_id, product_id, quantity) values(%s, %s, %s)'
            db.execute_sql(query, (obj.user_id, obj.product_id, obj.quantity))
            return get_response_code('added_to_cart')
        else:
            raise BookStoreError(get_response_code("out_of_stock"))
        

    @staticmethod
    def delete(id, user_id):
        query = 'delete from cart where product_id = %s and user_id = %s'
        params = (id, user_id,)
        return db.execute_sql(query, params)


    @staticmethod
    def update(id):
        pass

class CartModel(Product):
    objects = CartManager()

    
    def __init__(self, id=None, title=None, image=None, author=None, quantity=None, price=None, description = None, user_id=None, product_id=None):
        self.id = id
        self.title = title
        self.image = image
        self.author = author
        self.quantity = quantity
        self.price = price
        self.description = description
        self.user_id = user_id
        self.product_id = product_id

    def save(self):
        if self.id:
            return self.objects.update(self)
        else:
            return self.objects.insert(self)

