from django.core.mail import send_mail
from bookstore import settings
from django.template.loader import render_to_string


'''
    Mail template for user 
'''
def send_custom_mail(obj, template_name, subject=None,user_email=None, total=0, order_id=None, address=None):
    subject = subject
    html_message = render_to_string(template_name,{
        'order_data_object' : obj, 
        'total':total,
        'order_id':order_id,
        'address' : address
    })
    from_email = (settings.EMAIL_HOST_USER)
    to_list = user_email
    send_mail(subject,message=None, from_email= from_email,recipient_list= to_list, html_message = html_message)