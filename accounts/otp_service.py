import datetime
from random import randint
import re

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class OTP:
    otp_expiry_minutes = 1

    def generate_otp(self, data):
        otp = randint(1000, 9999)
        if re.match(r'[^@]+@[^@]+\.[^@]+', data):
            self.send_otp_with_email(otp, data)
        elif re.match(r'\d{10}', data):
            self.send_otp_with_phone(otp, data)
        else:
            return False

        cache.set(data, (otp, datetime.datetime.now()),
                  self.otp_expiry_minutes * 60)
        return otp

    def verify_otp(self, otp, data):
        stored_otp_info = cache.get(data)
        if stored_otp_info is None:
            return False
        stored_otp, timestamp = stored_otp_info

        if stored_otp == int(otp):
            if datetime.datetime.now() - timestamp > datetime.timedelta(minutes=self.otp_expiry_minutes):
                self.clear_otp(data)
                return False
            else:
                self.clear_otp(data)
                return True
        else:
            return False

    def clear_otp(self, data):
        cache.delete(data)

    def send_otp_with_email(self, otp, email):
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('accounts/active_email.html', {
            'user': email,
            'code': otp,
        })
        to_email = email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    def send_otp_with_phone(self, otp, phone):
        print(otp) # this is just for test
