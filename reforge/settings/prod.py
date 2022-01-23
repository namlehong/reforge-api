from .base import *

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '2^f+3@v7$v1f8yt0!s)3-1t$)tlp+xm17=*g))_xoi&&9m#2a&')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DJANGO_DB_NAME', 'reforge'),
        'USER': os.getenv('DJANGO_DB_NAME', 'reforge'),
        'PASSWORD': os.getenv('DJANGO_DB_PWD', 'reforge'),
        'HOST': os.getenv('DJANGO_DB_HOST', 'postgresql-headless'),
    }
}
