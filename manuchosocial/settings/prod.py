import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+w!wucr14o*vq%e9jitfsdlfr4^q*5=ng*p4e0-sa$2u$&nio0'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ["localhost", "*"]

#Email backend settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'password'