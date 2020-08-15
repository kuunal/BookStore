from django.db import connection as cn
from bookstore.utility import DataBaseOperations as db
from response_codes import get_response_code

'''
    Get latest order id from database
'''
def get_latest_order_id():
    cursor = cn.cursor()
    id = db.execute_sql('select order_id from orders order by order_id desc limit 1', None, False)
    if id:
        id = id+1
    else:
        id=1
    return id


def generate_cancelled_products(order_status, response, title): 
    try:  
        order_status['products_cancelled']['title'].append(title)
    except KeyError:
        order_status['products_cancelled']['title'] = [title,]
    order_status['products_cancelled']['reason'] = get_response_code(response)
    return order_status



            