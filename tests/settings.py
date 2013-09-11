import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tests.db',
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'supportform',
    'tests',
)

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

SITE_ID = 1

SECRET_KEY = 'acb123'
