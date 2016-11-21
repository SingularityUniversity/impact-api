# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

from mysite.settings.base import *


SECRET = ['']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DJANGO_ROOT = '/usr/local/lib/python2.7/site-packages/django/'

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'organizers',
        'USER': 'root',
        'PASSWORD': 'd15turb3d'
    }
}


COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kwasi.innovate@gmail.com'
EMAIL_HOST_PASSWORD = 'innovate'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'mysite.log')
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}