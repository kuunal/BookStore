from django.db import models, connection
from wishlist.models import WishListsManager
from django.core.exceptions import ValidationError
from response_codes import get_response_code
from products.models import Product

class CartManager:

    @staticmethod
    def all(user_id=None, params=None, query=None):
        try:
            cursor = connection.cursor()
            if not query:
                query = 'select p.*, c.quantity, c.user_id as quantity_in_cart from cart c inner join product p on c.product_id = p.id where c.user_id = %s'
                params = (user_id,)
            cursor.execute(query, params)
            result = cursor.fetchall()
            objects = []
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
        finally:
            cursor.close()
        

    @staticmethod
    def get(id, user_id):
        query = 'select p.*, c.quantity from cart c inner join product p on c.product_id = p.id where c.user_id = %s and c.product_id=%s'
        params = (user_id, id)
        return CartManager.all(query=query,params=params)

    @staticmethod
    def insert(obj):
        try:
            cursor = connection.cursor()
            cursor.execute('select quantity from cart where product_id = %s and user_id = %s', (obj.product_id, obj.user_id) )
            count = cursor.fetchone()
            if count:
                count = count[0]
                cursor.execute('select quantity from product where id = %s', (obj.product_id,))
                total_quantity = cursor.fetchone()[0]
                if total_quantity >= int(obj.quantity):
                    result = cursor.execute('update cart set quantity = %s where  product_id = %s and user_id = %s', (int(obj.quantity), obj.product_id, obj.user_id))
                    return get_response_code('updated_quantity')
                else:
                    raise ValidationError("Product out of stock for that quantity")
            query = 'insert into cart(user_id, product_id, quantity) values(%s, %s, %s)'
                    
            return WishListsManager.insert(obj, query, (obj.user_id, obj.product_id, obj.quantity))
        finally:
            cursor.close()

    @staticmethod
    def delete(id, user_id):
        query = 'delete from cart where product_id = %s and user_id = %s'
        return WishListsManager.delete(id, user_id, query)

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

