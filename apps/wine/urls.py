# -*- coding: utf8 -*-
from django.conf.urls import url
from apps.wine.views import (
    get_optional,
    set_optional,
    del_optional,
    search_wine,
    sort_optional,
    sell,
    buy,
    detail
)
from apps.wine.wine_view_lib import (
    forchart,
    k_line,
    quotes
)
from apps.wine.tests import insert_wine


urlpatterns = [
    url(r'^getopt/$', get_optional, name='get_optional'),  # 获取自选列表
    url(r'^setopt/$', set_optional, name='set_optional'),  # 添加自选
    url(r'^delopt/$', del_optional, name='del_optional'),  # 删除自选
    url(r'^search/$', search_wine, name='search_wine'),  # 搜索
    url(r'^sortopt/$', sort_optional, name='sort_optional'),  # 对自选列表排序
    url(r'^sell/$', sell, name='sell'),  # 卖出
    url(r'^buy/$', buy, name='buy'),  # 买入
    url(r'^detail/$', detail, name='detail'),  # 详情数据
    url(r'^test/$', insert_wine, name='test_insert_wine'),  # 测试用
    url(r'^forchart/$', forchart, name='forchart'),  # 分时数据
    url(r'^kline/$', k_line, name='k_line'),  # K线图数据
    url(r'^quotes/$', quotes, name='quotes')  # 行情数据
]
