import os

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages','django.contrib.sessions',
    'django.contrib.admin',
    'octopus',
    'test_app',
    'django.contrib.sites'
]

SECRET_KEY = '1'

DEBUG = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.request',
)

APPEND_SLASHES = True

root_dir = os.path.dirname(os.path.realpath(__file__))

STATIC_ROOT = os.path.join(root_dir, 'static')
# STATICFILES_DIRS = [STATIC_ROOT]
print(STATIC_ROOT)
TEMPLATE_DIRECTORIES = (os.path.join(root_dir, 'test_app/templates'))

MIDDLEWARE_CLASSES = ('django.middleware.csrf.CsrfViewMiddleware', )
#MIDDLEWARE_CLASSES = ('django.middleware.csrf.CsrfViewMiddleware', )

ROOT_URLCONF = "test_app.urls"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.db',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRECTORIES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]