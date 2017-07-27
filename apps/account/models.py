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
