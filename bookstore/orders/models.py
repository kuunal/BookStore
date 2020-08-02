from django.db import models, connection
from wishlist.models import WishListsManager
from django.core.exceptions import ValidationError


class OrderManager:
    

    @staticmethod
    def filter(user_id, query=None,params=None):
        try:
            cursor = connection.cursor()
            query = 'select p.*, o.quantity, o.address as quantity_in_order from orders o inner join product p on o.product_id = p.id where o.user_id = %s'
            params = (user_id,)
            cursor.execute(query, params)
            records = cursor.fetchall()
            objects = []
            for row in records:
                order_object = OrderModel()
                order_object.id = row[0]
                order_object.title = row[1]
                order_object.image = row[2] 
                order_object.price = row[4]
                order_object.description=row[5]
                order_object.author = row[6]
                order_object.quantity = row[7]
                order_object.address = row[8]
                objects.append(order_object)
            return objects  
        except:
            cursor.close()

    @staticmethod
    def insert(obj, params=None, total=None):
        try:
            cursor = connection.cursor()
            cursor.execute('select order_id from orders order by order_id desc limit 1')
            id = cursor.fetchone()
            if id:
                id = id[0]
            else:
                id=1
            cursor.execute('select quantity,price from product where id = %s', (obj.product_id,))
            available_quantity = cursor.fetchone()[0]
            price = cursor.fetchone()[1]
            if not params:
                params = [(obj.user_id, obj.product_id, obj.quantity, obj.address, id),]
                total = obj.quantity * price 
            for orders in params:
                if  available_quantity == 0 :
                    raise ValidationError("Product out of stock") 
                if available_quantity < obj.quantity:
                    raise ValidationError("Product out of stock for that quantity") 
                
                query = 'insert into orders(user_id, product_id, quantity, address, order_id) values(%s, %s, %s, %s, %s)'

                result =  cursor.execute(query, orders)
                if result:
                    cursor.execute('update product set quantity = quantity-%s where id = %s', (obj.quantity, obj.product_id))
                return result
        
        finally:
            cursor.close()






class OrderModel:
    objects = OrderManager()

    def __init__(self, id=None, product_id=None, user_id=None, quantity=None, price=None, total=None, address=None):
        self.id = id
        self.product_id = product_id
        self.user_id = user_id 
        self.quantity = quantity
        self.total = total
        self.price = price
        self.address = address

    def save(self):
        if not self.id:
            self.objects.insert(self)



