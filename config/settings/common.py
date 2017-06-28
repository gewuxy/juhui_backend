# encoding: utf8
# @Time    : 2017-06-13 17:00
# @Author  : xiaoqiu
# @Site    : 公共的环境配置 修改请慎重

from __future__ import absolute_import, unicode_literals
import environ

ROOT_DIR = environ.Path(__file__) - 3
# (juhui/config/settings/common.py - 3 = cpic-easySearch/)
APPS_DIR = ROOT_DIR.path('apps')

# 从 .env 文件中读取相关的环境配置信息
env = environ.Env()
env.read_env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.sites',
    # 'django.contrib.messages',
    'oauth2_provider',
    'rest_framework',
    # 'rest_framework.authtoken'
)

THIRD_PARTY_APPS = (
    'django_crontab',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'apps.account',
    'apps.wine',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
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
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'apps.Middleware'
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


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 阿里大于
ALIDAYU_KEY = '24470660'
ALIDAYU_SECRET = '7b0967b1d2f3b7159808170721d137ff'
CODE_EXPIRE = 90

# 微信
APP_ID = 'wx53502d888764b329'
APP_SECRET = '018d5c10649a2eae7356013549f9fab1'
