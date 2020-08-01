from django.db import models, connection
from wishlist.models import WishListsManager


class OrderManager:
    

    @staticmethod
    def filter(user_id):
        try:
            cursor = connection.cursor()
            query = ''' select * from orders where o.user_id = %s and paid = %s'''
            params = (user_id, 1,)
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
            cursor.execute('select quantity from product where id = %s', (obj.quantity,))
            if cursor.fetchone()[0] < obj.quantity:
                return None 
            query = 'insert into addresses(user_id, product_id, quantity, address, paid, is_delivered) values(%s, %s, %s, %s, %s, %s)'
            params = (obj.user_id, obj.quantity, obj.product_id, obj.address, 0, 0)
            result =  WishListsManager.insert(query, params)
            if result > 0:
                cursor.execute('update product set quantity = ')
            return result
        except:
            cursor.close()






class OrderModel:
    objects = OrderManager()

    def __init__(self, id=None, order_id=None, user_id=None, quantity=None, total=None, address=None, paid=None, is_delivered=None):
        self.id = id
        self.order_id = order_id
        self.user_id = user_id 
        self.quantity = quantity
        self.total = total
        self.address = address
        self.paid = paid
        self.is_delivered = is_delivered

    def save(self):
        if not self.id:
            self.objects.insert()



