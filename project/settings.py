"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# في بداية الملف


from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_=e0@#_o21+)w^@vc2usfoufg0#gyy27lr5#*@z+5tcxzj4@)i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #for deploy
# DEBUG = False  # صحيح للنشر
# ولكنك تحتاج لتسجيل الأخطاء في الإنتاج:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
# DEBUG = True
# ________________

ALLOWED_HOSTS = [
    'graduation-project-*.vercel.app',
    '.vercel.app',
    'localhost',
]

X_FRAME_OPTIONS = 'DENY'  # Prevents clickjacking attacks

# Static files (CSS, JavaScript, Images)
# إعدادات الملفات الثابتة
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # مهم لـ collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # مجلد static الأساسي
]

# إذا كنت تستخدم Whitenoise (مطلوب لـ Vercel)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Database configuration
import dj_database_url





# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# For Vercel deployment
ALLOWED_HOSTS = ['.vercel.app', '.now.sh', '127.0.0.1', 'localhost']

WSGI_APPLICATION = 'api.wsgi.app'

# ________________



# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://rngna-197-35-92-181.a.free.pinggy.link',
    # أضف أي domains تانية هنا
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'bootstrap5',
    'hitcount',
    'django.contrib.humanize',
    "debug_toolbar",



    'settings',
    'accounts',
    'graduation_project',
]
#for Auth (login) by id_notional mabye
AUTHENTICATION_BACKENDS = [
    'accounts.auth_backends.NationalIDAuthenticationBackend',  # Custom backend for National ID
    'django.contrib.auth.backends.ModelBackend',  # Default fallback
]


# for trust csrf in pinngy for share server for test project 
CSRF_TRUSTED_ORIGINS = [
    'https://rnztq-197-35-43-199.a.free.pinggy.link',
    # Add other domains as needed
]

# for debug_toolbar
INTERNAL_IPS = [
    '127.0.0.1',  # Add your local IP address here
]

# for show pdf
X_FRAME_OPTIONS = "ALLOW-FROM http://127.0.0.1:8000"


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # أضف هذا

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "settings.context_processor.home",

            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# DATABASES['default'] = dj_database_url.config()



import os
import dj_database_url

# إعداد قاعدة البيانات
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:aSMpTwRMJxkxhKoWlSLMHhAdajbNtWhh@maglev.proxy.rlwy.net:10239/railway',
        conn_max_age=600,  # يحسن الأداء
    )
}
# default='postgresql://neondb_owner:npg_QG4ZWgw7ROqH@ep-dawn-poetry-a5ibwxba-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require',

# لتعطيل source maps في الإنتاج
if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'



# __________________________
# Static files config for Vercel
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # Database config
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.config(
#         default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }

# # Required for Vercel
# ALLOWED_HOSTS = [
#     '.vercel.app', 
#     '.now.sh',
#     'localhost',
#     '127.0.0.1'
# ]
# __________________________



# DATABASES = {
#     'default': {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("DB_NAME"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#         "HOST": os.environ.get('DB_HOST'),
#         "PORT": os.getenv("DB_PORT"),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "staticfiles_build" / "static"

# STATIC_ROOT = "static_root"
# MEDIA_URL = '/media/'
# MEDIA_ROOT = "media_root"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LOGIN_URL = '/accounts/login/'
# settings.py
LOGIN_REDIRECT_URL = '/'  # أو صفحة معينة
LOGOUT_REDIRECT_URL = '/'  # أو صفحة معينة



# chaching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}





# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Replace with your Gmail email address
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True



