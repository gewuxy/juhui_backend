# -*- coding: utf8 -*-
from django.conf.urls import url
from apps.account.views import (
    register,
    send_sms,
    login,
    logout,
    resetpassword,
    InfoView
)
from apps.account.tests import (
    create_user,
    distrib_position,
    create_commission_1,
    create_commission_0,
    create_deal
)


urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^sendsms/$', send_sms, name='send_sms'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^resetpw/$', resetpassword, name='resetpassword'),
    url(r'^info/$', InfoView.as_view(), name='info'),
    url(r'^createuser/$', create_user, name='create_user'),
    url(r'^distribposition/$', distrib_position, name='distrib_position'),
    url(r'^createcommission1/$', create_commission_1,
        name='create_commission_1'),
    url(r'^createcommission0/$', create_commission_0,
        name='create_commission_0'),
    url(r'^createdeal/$', create_deal, name='create_deal')
]
