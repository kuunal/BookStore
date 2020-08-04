from django.db import models, connection
from wishlist.models import WishListsManager
from django.core.exceptions import ValidationError
from .services import get_latest_order_id
from login.tasks import order_placed_mail_to_user
from bookstore.book_store_exception import BookStoreError

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
    def insert(obj, total=None, address=None, id = None):
        try:
            print(obj)
            cursor = connection.cursor()
            id = get_latest_order_id()
            mail_response = []
            for orders in obj:
                cursor.execute('select quantity, price, image, title, author from product where id = %s', (orders.product_id,))
                result = cursor.fetchone()
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

                result =  cursor.execute(query, (orders.user_id, orders.product_id, orders.quantity, address, id))
                if result:
                    if len(obj) > 1:
                        cursor.execute('delete from cart where product_id = %s and user_id=%s', (orders.product_id, orders.user_id))
                    cursor.execute('update product set quantity = quantity-%s where id = %s', (orders.quantity, orders.product_id))
                product_info = {
                    'title':title,
                    'image': image,
                    'price':price,
                    'author':author,
                    'quantity':orders.quantity
                }
                mail_response.append(product_info)
            order_placed_mail_to_user.delay(mail_response, total, obj[0].user_id)   
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
            self.objects.insert([self,])



