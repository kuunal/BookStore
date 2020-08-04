from django.db import connection as cn
from bookstore.utility import DataBaseOperations as db

def get_latest_order_id():
    cursor = cn.cursor()
    id = db.execute_sql('select order_id from orders order by order_id desc limit 1', None, False)
    if id:
        id = id+1
    else:
        id=1
    return id


            