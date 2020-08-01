from django.db import models

# Create your models here.

class OrderManager:
    pass



class OrderModel:
    objects = OrderManager()

    def __init__(self, id=None, order_id=None, user_id=None, quantity=None, total=None, address=None):
        self.id = id
        self.order_id = order_id
        self.user_id = user_id 
        self.quantity = quantity
        self.total = total
        self.address = address



