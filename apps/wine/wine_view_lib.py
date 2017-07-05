# -*- coding: utf8 -*-
from apps.wine.models import Deal, WineInfo
from django.http import JsonResponse
from apps import get_response_data
import time
import datetime


def forchart(request):
    wine_code = request.POST.get('code')
    period = request.POST.get('period', '1m')
    now = request.POST.get('now')
    if wine_code is None:
        print('code is None...')
        return JsonResponse(get_response_data('000002'))
    if now is None:
        now = int(time.time())
    elif now.isdigit():
        now = int(now)
    else:
        print('now is not digit...')
        return JsonResponse(get_response_data('000002'))
    # 返回的数据
    tmp_data = {
        'timestamp': {
            'last_price': '',
            'high_price': '',
            'low_price': '',
            'num': '',
            'timestamp': ''
        }
    }
    data = []
    if period == '1m':
        delta = 1
    elif period == '5m':
        delta = 5
    elif period == '15m':
        delta = 15
    elif period == '30m':
        delta = 30
    elif period == '60m':
        delta = 60

    try:
        now_date = datetime.datetime.fromtimestamp(now).date()
        wine = WineInfo.objects.get(code=wine_code)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    start_time = int(time.mktime(now_date.timetuple()))
    for deal in Deal.objects.filter(
            wine=wine, create_at__date=now_date).order_by('create_at'):
        print('======price=====')
        print('{0}'.format(deal.price))
        hour = deal.create_at.hour
        minute = deal.create_at.minute
        timestamp = start_time + 60 * hour + minute // delta * delta
        timestamp = str(timestamp)
        if not tmp_data.get(timestamp):
            tmp_data[timestamp] = {}
            tmp_data[timestamp]['last_price'] = deal.price
            tmp_data[timestamp]['high_price'] = deal.price
            tmp_data[timestamp]['low_price'] = deal.price
            tmp_data[timestamp]['num'] = deal.num
            tmp_data[timestamp]['timestamp'] = timestamp
        else:
            tmp_data[timestamp]['num'] += deal.num
            tmp_data[timestamp]['last_price'] = deal.price
            if tmp_data[timestamp]['high_price'] < deal.price:
                tmp_data[timestamp]['high_price'] = deal.price
            if tmp_data[timestamp]['low_price'] > deal.price:
                tmp_data[timestamp]['low_price'] = deal.price
            tmp_data[timestamp]['timestamp'] = timestamp
        data.append(tmp_data[timestamp])
    return JsonResponse(get_response_data('000000', data))
