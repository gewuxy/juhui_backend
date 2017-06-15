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
    # Admin
)

THIRD_PARTY_APPS = (
    'django_crontab',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # 'apps.xxx',  # 新增app
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'apps.sysadmin.middleware.QtsAuthenticationMiddleware',
    # 'apps.sysadmin.middleware.SysExceptionMiddleware',
    # 'apps.sysadmin.middleware.SysLogMiddleware',  # 增加log日志记录
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
