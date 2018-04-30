from local_settings import *

DEBUG = False 

ALLOWED_HOSTS = ['www.sttrbboy.us']

ADMINS = (
    ('Administrator', 'admin@sttrbboy.us'),
)
SERVER_EMAIL = 'noreply@sttrbboy.us'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sttrbboy',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}