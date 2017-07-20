# -*- coding: utf8 -*-
from django.conf.urls import url
from apps.account.views import (
    register,
    send_sms,
    login,
    logout,
    resetpassword,
    InfoView,
    upload
)
from apps.account.tests import (
    create_user,
    distrib_position,
    create_commission_1,
    create_commission_0,
    create_deal,
    insert_position
)


urlpatterns = [
    url(r'^register/$', register, name='register'),  # 注册
    url(r'^sendsms/$', send_sms, name='send_sms'),  # 发送验证码短信
    url(r'^login/$', login, name='login'),  # 登录
    url(r'^logout/$', logout, name='logout'),  # 退出登录
    url(r'^resetpw/$', resetpassword, name='resetpassword'),  # 修改密码
    url(r'^info/$', InfoView.as_view(), name='info'),  # 用户个人信息
    url(r'^upload/$', upload, name='upload'),  # 上传媒体信息
    # 以下为测试接口
    url(r'^createuser/$', create_user, name='create_user'),
    url(r'^distribposition/$', distrib_position, name='distrib_position'),
    url(r'^createcommission1/$', create_commission_1,
        name='create_commission_1'),
    url(r'^createcommission0/$', create_commission_0,
        name='create_commission_0'),
    url(r'^createdeal/$', create_deal, name='create_deal'),
    url(r'insertposition', insert_position, name='insert_position')
]
