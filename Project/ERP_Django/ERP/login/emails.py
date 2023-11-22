from django.core.mail import send_mail
import random
from django.conf import settings
from .models import LoginUser


def send_otp_via_email(email,user_id,password):
    subject="you account verification email"
    otp=random.randint(1000,9999)
    message=f'your otp is {otp}'
    email_from=settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    user_obj=LoginUser(user_id=user_id,password=password,otp=otp)
    user_obj.save()



import jwt
from datetime import datetime, timedelta
import os
import base64


SECRET_KEY = 'your-secret-key'

def generate_jwt_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')    