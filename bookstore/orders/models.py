from django.db import models, connection
from wishlist.models import WishListsManager
from django.core.exceptions import ValidationError
from .services import get_latest_order_id
from login.tasks import order_placed_mail_to_user
from bookstore.book_store_exception import BookStoreError
from bookstore.utility import DataBaseOperations as db
from response_codes import get_response_code

class OrderManager:
    

    @staticmethod
    def filter(user_id, query=None,params=None):
        query = 'select p.*, o.quantity, o.address as quantity_in_order from orders o inner join product p on o.product_id = p.id where o.user_id = %s'
        params = (user_id,)
        records = db.execute_sql(query, params, True)
        objects = []
        if records:
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
        

    @staticmethod
    def insert(obj, total=None, address=None, id = None):
        id = get_latest_order_id()
        mail_response = []
        for orders in obj:
            result = db.execute_sql('select quantity, price, image, title, author from product where id = %s', (orders.product_id,),True)[0]
            available_quantity = result[0]
            price = result[1]
            image = result[2]
            title = result[3]
            author = result[4]
            if not address:
                address = orders.address
                total = orders.quantity * price 
            if  available_quantity == 0 :
                raise BookStoreError(get_response_code('not_available')) 
            if available_quantity < orders.quantity:
                raise BookStoreError(get_response_code('out_of_stock')) 
            
            query = 'insert into orders(user_id, product_id, quantity, address, order_id) values(%s, %s, %s, %s, %s)'

            result =  db.execute_sql(query, (orders.user_id, orders.product_id, orders.quantity, address, id))
            product_info = {
                'title':title,
                'image': image,
                'price':price,
                'author':author,
                'quantity':orders.quantity
            }
            mail_response.append(product_info)
        order_placed_mail_to_user.delay(mail_response, total, obj[0].user_id)   







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
            self.objects.insert([self,])



