# -*- coding: utf8 -*-
from django.conf.urls import url
from apps.account.views import (
    register,
    # login,
    # logout,
    # resetpassword
)


urlpatterns = [
    url(r'^register/$', register, name='register'),
    # url(r'^login/$',  login, name='login'),
    # url(r'^logout/$', logout, name='logout'),
    # url(r'^resetpw/$', resetpassword, name='resetpassword'),
]