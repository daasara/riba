DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'riba',
        'USER': 'root',
        'PASSWORD': 'allagr2nd',
    },
    'tinla_slave': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'riba',
        'USER': 'root',
        'PASSWORD': 'allagr2nd',
    }

}
ROOT_URLCONF = 'urls'
#LOGGING_CONF = '/home/saumil/tinla/logging.conf.debug'
#MEDIA_URL = '/media/'
TABLE_PREFIX = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS' : False}
UPLOAD_ROOT = '/home/saumil/tinla/media/futurebazaar/u'
INTERNAL_IPS = ('127.0.0.1', 'localhost')

SOUTH_DATABASE_ADAPTERS = {
       'default': 'south.db.mysql',
        }
