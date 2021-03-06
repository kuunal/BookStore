from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .otp import send_otp
from .models import LoginManager
from .send_mail import send_custom_mail
from products.models import Product
from products.services import set_cache


SUBJECT_FOR_ORDER_PLACED = "Your order has been placed"
TEMPLATE_NAME = 'login/email_for_order_placed.html'

@shared_task
def send_otp_to_user_while_login(phone_no, random_otp):
    send_otp(phone_no, random_otp)

@shared_task
def order_placed_mail_to_user(obj, total, user_id, order_id, address):
    products = Product.objects.all()
    set_cache(products)
    user_email = LoginManager.get(user_id)
    send_custom_mail(obj, TEMPLATE_NAME, SUBJECT_FOR_ORDER_PLACED, user_email, total, order_id, address)

