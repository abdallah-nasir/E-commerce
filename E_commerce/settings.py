"""
Django settings for E_commerce project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import django_heroku
import dj_database_url
from decouple import config
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=config("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS =["127.0.0.1","localhost","universal-e-commerce.herokuapp"]
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD =True
SESSION_COOKIE_PATH = '/;HttpOnly'
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True 
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_HSTS_INCLUDE_SUBDOMAINS =True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #my apps
    "shop",
    #3rd party apps
    'crispy_forms',
    'django_filters',   
    # 'google_translate',
    # 'django_celery_beat',
    # 'shopify_sync',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware"
]

ROOT_URLCONF = 'E_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'E_commerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     } 
# }    
DATABASES={
    "default":{
        "ENGINE":"django.db.backends.postgresql_psycopg2",
        "NAME":"E-commerce",
        "USER":"postgres",
        "PASSWORD":config("DB_PASSWORD"),
        "HOST":"localhost",
        "PORT":""
    }     
}
DATABASE_URL=config("DB_URL")
DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
#crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'  
# "Email Backend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'abdullahnasser6@gmail.com'
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL= False
EMAIL_PORT = '587'
#allauth 
SITE_ID=1
LOGIN_REDIRECT_URL ="shop:home"
ACCOUNT_ADAPTER="allauth.account.adapter.DefaultAccountAdapter"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL=LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL =True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_CONFIRMATION_HMAC =True
ACCOUNT_EMAIL_REQUIRED =True
ACCOUNT_EMAIL_VERIFICATION ="mandatory"   
ACCOUNT_EMAIL_SUBJECT_PREFIX ="Site"
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN =60
ACCOUNT_EMAIL_MAX_LENGTH=245
ACCOUNT_MAX_EMAIL_ADDRESSES=1
ACCOUNT_LOGIN_ATTEMPTS_LIMIT =3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT =120
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE =True
ACCOUNT_LOGIN_ON_PASSWORD_RESET =True
ACCOUNT_LOGOUT_REDIRECT_URL ="shop:home"
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =True
ACCOUNT_SESSION_REMEMBER =None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE =True
ACCOUNT_SIGNUP_REDIRECT_URL =LOGIN_REDIRECT_URL
# ACCOUNT_USERNAME_BLACKLIST 
ACCOUNT_UNIQUE_EMAIL =True
ACCOUNT_USERNAME_MIN_LENGTH =1
ACCOUNT_USERNAME_REQUIRED =True
SOCIALACCOUNT_AUTO_SIGNUP =False
SOCIALACCOUNT_EMAIL_VERIFICATION =ACCOUNT_EMAIL_VERIFICATION
SOCIALACCOUNT_QUERY_EMAIL =ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS =False
ACCOUNT_FORMS = {'login': 'shop.forms.MyCustomLoginForm'} 

      
AUTHENTICATION_BACKENDS = [
    # ............
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    #      ...
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id':config("GOOGLE_CLIENT_ID"),
            'secret':config("GOOGLE_SECRET"),
            'key': ''
        }
    },

    'facebook': {
    # For each OAuth based provider, either add a ``SocialApp``
    # (``socialaccount`` app) containing the required client
    # credentials, or list them here:
    'APP': {
        'client_id':config("FACEBOOK_CLIENT_ID"),
        'secret':config("FACEBOOK_SECRET"),
        'key': '',
       
    }
}
}
#    'github': {
#     # For each OAuth based provider, either add a ``SocialApp``
#     # (``socialaccount`` app) containing the required client
#     # credentials, or list them here:
#     'APP': {
#         'client_id':config("git_client_id"),
#         'secret': config("git_secret"),
#         'key': '',
       
#     }
# }
### BRAIN  

# stripe

STRIPE_PUBLIC_KEY=config("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY=config("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET=config("STRIPE_WEBHOOK_KEY")
#  SHOPIFY
SHOPIFY_API_KEY=config("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET=config("SHOPIFY_API_SECRET")

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

from django.utils.translation import gettext_lazy as _
LANGUAGE_CODE = 'en-us'
LANGUAGES = (            # supported languages
    ('en', _('English')),
    ('en-gb', _('English (Great Britain)')),
    ('de', _('German')),
    ('tr', _('Turkish')),
    ("ar",_("Arabic")),
)
TIME_ZONE="Atlantic/Bermuda"  
USE_I18N = True

USE_L10N = True    

USE_TZ = False 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT=  os.path.join(BASE_DIR,"static")

STATICFILES_DIRS=[
     os.path.join(BASE_DIR,"static_in_env")
] 

MEDIA_URL="/media/"

MEDIA_ROOT=  os.path.join(BASE_DIR,"media")

STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"

django_heroku.settings(locals())
#for translation
LOCALE_PATHS=(   
    os.path.join(BASE_DIR,"locale/"),
             )