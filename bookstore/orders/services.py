from django.db import connection as cn

def get_latest_order_id():
    try:
        cursor = cn.cursor()
        cursor.execute('select order_id from orders order by order_id desc limit 1')
        id = cursor.fetchone()
        if id:
            id = id[0]+1
        else:
            id=1
        return id
    finally:
        cursor.close()
            