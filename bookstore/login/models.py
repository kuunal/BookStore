from django.db import models, connection

# Create your models here.

class LoginManager:

    @staticmethod
    def get(user_id):
        try:
            cursor = connection.cursor()
            cursor.execute('Select email from users where id = %s', (user_id,))
            user_email = cursor.fetchall()[0]
            return user_email
        finally :
            cursor.close()
