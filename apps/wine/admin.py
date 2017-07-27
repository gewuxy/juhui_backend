from django.contrib import admin
from apps.wine.models import Position, WineInfo

class PositionAdmin(admin.ModelAdmin):
    list_display = ['wine_info_name', 'user_mobile', 'price', 'num']
    # search_fields = ['wine_info_name',]

    def wine_info_name(self, obj):
        return u'%s' % obj.wine.name

    def user_mobile(self, obj):
        return u'%s' % obj.user.mobile

admin.site.register(Position, PositionAdmin)
admin.site.register(WineInfo)
