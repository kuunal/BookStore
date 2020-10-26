from django.db import models, connection
from bookstore.utility import DataBaseOperations as db
from django.utils import timezone

# Create your models here.


class LoginManager:
    @staticmethod
    def get_user(login_id, password):
        user_email = db.execute_sql(
            "select phone_no from users where (email = %s or phone_no like %s) and password = %s ",
            (login_id, "%" + login_id, password),
            False,
        )
        return user_email

    @staticmethod
    def store_onto_OTP_table(phone_no, random_otp):
        db.execute_sql(
            "insert into otp_history(phone_no, otp, datetime) values(%s, %s, %s)",
            (phone_no, random_otp, timezone.now()),
        )

    @staticmethod
    def get_otp_for_phone_no(phone_no):
        return db.execute_sql(
            "select otp, datetime from otp_history where phone_no = %s",
            [phone_no],
            True,
        )

    @staticmethod
    def get_user_id_from_phone_no(phone_no):
        return db.execute_sql(
            "select id from users where phone_no = %s",
            [
                phone_no,
            ],
            False,
        )

    @staticmethod
    def delete_otp_for_authenticated_user(phone_no):
        db.execute_sql("delete from otp_history where phone_no = %s", [phone_no])
