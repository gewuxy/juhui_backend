# -*- coding: UTF-8 -*-
from django.conf.urls import include, url
from apps import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^api/account/', include('apps.account.urls', namespace='account')),
    url(r'^api/wine/', include('apps.wine.urls', namespace='wine'))
]
