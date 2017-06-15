#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from apps import login, register, change_pw, index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/?$', login, name='login'),
    url(r'^register/?$', register, name='register'),
    url(r'^changepw/?$', change_pw, name='changepw'),
]

