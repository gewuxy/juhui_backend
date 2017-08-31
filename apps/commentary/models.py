# -*- coding: utf8 -*-
from django.db import models
from apps.account.models import Jh_User


class Blog(models.Model):
    '''
    短评/长文数据表
    '''
    author = models.ForeignKey(Jh_User)
    title = models.CharField(default='', verbose_name='标题', max_length=64)
    abstract = models.CharField(default='', verbose_name='摘要', max_length=255)
    img = models.CharField(default='', verbose_name='图片', max_length=255)
    content = models.TextField(default='', verbose_name='正文')
    area = models.CharField(default='', verbose_name='地点', max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'commentary_blog'

    def __str__(self):
        return '{0}--{1}--{2}'.format(self.title, self.author.nickname, self.create_time)


class BlogComment(models.Model):
    '''
    短评/长文的评论数据表
    '''
    blog = models.ForeignKey(Blog)
    author = models.ForeignKey(Jh_User)
    content = models.TextField(default='', verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'commentary_blog_comment'

    def __str__(self):
        return '{0}--{1}--{2}'.format(self.content[:10], self.author.nickname, self.create_time)


class Likes(models.Model):
    '''
    短评/长文的点赞数据表
    '''
    blog = models.ForeignKey(Blog)
    author = models.ForeignKey(Jh_User)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否取消点赞')

    class Meta:
        db_table = 'commentary_blog_likes'

    def __str__(self):
        return '{0}--{1}'.format(self.author.nickname, self.create_time)
