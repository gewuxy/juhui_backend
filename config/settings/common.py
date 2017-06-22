# encoding: utf8
# @Time    : 2017-06-13 17:00
# @Author  : xiaoqiu
# @Site    : 公共的环境配置 修改请慎重

from __future__ import absolute_import, unicode_literals
import environ

ROOT_DIR = environ.Path(__file__) - 3  # (juhui/config/settings/common.py - 3 = cpic-easySearch/)
APPS_DIR = ROOT_DIR.path('apps')

# 从 .env 文件中读取相关的环境配置信息
env = environ.Env()
env.read_env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'rest_framework',
    'rest_framework.authtoken'
)

THIRD_PARTY_APPS = (
    'django_crontab',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'apps.account',  # 新增app
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}
'''
AUTHENTICATION_BACKENDS = (
    'apps.account.TokenBackend.TokenBackend',
    # 'django.contrib.auth.backends.ModelBackend',
)
'''
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.Middleware'
)
DEBUG = env.bool('DJANGO_DEBUG', True)
# ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', default='[*]')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'juhui',
        'USER': 'juhui',
        'PASSWORD': 'juhui6668',
        'HOST': 'localhost',
        'PORT': '3306',
        'CHARSET': 'utf8',
    },
}

# mongodb set
# MONGO_DATABASES = {
#     'HOST': '127.0.0.1',
#     'PORT': 27017,
#     'DEFAULT_DB': 'juhui',
# }
REDIS = {
    'HOST': 'localhost',
    'PORT': 6379
}

DATABASES['default']['ATOMIC_REQUESTS'] = True
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# 阿里大于
ALIDAYU_KEY = '24470660'
ALIDAYU_SECRET = '7b0967b1d2f3b7159808170721d137ff'
CODE_EXPIRE = 90
