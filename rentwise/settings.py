"""
Django settings for rentwise project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import uuid

import dj_database_url
from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "97wweejib1af0_&9glcl#$vteh6q%!6%_vcrc^wt_%(ed^6wx*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'social_django',
    'app',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'djplaces',
    's3direct',
    'django_tables2',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'rentwise.urls'

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

WSGI_APPLICATION = 'rentwise.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {'default': db_from_env}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SITE_ID = '1'

SOCIAL_AUTH_FACEBOOK_KEY = '191007684701647'
SOCIAL_AUTH_FACEBOOK_SECRET = '4ff6ba0463f68543fc8743094f8ffc7a'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile', ]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email, picture'}

LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')

# These URLs are used on different steps of the auth process, some for successful results and others for
# error situations.

# SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy('home')
# Used to redirect the user once the auth process ended successfully. The value of ?next=/foo is used if it was present

SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
# URL where the user will be redirected in case of an error

# SOCIAL_AUTH_LOGIN_URL = '/login-url/'
# Is used as a fallback for LOGIN_ERROR_URL

SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'
# The user will be redirected to this URL when a social account is disconnected

# SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'
# Inactive users can be redirected to this URL when trying to authenticate.

SOCIAL_AUTH_USER_MODEL = 'auth.User'

SOCIAL_AUTH_SESSION_EXPIRATION = True

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'app.varia.save_profile',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

MIGRATION_MODULES = {
    'sites': 'rentwise.migrations.sites',
}

MAPS_API_KEY = 'AIzaSyCn_Tc8zAWwsTmDgYmZLfuSGX2VyGN0OEo'

# AWS keys
AWS_SECRET_ACCESS_KEY = '4cr2LSorfsSRznLKp3gVu9A9AdNg53oVd/elHJGA'
AWS_ACCESS_KEY_ID = 'AKIAJQIO7VQFYZF7MKSA'
AWS_STORAGE_BUCKET_NAME = 'ybuy'

# The region of your bucket, more info:
# http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
S3DIRECT_REGION = 'eu-west-2'


# Destinations, with the following keys:
#
# key [required] Where to upload the file to, can be either:
#     1. '/' = Upload to root with the original filename.
#     2. 'some/path' = Upload to some/path with the original filename.
#     3. functionName = Pass a function and create your own path/filename.
# auth [optional] An ACL function to whether the current Django user can perform this action.
# allowed [optional] List of allowed MIME types.
# acl [optional] Give the object another ACL rather than 'public-read'.
# cache_control [optional] Cache control headers, eg 'max-age=2592000'.
# content_disposition [optional] Useful for sending files as attachments.
# bucket [optional] Specify a different bucket for this particular object.
# server_side_encryption [optional] Encryption headers for buckets that require it.


def path_filename(filename):
    return 'uploads/images/%s.%s' % (uuid.uuid1(), filename.split('.')[1])


S3DIRECT_DESTINATIONS = {
    'images_destination': {
        # REQUIRED
        'key': path_filename,

        # OPTIONAL
        'auth': lambda u: u.is_authenticated,  # Default allow anybody to upload
        'allowed': ['image/jpeg', 'image/png', 'image/gif', ],
        'cache_control': 'max-age=2592000',  # Default no cache-control
        'content_disposition': 'attachment',  # Default no content disposition
        'content_length_range': (5000, 20000000),  # Default allow any size
    }
}
S3DIRECT_URL_STRUCTURE = 'https://{1}.{0}'

ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'YBuy <kristjan.r@gmail.com>'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
