# -*- coding：utf8 -*-
from django.conf.urls import url
from apps.commentary.views import (
    save_blog,
    save_comment,
    save_like,
    get_blog_detail,
    get_comments,
    delete_blog,
    delete_comment,
    delete_like,
    get_blog_list,
    save_comment_like,
    delete_comment_like,
    get_notices,
    get_wine_blogs,
)


urlpatterns = [
    url(r'^saveblog/$', save_blog, name='save_blog'),  # 存储短评／长文信息
    url(r'^savecomment/$', save_comment, name='save_comment'),  # 存储评论信息
    url(r'^savelike/$', save_like, name='save_like'),  # 存储短评获赞信息
    url(r'^getblogdetail/$', get_blog_detail, name='get_blog_detail'),  # 获取短评／长文的详细内容
    url(r'^getcomments/$', get_comments, name='get_comments'),  # 获取短评／长文的评论
    url(r'^deleteblog/$', delete_blog, name='delete_blog'),  # 删除短评／长文
    url(r'^deletecomment/$', delete_comment, name='delete_comment'),  # 删除短评／长文的评论
    url(r'^deletelike/$', delete_like, name='delete_like'),  # 取消短评／长文的赞
    url(r'^getbloglist/$', get_blog_list, name='get_blog_list'),  # 获取短评／长文列表
    url(r'^savecommentlike/$', save_comment_like, name='save_comment_like'),  # 存储评论获赞信息
    url(r'^deletecommentlike/$', delete_comment_like, name='delete_comment_like'),  # 取消评论的赞
    url(r'^getnotices/$', get_notices, name='get_notices'),  # 获取提醒消息列表
    url(r'^getwineblogs/$', get_wine_blogs, name='get_wine_blogs'),  # 获取葡萄酒相关短评列表

]