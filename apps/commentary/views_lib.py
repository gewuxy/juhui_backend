# -*- coding: utf8 -*-
from apps.commentary.models import BlogComment, Likes


def notice_friends():
    '''
    :return: 通知朋友
    '''
    pass


def get_comments_count(blog):
    '''
    :param blog: 短评／长文
    :return: 评论数
    '''
    count = BlogComment.objects.filter(blog=blog, is_delete=False).count()
    return count


def get_likes_count(blog):
    '''
    :param blog: 短评／长文
    :return: 获赞数
    '''
    count = Likes.objects.filter(blog=blog, is_delete=False).count()
    return count


def get_comments(blog, page=1, page_num=10):
    '''
    :param blog: 短频／长文
    :param page: 页码
    :param page_num: 页长
    :return: 评论内容列表
    '''
    comments = BlogComment.objects.filter(blog=blog, is_delete=False).order_by('-create_time')
    start = (page - 1) * page_num
    end = page * page_num
    comments_json = []
    for comment in comments[start:end]:
        comments_json.append(comment.to_json())
    return comments_json
