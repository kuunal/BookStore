from django.db import models, connection
from bookstore.utility import DataBaseOperations as db
# Create your models here.

class LoginManager:

    @staticmethod
    def get(user_id):
        cursor = connection.cursor()
        user_email = db.execute_sql('Select email from users where id = %s', (user_id,), False)
        return user_email

