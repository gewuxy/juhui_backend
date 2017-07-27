from django.contrib import admin
from apps.wine.models import Position, WineInfo, Commission

class PositionAdmin(admin.ModelAdmin):
    list_display = ['wine_info_name', 'user_mobile', 'price', 'num']
    # search_fields = ['wine_info_name',]

    def wine_info_name(self, obj):
        return u'%s' % obj.wine.name

    def user_mobile(self, obj):
        return u'%s' % obj.user.mobile

class CommissionAdmin(admin.ModelAdmin):
    list_display = [
        'wine_info_name', 'commission_direction', 'price', 'num', 'user_moile',
        'commission_status', 'create_at', 'update_at'
    ]


admin.site.register(Position, PositionAdmin)
admin.site.register(WineInfo)
