# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

from mysite.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DJANGO_ROOT = '/usr/local/lib/python2.7/site-packages/django/'

ALLOWED_HOSTS = ['*']


COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kwasispam@gmail.com'
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