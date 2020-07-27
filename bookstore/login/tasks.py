from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .otp import send_otp


MESSAGE_FOR_LOGIN="Your otp is "


@shared_task
def send_otp_to_user_while_login(phone_no, random_otp):
    send_otp(phone_no, random_otp)