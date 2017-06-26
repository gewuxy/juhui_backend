# -*- coding: utf8 -*-
from django.conf.urls import url
from apps.wine.views import (
    get_optional,
    set_optional,
    del_optional,
    search_wine
)
from apps.wine.tests import insert_wine


urlpatterns = [
    url(r'^getopt/$', get_optional, name='get_optional'),
    url(r'^setopt/$', set_optional, name='set_optional'),
    url(r'^delopt/$', del_optional, name='del_optional'),
    url(r'^search/$', search_wine, name='search_wine'),
    url(r'^test/$', insert_wine, name='test_insert_wine')
]
