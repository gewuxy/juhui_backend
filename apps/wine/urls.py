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
    detail,
    today_deal,
    history_deal,
    today_commission,
    history_commission,
    cancel_commission,
    detail_cancel_comm,
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
    url(r'^cancelcommission/$', cancel_commission, name='cancel_commission'),  # 撤销委托单
    url(r'^detail/$', detail, name='detail'),  # 详情数据
    url(r'^test/$', insert_wine, name='test_insert_wine'),  # 测试用
    url(r'^forchart/$', forchart, name='forchart'),  # 分时数据
    url(r'^kline/$', k_line, name='k_line'),  # K线图数据
    url(r'^quotes/$', quotes, name='quotes'),  # 行情数据
    url(r'^todaydeal/$', today_deal, name='today_deal'),  # 当日成交
    url(r'^historydeal', history_deal, name='history_deal'),  # 历史成交
    url(r'todaycommission', today_commission, name='today_commission'),  # 当日委托
    url(r'historycommission', history_commission, name='history_commission'), # 历史委托
    url(r'detailcancelcomm', detail_cancel_comm, name='detail_cancel_comm'),  # 详情页撤单
]
