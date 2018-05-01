from local_settings import *

DEBUG = False 

ALLOWED_HOSTS = ['www.sttr-bboy.us']
CSRF_TRUSTED_ORIGINS = ['.sttr-bboy.us']

ADMINS = (
    ('Administrator', 'admin@sttr-bboy.us'),
)
SERVER_EMAIL = 'noreply@sttr-bboy.us'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sttrbboy_prod',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
