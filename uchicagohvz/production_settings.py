from local_settings import *

DEBUG = False

ALLOWED_HOSTS = ['hvz.gryphus.io']

ADMINS = (
    ('Administrator', 'greg+hvz@gryphus.io'),
)

try:
    from secrets import DATABASES
except:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'uchicagohvz',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

# REST framework settings
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
	)
}

# Email settings
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
CELERY_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

try:
    from secrets import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
except:
    EMAIL_HOST_USER = 'placeholder'
    EMAIL_HOST_PASSWORD = 'placeholder'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
MAIL_USE_TLS = True

# Chat settings
CHAT_SERVER_URL = '//hvz.gryphus.io/chat'
CHAT_ADMIN_URL = '//hvz.gryphus.io/admin'

try:
    from secrets import GEOPOSITION_GOOGLE_MAPS_API_KEY
except:
    GEOPOSITION_GOOGLE_MAPS_API_KEY = 'placeholder'
