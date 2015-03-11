import os

INSTALLED_APPS = [
    'octopus',
    'test_app'
]

SECRET_KEY = '1'

DEBUG = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

TEMPLATE_CONTEXT_PROCESSORS = (
  # ...
  'django.core.context_processors.request',
  # ...
)

APPEND_SLASHES = True

TEMPLATE_DIRECTORIES = (
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 'test_app/templates'))

MIDDLEWARE_CLASSES = ('django.middleware.csrf.CsrfViewMiddleware', )

ROOT_URLCONF = "test_app.urls"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.db',
    }
}
