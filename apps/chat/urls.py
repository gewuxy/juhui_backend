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


urlpatterns = [
    url(r'^comment/$', get_comment, name='get_comment'),
    url(r'^createcomment/$', create_comment, name='create_comment'),
    url(r'upload/$', upload, name='upload'),
    url(r'save/$', save_comment, name='save_comment')
]
