from django.db import models, connection
from wishlist.models import WishListsManager


class OrderManager:
    

    @staticmethod
    def filter(user_id, query=None,params=None):
        try:
            cursor = connection.cursor()
            query = ''' select * from orders where o.user_id = %s and paid = %s'''
            params = (user_id, 0,)
            cursor.execute(query, params)
            records = cursor.fetchall()
            for row in records:
                order_object = OrderModel()
                order_object.id = row[0]
                order_object.order_id = row[1]
                order_object.user_id = row[2] 
                order_object.quantity = row[3]
                order_object.total = row[4]
                order_object.address = row[6]
        except:
            cursor.close()

    @staticmethod
    def insert(obj):
        try:
            cursor = connection.cursor()
            query = 'insert into orders(user_id, product_id, quantity, address) values(%s, %s, %s, %s)'
            params = (obj.user_id, obj.quantity, obj.product_id, obj.address, 0, 0)
            result =  WishListsManager.insert(None,query, params)
            if result:
                cursor.execute('update orders set total = (select price from product where id=%s,)* obj.quantity where user_id =%s and product_id=%s', (obj.product_id, obj.user_id, obj.product_id))
                cursor.execute('update product p1 join product p2 set p1.quantity = p2.quantity-%s where p1.id = %s', (obj.product_id, obj.quantity, obj.product_id))
            return result
        except:
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



