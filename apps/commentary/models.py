# -*- coding: utf8 -*-
from django.db import models
from apps.account.models import Jh_User


class Blog(models.Model):
    '''
    短评/长文数据表
    '''
    author = models.ForeignKey(Jh_User)
    title = models.CharField(default='', verbose_name='标题', max_length=64)
    abstract = models.TextField(default='', verbose_name='摘要')
    first_img = models.CharField(default='', verbose_name='首图', max_length=255)
    content = models.TextField(default='', verbose_name='正文')
    area = models.CharField(default='', verbose_name='地点', max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    parent_blog_id = models.IntegerField(default=0, verbose_name='转发源短评id')

    class Meta:
        db_table = 'commentary_blog'

    def __str__(self):
        return '{0}--{1}--{2}'.format(self.title, self.author.nickname, self.create_time)

    def to_json(self):
        d = {}
        d['blog_id'] = self.id
        d['author_id'] = self.author.id
        d['author_name'] = self.author.nickname
        d['author_img'] = self.author.img_url
        d['title'] = self.title
        d['content'] = self.content
        d['abstract'] = self.abstract
        d['first_img'] = self.first_img
        d['area'] = self.area
        d['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        d['is_delete'] = self.is_delete
        d['parent_blog_id'] = self.parent_blog_id
        return d


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

    def to_json(self):
        d = {}
        D['comment_id'] = self.id
        d['blog_id'] = self.blog.id
        d['blog_title'] = self.blog.title
        d['author_name'] = self.author.nickname
        d['author_img'] = self.author.img_url
        d['content'] = self.content
        d['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        d['is_delete'] = self.is_delete
        return d


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


class CommentLikes(models.Model):
    '''
    评论点赞数据表
    '''
    comment = models.ForeignKey(BlogComment)
    author = models.ForeignKey(Jh_User)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否取消点赞')

    class Meta:
        db_table = 'commentary_comment_likes'

    def __str__(self):
        return '{0}--{1}'.format(self.author.nickname, self.create_time)