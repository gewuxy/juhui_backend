# -*- coding: utf8 -*-
from django.conf.urls import url
from apps.news.views import (
    insert_news,
    get_news
)


urlpatterns = [
    url(r'^insert/$', insert_news, name='insert_news'),  # 保存资讯信息
    url(r'^getnews/$', get_news, name='get_news'),  # 获取资讯
]
