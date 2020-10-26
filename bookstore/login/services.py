from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import connection as cn
from datetime import timedelta
from bookstore import settings
from bookstore.redis_setup import get_redis_instance
from .default_jwt import jwt_decode
from response_codes import get_response_code, OTP_GENERATION_LIMIT
from rest_framework import authentication, exceptions
from bookstore.book_store_exception import BookStoreError
from bookstore.utility import DataBaseOperations as db


"""
    Gives currently logged in user or throws and exception 
"""


def get_current_user(request):
    redis_instance = get_redis_instance()
    token = request.headers.get("x_token")
    user_id = jwt_decode(token)
    for key in redis_instance.scan_iter():
        if key.decode("utf-8") == str(user_id):
            return user_id
    raise BookStoreError(get_response_code("login_required"))


"""
    Makes sure if for applied funtions for user to be logged in
"""


def login_required(func):
    def wrapper(obj=None, request=None, id=None):
        if request == None:
            get_current_user(obj)
            return func(obj)
        get_current_user(request)
        return func(obj, request, id)

    return wrapper


"""
    Blocks user if exceeds otp generation limit
"""


def check_if_otp_generated_for_more_than_limit_for_user(phone_no):
    count = db.execute_sql("select count(*) from otp_history", None, True)
    count = count[0][0]
    if count and count > OTP_GENERATION_LIMIT:
        blocked_time = timezone.now() + timedelta(days=1)
        db.execute_sql("delete from otp_history where phone_no = %s", (phone_no,))
        db.execute_sql(
            "insert into otp_history(phone_no, otp, datetime) values(%s,%s,%s)",
            (phone_no, "blockd", blocked_time),
        )
        raise BookStoreError(get_response_code("too_many_otp"))


"""
    Returns time remaining for unblock for blocked user
"""


def calculate_remaining_block_time(block_time):
    remaining_block_time = (
        timezone.now() - block_time
    ).total_seconds() // settings.OTP_BLOCK_TIME
    print(remaining_block_time, block_time)
    return remaining_block_time


"""
    Checks and ublocks user if block time is expired for certain user
"""


def check_if_user_is_blocked(phone_no):
    block_time = db.execute_sql(
        "select datetime from otp_history where phone_no = %s and otp = %s",
        [phone_no, "blockd"],
        True,
    )
    if block_time:
        block_time = block_time[:1][0][0]
        remaining_time = calculate_remaining_block_time(block_time)
        if remaining_time < 0:
            raise BookStoreError(
                {
                    "status": 400,
                    "message": "You are blocked for trying so many times. Please come back after "
                    + str(abs(remaining_time))
                    + " Hours",
                }
            )
        else:
            db.execute_sql("delete from otp_history where phone_no = %s", [phone_no])
