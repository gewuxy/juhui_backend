# -*- coding: utf8 -*-
from django.db import models
from apps.account.models import Jh_User


class WineInfo(models.Model):
    '''
    红酒信息表
    '''
    code = models.CharField(max_length=16, verbose_name='交易代码')
    name = models.CharField(max_length=64, verbose_name='名称')
    winery = models.CharField(max_length=64, verbose_name='酒庄', default='')
    proposed_price = models.FloatField(verbose_name='参考价格')
    is_delete = models.BooleanField(default=False, verbose_name='是否无效酒')

    class Meta:
        db_table = 'wine_info'

    def __unicode__(self):
        return '{0}\({1}\)'.format(self.name, self.code)

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        return d


class WineTradeOrder(models.Model):
    '''
    红酒交易订单
    '''
    wine = models.ForeignKey(WineInfo)
    buyer = models.ForeignKey(Jh_User, related_name='buyer')
    seller = models.ForeignKey(Jh_User, related_name='seller')
    commissioned_price = models.FloatField(verbose_name='委托价格')
    trade_price = models.FloatField(verbose_name='交易价格')
    trade_status = models.IntegerField(
        verbose_name='交易状态', default=1, choices=[(0, '交易完成'), (1, '待交易')])
    commissioned_at = models.DateTimeField(auto_now_add=True, verbose_name='委托时间')
    trade_at = models.DateTimeField(auto_now=True, verbose_name='交易时间')
