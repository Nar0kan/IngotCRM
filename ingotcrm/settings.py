from pathlib import Path
import environ
import os

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

READ_DOT_ENV_FILE = env.bool('READ_DOT_ENV_FILE', default=False) # False in production

if READ_DOT_ENV_FILE:
    environ.Env.read_env(os.path.join(BASE_DIR / "ingotcrm", '.env'))

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app']

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'leads',
    'agents',
    'ecom.apps.EcomConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_tailwind',
    'future',
    'django_filters',
    'paypal.standard.ipn',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',               # whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ingotcrm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ingotcrm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = "static_root"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'leads.User'

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_REDIRECT_URL = "/leads"
LOGIN_URL = "/login"
LOGOUT_REDIRECT_URL = "/"

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# PAYPAL SETTINGS

# For 3rd apps to open own windows (paypal window for donations)
SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'

# For django-paypal
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = env('PAYPAL_RECEIVER_EMAIL')
PAYPAL_RECEIVER_ID = env('PAYPAL_RECEIVER_ID')

# AWS Bucket
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_SIGNATURE_NAME = 's3v4',
# AWS_S3_REGION_NAME = 'eu-north-1'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL =  None
# AWS_S3_VERITY = True
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STORAGES = {"default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"}}
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# s3 static settings
# STATIC_LOCATION = 'static'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
# STATICFILES_STORAGE = 'hello_django.storage_backends.StaticStorage'

# s3 public media settings
# PUBLIC_MEDIA_LOCATION = 'media'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
# DEFAULT_FILE_STORAGE = 'ingotcrm.storage_backends.PublicMediaStorage'

# s3 private media settings
# PRIVATE_MEDIA_LOCATION = 'private'
# PRIVATE_FILE_STORAGE = 'hello_django.storage_backends.PrivateMediaStorage'

# For debug purposes
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'mysite.log',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers':['file'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#         'MYAPP': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#         },
#     }
# }