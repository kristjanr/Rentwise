# Honor the 'X-Forwarded-Proto' header for request.is_secure()
import os

# Make the website use https only
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600

SECRET_KEY = os.environ.get('SECRET_KEY')

# Turn debug mode off for security
DEBUG = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'pinax_theme_bootstrap.context_processors.theme',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'debug': DEBUG,
        },
    },
]

# Allow running this app only on specific hostname
ALLOWED_HOSTS = ['rentwise.herokuapp.com', ]

# Whitenoise configuration, for faster static files loading
WHITENOISE_AUTOREFRESH = False
STATIC_HOST = 'https://d39cnotbzpr2wz.cloudfront.net'
STATIC_URL = STATIC_HOST + '/static/'
