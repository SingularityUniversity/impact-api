# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
import dj_database_url
import os
from mysite.settings.base import *
from mysite.settings.local import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DJANGO_ROOT = '/usr/local/lib/python2.7/site-packages/django/'

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DW_RDS_DB_NAME'],
        'USER': os.environ['DW_RDS_USERNAME'],
        'PASSWORD': os.environ['DW_RDS_PASSWORD'],
        'HOST': os.environ['DW_RDS_HOSTNAME'],
        'PORT': os.environ['DW_RDS_PORT'],
    }
}

COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)




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