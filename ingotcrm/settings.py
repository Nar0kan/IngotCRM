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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
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


# SMTP Mail configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Console backend
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# AWS Bucket
USE_S3 = os.getenv('USE_S3')

if USE_S3 == 'TRUE':
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'ingotcrm.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

AUTH_USER_MODEL = 'leads.User'

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

# For debug purposes
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'formatters': {
#        'verbose': {
#            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#            'datefmt' : "%d/%b/%Y %H:%M:%S"
#        },
#        'simple': {
#            'format': '%(levelname)s %(message)s'
#        },
#    },
#    'handlers': {
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'filename': 'mysite.log',
#            'formatter': 'verbose'
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers':['file'],
#            'propagate': True,
#            'level':'DEBUG',
#        },
#        'MYAPP': {
#            'handlers': ['file'],
#            'level': 'DEBUG',
#        },
#    }
#}
