import os

INSTALLED_APPS = [
    'octopus',
    'test_app'
]

SECRET_KEY = '1'

DEBUG = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


TEMPLATE_DIRECTORIES = (
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 'test_app/templates'))

ROOT_URLCONF = "test_app.urls"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.db',
    }
}
