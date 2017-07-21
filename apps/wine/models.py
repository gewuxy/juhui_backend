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


"""
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
    commissioned_at = models.DateTimeField(
        auto_now_add=True, verbose_name='委托时间')
    trade_at = models.DateTimeField(auto_now=True, verbose_name='交易时间')
"""


class Commission(models.Model):
    '''
    委托表
    '''
    wine = models.ForeignKey(WineInfo)
    trade_direction = models.IntegerField(
        verbose_name='买卖方向', default=1, choices=[(0, '买入'), (1, '卖出')])
    price = models.FloatField(verbose_name='委托价')
    num = models.IntegerField(verbose_name='委托数量', default=1)
    user = models.ForeignKey(Jh_User)
    status = models.IntegerField(verbose_name='状态', default=0, choices=[
        (0, '可撤'), (1, '已撤单'), (2, '已成交'), (3, '取消')])
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='委托时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def to_json(self):
        d = {}
        d['id'] = self.id
        d['wine_code'] = self.wine.code
        d['wine_name'] = self.wine.name
        d['trade_direction'] = '卖出' if self.trade_direction == 1 else '买入'
        d['user_id'] = self.user.id
        d['user_name'] = self.user.nickname
        d['status'] = self.status
        d['price'] = self.price
        d['num'] = self.num
        d['create_at'] = self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        d['update_at'] = self.update_at.strftime('%Y-%m-%d %H:%M:%S')
        return d


class Deal(models.Model):
    '''
    成交表
    '''
    wine = models.ForeignKey(WineInfo)
    buyer = models.ForeignKey(Jh_User, related_name='buyer')
    seller = models.ForeignKey(Jh_User, related_name='seller')
    price = models.FloatField(verbose_name='成交价')
    num = models.IntegerField(verbose_name='成交数量', default=1)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='成交时间')

    def to_json(self):
        d = {}
        d['wine_code'] = self.wine.code
        d['wine_name'] = self.wine.name
        d['buyer_id'] = self.buyer.id
        d['buyer_name'] = self.buyer.nickname
        d['seller_id'] = self.seller.id
        d['seller_name'] = self.seller.nickname
        d['price'] = self.price
        d['num'] = self.num
        d['create_at'] = self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        return d


class Position(models.Model):
    '''
    持仓表
    '''
    wine = models.ForeignKey(WineInfo)
    user = models.ForeignKey(Jh_User)
    price = models.FloatField(verbose_name='开仓价')
    num = models.IntegerField(verbose_name='持仓量', default=1)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
