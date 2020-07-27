from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import connection as cn
from datetime import timedelta


def check_if_otp_generated_for_more_than_limit_for_user(phone_no):
    try:
        cursor = cn.cursor()
        cursor.execute('select count(*) from otp_history')
        count = cursor.fetchall()
        count = count[0][0]
        if count and count > 1:
            blocked_time = timezone.now()+timedelta(days=1)
            print(blocked_time)
            cursor.execute('delete from otp_history where phone_no = %s',(phone_no,))
            cursor.execute('insert into otp_history(phone_no, otp, datetime) values(%s,%s,%s)', (phone_no, "blockd", blocked_time))
            raise ValidationError("You have tried too many times. Please come back again tommorow")
    finally:
        cursor.close()