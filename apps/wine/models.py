# -*- coding: utf8 -*-
from django.db import models


class WineInfo(models.Model):
    '''
    红酒信息表
    '''
    code = models.CharField(max_length=16, verbose_name='交易代码')
    name = models.CharField(max_length=64, verbose_name='名称')
    winery = models.CharField(max_length=64, verbose_name='酒庄', default='')

    class Meta:
        db_table = 'wine_info'

    def __unicode__(self):
        return '{0}\({1}\)'.format(self.name, self.code)
