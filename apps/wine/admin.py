from django.contrib import admin
from apps.wine.models import Position, WineInfo, Commission, Deal

class PositionAdmin(admin.ModelAdmin):
    list_display = ['wine_info_name', 'owner', 'price', 'num']
    search_fields = ['wine__name', 'user__nickname', 'user__mobile']

    def wine_info_name(self, obj):
        return u'%s' % obj.wine.name

    def owner(self, obj):
        return '{0}[{1}]'.format(obj.user.nickname, obj.user.mobile)

class CommissionAdmin(admin.ModelAdmin):
    list_display = [
        'wine_info_name', 'commission_direction', 'price', 'num', 'owner',
        'commission_status', 'create_at', 'update_at'
    ]
    search_fields = ['wine__name', 'user__nickname', 'user__mobile', ]

    def wine_info_name(self, obj):
        return u'%s' % obj.wine.name

    def commission_direction(self, obj):
        if obj.trade_direction == 0:
            return u'买入'
        else:
            return u'卖出'

    def owner(self, obj):
        return '{0}[{1}]'.format(obj.user.nickname, obj.user.mobile)

    def commission_status(self, obj):
        if obj.status == 0:
            return u'可撤单'
        elif obj.status == 1:
            return u'已撤单'
        elif obj.status == 2:
            return u'已成交'
        else:
            return u'已取消'

class DealAdmin(admin.ModelAdmin):
    list_display = ['wine_info_name', 'buyer_name', 'seller_name', 'price', 'num', 'create_at']
    search_fields = ['wine__name', 'buyer__nickname', 'buyer__mobile', 'seller__nickname', 'seller__mobile']

    def wine_info_name(self, obj):
        return u'%s' % obj.wine.name

    def buyer_name(self, obj):
        if obj.buyer.nickname:
            return u'%s' % obj.buyer.nickname
        else:
            return u'%s' % obj.buyer.mobile

    def seller_name(self, obj):
        if obj.seller.nickname:
            return u'%s' % obj.seller.nickname
        else:
            return u'%s' % obj.seller.mobile

admin.site.register(Position, PositionAdmin)
admin.site.register(WineInfo)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Deal, DealAdmin)

