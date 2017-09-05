# -*- coding：utf8 -*-
from django.conf.urls import url
from apps.commentary.views import (
    save_blog,
    save_comment,
    save_like,
    get_blog_detail,
    get_comments
)


urlpatterns = [
    url(r'^saveblog/$', save_blog, name='save_blog'),  # 存储短评／长文信息
    url(r'^savecomment/$', save_comment, name='save_comment'),  # 存储评论信息
    url(r'^savelike/$', save_like, name='save_like'),  # 存储获赞信息
    url(r'^getblogdetail/$', get_blog_detail, name='get_blog_detail'),  # 获取短评／长文的详细内容
    url(r'^getcomments/$', get_comments, name='get_comments')  # 获取短评／长文的评论
]