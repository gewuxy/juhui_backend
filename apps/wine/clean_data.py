# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps import get_response_data
from apps.wine.models import Commission

import requests
import datetime


# 清理历史委托中未成交的数据
def clean_old_comm(request):
    today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    old_commissions = Commission.objects.filter(create_at__lt=today_start, status=0, )
    return 