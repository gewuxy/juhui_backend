# -*- coding: utf8 -*-
from django.conf.urls import url
from apps.chat.views import (
    get_comment,
    upload,
    save_comment,
)
from apps.chat.tests import (
    create_comment,
)
from apps.chat.chat_view_lib import first_set_select_redis

urlpatterns = [
    url(r'^comment/$', get_comment, name='get_comment'),  # 获取聊天记录
    url(r'^createcomment/$', create_comment, name='create_comment'),  # 测试用
    url(r'upload/$', upload, name='upload'),  # 上传媒体文件
    url(r'save/$', save_comment, name='save_comment'),  # 保存聊天信息
    url(r'setselectredis', first_set_select_redis, name='first_set_select_redis')  # 初始化自选信息到redis中
]
