# encoding: utf8
from django.db import models
from django.contrib.auth.models import User


class Jh_User(models.Model):
    '''
    用户信息表
    '''
    union_id = models.CharField(
        max_length=128, verbose_name='用户union_id', null=True)
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=40, verbose_name='昵称', null=True)
    mobile = models.CharField(max_length=12, verbose_name='手机号码', default='')
    img_url = models.CharField(
        max_length=255, verbose_name='头像url', default='')
    email = models.CharField(max_length=64, verbose_name='邮箱', default='')
    role = models.IntegerField(
        default=0, verbose_name='用户权限', choices=[(0, '普通用户'), (1, '管理人员')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否无效用户')
    funds = models.FloatField(default=0, verbose_name='资金')
    trade_passwd = models.CharField(
        max_length=64, verbose_name='交易密码', default='')
    personal_select = models.CharField(
        max_length=500, verbose_name='自选', default='')

    class Meta:
        db_table = 'account_jh_user'

    def __str__(self):
        return '{0}[{1}]'.format(self.nickname, self.mobile)

    def get_role_name(self):
        role_map = dict([('0', '普通人员'), ('1', '管理人员')])
        return role_map[str(self.role)]

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        d['user'] = d['user'].id
        return d


    class Attention(models.Model):
        '''
        用户关注表
        '''
        user = models.ForeignKey(Jh_User)
        attention_obj_type = models.IntegerField(
            default=0, verbose_name='关注对象类型', choices=[(0, '用户'), (1, '酒')])
        attention_obj_id = models.CharField(default='', verbose_name='关注对象id', max_length=8)
        attention_obj_name = models.CharField(default='', verbose_name='关注对象名称', max_length=40)
        is_attention = models.BooleanField(default=False, verbose_name='是否关注')
        create_time = models.DateTimeField(auto_now_add=True)

        class Meta:
            db_table = 'account_attention'

        def __str__(self):
            if self.is_attention:
                pre_str = '[关注]'
            else:
                pre_str = '[不关注]'
            return '{0}--{1}--{2}'.format(pre_str, self.user.nickname, self.attention_obj_name)


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


    class BlogComment(models.Model):
        '''
        短评/长文的评论数据表
        '''
        blog = models.ForeignKey(Blog)
        author = models.ForeignKey(Jh_User)
        content = models.TextField(default='', verbose_name='评论内容')
        create_time = models.DateTimeField(auto_now_add=True)
        is_delete = models.BooleanField(default=False, verbose_name='是否删除')


    class Likes(models.Model):
        '''
        短评/长文的点赞数据表
        '''
        blog = models.ForeignKey(Blog)
        author = models.ForeignKey(Jh_User)
        create_time = models.DateTimeField(auto_now_add=True)
        is_delete = models.BooleanField(default=False, verbose_name='是否取消点赞')
