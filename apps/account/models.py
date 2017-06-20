# encoding: utf8
from django.db import models
from django.contrib.auth.models import User


class Jh_User(models.Model):
    '''
    用户信息表
    '''
    userid = models.CharField(max_length=16, verbose_name='用户id', null=True)
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

    class Meta:
        db_table = 'account_jh_user'

    def __unicode__(self):
        return '{0}\[{1}\]'.format(self.phone, self.nickname)

    def get_role_name(self):
        role_map = dict([('0', '普通人员'), ('1', '管理人员')])
        return role_map[str(self.role)]
