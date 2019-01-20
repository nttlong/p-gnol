"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.8.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.conf.urls import url, include


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bw(lu4t*o&*ot4&gf^&74ksjz3r+ji6bxr_9$y0sacg*ks0m0w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','172.16.11.127']
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
AUTHENTICATION_BACKENDS = [
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
    'quicky.backends.HashModelBackend'
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
)



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
   'default' : {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'hrm1',
       'HOST': '127.0.0.1',
       'PORT': 3306,
       'USER': 'root',
       'PASSWORD': 'password'
   }
}



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True

USE_MULTI_TENANCY=True
# MULTI_TENANCY_DEFAULT_SCHEMA="sys"
MULTI_TENANCY_DEFAULT_SCHEMA="lv"
MULTI_TENANCY_CONFIGURATION_=dict(
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    name="hrm",
    collection="sys.customers"
)

import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.getcwd()+os.sep+ 'logs'+os.sep+'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
STATIC_URL="/static/"
import xdj
ROOT_URLCONF=xdj.load_urls()