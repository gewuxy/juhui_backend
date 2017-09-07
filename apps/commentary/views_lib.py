# -*- coding: utf8 -*-
from apps.commentary.models import BlogComment, Likes, Blog
import redis
import json

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=1)


def notice_friends(msg_type, content, create_time, to_id='', from_id='', from_name='', from_img=''):
    '''
    :param msg_type: 消息类型(新短评new_commentary，评论comment，点赞like)
    :param content: 消息内容
    :param create_time: 消息发生时间
    :param to_id: 消息接受用户的id
    :param from_id: 消息来源用户的id
    :param from_name: 消息来源用户的昵称
    :param from_img: 消息来源用户的头像
    :return: 广播短评页面的消息提醒
    '''
    if from_name is None:
        from_name = ''
    REDIS_CLIENT.publish('commentary', json.dumps({
        'msg_type': msg_type,
        'content': content,
        'create_time': create_time,
        'to_id': to_id,
        'from_id': from_id,
        'from_name': from_name,
        'from_img': from_img
    }))
    return True


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


def get_blog_list(page=1, page_num=10):
    '''
    :param page: 页码
    :param page_num: 页长
    :return:  短评／长文列表
    '''
    blogs = Blog.objects.filter(is_delete=False).order_by('-create_time')
    start = (page - 1) * page_num
    end = page * page_num
    blog_list = []
    for blog in blogs[start:end]:
        tmp_blog = blog.to_json()
        tmp_blog['comments_count'] = get_comments_count(blog)
        tmp_blog['likes_count'] = get_likes_count(blog)
        blog_list.append(tmp_blog)
    return blog_list
