# -*- coding: utf8 -*-
from apps.wine.models import Deal, WineInfo, Position
from django.http import JsonResponse
from apps import get_response_data
import time
import datetime
import calendar
import logging
import requests
import redis
import json

_logger = logging.getLogger('wine_view_lib')
REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=1)

def up_ratio(code=None):
    if code:  # 获取该红酒的现价，涨幅
        today = datetime.datetime.now().date()
        yesterday = today - datetime.timedelta(days=1)
        wine = WineInfo.objects.get(code=code)
        t_deals = Deal.objects.filter(
            wine=wine, create_at__date=today).order_by('-create_at')
        if t_deals.count() == 0:
            return 0, '0.00%'
        last_price = t_deals[0].price
        y_deals = Deal.objects.filter(
            wine=wine, create_at__date=yesterday).order_by('-create_at')
        if y_deals.count() == 0:
            return 0, '0.00%'
        yesterday_price = y_deals[0].price
        if yesterday_price == 0:
            return 0, '0.00%'
        return last_price, '{:.2f}%'.format(
            (last_price - yesterday_price) / yesterday_price * 100)
    else:  # 获取行情数据
        high_ratio_codes = []
        low_ratio_codes = []
        today = datetime.datetime.now().date()
        yesterday = today - datetime.timedelta(days=1)
        for wine in WineInfo.objects.all():
            t_deals = Deal.objects.filter(
                wine=wine, create_at__date=today).order_by('-create_at')
            if t_deals.count() == 0:
                continue
            last_price = t_deals[0].price
            y_deals = Deal.objects.filter(
                wine=wine, create_at__lte=yesterday).order_by('-create_at')
            if y_deals.count() == 0:
                continue
            yesterday_price = y_deals[0].price
            if yesterday_price == 0:
                continue
            ratio = (last_price - yesterday_price) / yesterday_price
            if ratio > 0:
                high_ratio_codes.append((wine.code, ratio, last_price))
            elif ratio < 0:
                low_ratio_codes.append((wine.code, ratio, last_price))
        high_ratio_codes.sort(key=lambda x:x[1])
        high_ratio_codes = high_ratio_codes[:10]
        low_ratio_codes.sort(key=lambda x:x[1])
        low_ratio_codes = low_ratio_codes[:10]
        return high_ratio_codes, low_ratio_codes


def _get_quotes():
    high_ratio_codes = []
    low_ratio_codes = []
    for wine in WineInfo.objects.all():
        deals = Deal.objects.filter(wine=wine).order_by('-create_at')
        if deals.count() == 0:
            continue
        last_price = deals[0].price
        if deals.count() < 2:
            continue
        pre_price = deals[1].price
        if pre_price == 0:
            continue
        ratio = (last_price - pre_price) / pre_price
        if ratio > 0:
            high_ratio_codes.append((wine.code, ratio, last_price))
        elif ratio < 0:
            low_ratio_codes.append((wine.code, ratio, last_price))
    high_ratio_codes.sort(key=lambda x: x[1])
    high_ratio_codes = high_ratio_codes[:10]
    low_ratio_codes.sort(key=lambda x: x[1])
    low_ratio_codes = low_ratio_codes[:10]
    return high_ratio_codes, low_ratio_codes


def forchart(request):
    wine_code = request.POST.get('code')
    period = request.POST.get('period', '1d')
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
    data = {}
    if period == '5d':
        delta = 5
    else:
        delta = 1
    try:
        now = datetime.datetime.fromtimestamp(now)
        wine = WineInfo.objects.get(code=wine_code)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    start_datetime = now - datetime.timedelta(days=delta - 1)
    start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    for deal in Deal.objects.filter(
            wine=wine,
            create_at__gte=start_datetime,
            create_at__lte=now).order_by('create_at'):
        print('======price=====')
        print('{0}'.format(deal.price))
        timestamp = str(int(time.mktime(deal.create_at.timetuple())))
        if not tmp_data.get(timestamp):
            tmp_data[timestamp] = {}
            tmp_data[timestamp]['open_price'] = deal.price
            tmp_data[timestamp]['close_price'] = deal.price
            tmp_data[timestamp]['last_price'] = deal.price
            tmp_data[timestamp]['high_price'] = deal.price
            tmp_data[timestamp]['low_price'] = deal.price
            tmp_data[timestamp]['num'] = deal.num
            tmp_data[timestamp]['timestamp'] = timestamp
        else:
            tmp_data[timestamp]['num'] += deal.num
            tmp_data[timestamp]['close_price'] = deal.price
            tmp_data[timestamp]['last_price'] = deal.price
            if tmp_data[timestamp]['high_price'] < deal.price:
                tmp_data[timestamp]['high_price'] = deal.price
            if tmp_data[timestamp]['low_price'] > deal.price:
                tmp_data[timestamp]['low_price'] = deal.price
            tmp_data[timestamp]['timestamp'] = timestamp
        data[timestamp] = tmp_data[timestamp]
    data_list = list(data.values())
    data_list.sort(key=lambda x:x['timestamp'])
    return JsonResponse(get_response_data('000000', data_list))


def k_line(request):
    wine_code = request.POST.get('code')
    period = request.POST.get('period')
    now = request.POST.get('now')
    count = request.POST.get('count', 100)
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
        'date_str': {
            'high_price': '',  # 最高价
            'low_price': '',  # 最低价
            # 'up_down_num': '',  # 涨跌额
            # 'up_down_ratio': '',  # 涨跌幅
            'deal_count': '',  # 成交量
            'turnover_rate': '',  # 换手率
            'date': ''
        }
    }
    data = {}
    try:
        now = datetime.datetime.fromtimestamp(now)
        wine = WineInfo.objects.get(code=wine_code)
        count = int(count)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    try:
        if period[-1] == 'm':
            delta = int(period[:-1])
        elif period[-1] == 'd':
            delta = 60 * int(period[:-1])
    except Exception:
        delta = 1

    start_at = now - datetime.timedelta(minutes=delta * count)
    all_position = Position.objects.all()
    all_wine_coount = 0
    for position in all_position:
        all_wine_coount += position.num
    for deal in Deal.objects.filter(
            wine=wine,
            create_at__gte=start_at,
            create_at__lte=now).order_by('-create_at'):
        print('======price=====')
        print('{0}'.format(deal.price))
        timestamp = str(int(time.mktime(deal.create_at.timetuple())))
        if delta == 30 * 60:
            last_day_num = calendar.monthrange(
                deal.create_at.year, deal.create_at.month)[1]
            create_at = deal.create_at.replace(day=last_day_num)
            if create_at > now:
                # date_str = end_at.strftime('%Y-%m-%d')
                date_str = str(int(time.mktime(now.timetuple())))
            else:
                # date_str = create_at.strftime('%Y-%m-%d')
                date_str = str(int(time.mktime(create_at.timetuple())))

        else:
            delta_minutes = (now - deal.create_at).seconds // 60
            create_at = now - datetime.timedelta(
                days=delta_minutes // delta * delta)
            date_str = str(int(time.mktime(create_at.timetuple())))
        if not tmp_data.get(date_str):
            tmp_data[date_str] = {}
            tmp_data[date_str]['open_price'] = deal.price
            tmp_data[date_str]['close_price'] = deal.price
            tmp_data[date_str]['high_price'] = deal.price
            tmp_data[date_str]['low_price'] = deal.price
            tmp_data[date_str]['deal_count'] = deal.num
            tmp_data[date_str]['timestamp'] = date_str
            if all_wine_coount == 0:
                tmp_data[date_str]['turnover_rate'] = '0.00%'
            else:
                tmp_data[date_str]['turnover_rate'] = '{:.2f}%'.format(
                    deal.num / all_wine_coount * 100)

        else:
            tmp_data[date_str]['deal_count'] += deal.num
            tmp_data[date_str]['open_price'] = deal.price
            if tmp_data[date_str]['high_price'] < deal.price:
                tmp_data[date_str]['high_price'] = deal.price
            if tmp_data[date_str]['low_price'] > deal.price:
                tmp_data[date_str]['low_price'] = deal.price
            tmp_data[date_str]['timestamp'] = date_str
            if all_wine_coount == 0:
                tmp_data[date_str]['turnover_rate'] = '0.00%'
            else:
                tmp_data[date_str]['turnover_rate'] = '{:.2f}%'.format(
                    tmp_data[date_str]['deal_count'] / all_wine_coount * 100)
        data[date_str] = tmp_data[date_str]
    data_list = list(data.values())
    data_list.sort(key=lambda x: x['timestamp'])
    return JsonResponse(get_response_data('000000', data_list))


def quotes(request):
    # high, low = up_ratio()
    high, low = _get_quotes()
    data = {'high_ratio': [], 'low_ratio': []}
    for i in range(10):
        wine = WineInfo.objects.get(code=high[9 - i][0])
        wine_json = wine.to_json()
        wine_json['last_price'] = high[9 - i][2]
        wine_json['ratio'] = '{:.2f}%'.format(high[9 - i][1] * 100)
        data['high_ratio'].append(wine_json)
        wine = WineInfo.objects.get(code=low[i][0])
        wine_json = wine.to_json()
        wine_json['last_price'] = low[i][2]
        wine_json['ratio'] = '{:.2f}%'.format(low[i][1])
        data['low_ratio'].append(wine_json)
    return JsonResponse(get_response_data('000000', data))


def price_emit(code, timestamp):
    REDIS_CLIENT.publish('last_price', json.dumps({'code': code, 'time': timestamp}))
    return True


def change_price(code, price):
    try:
        wine = WineInfo.objects.get(code=code)
        wine.proposed_price = float(price)
        wine.save()
        return True
    except Exception:
        return False


def select_emit(code, operation):
    select_key = 'juhui_chat_select_' + code
    select_val = REDIS_CLIENT.get(select_key)
    if select_val:
        select_val = int(select_val)
    else:
        select_val = 0
    if operation == 'add':
        select_val += 1
    elif operation == 'delete':
        select_val -= 1
    else:
        pass
    if select_val < 0:
        select_val = 0
    popularity_key = 'juhui_chat_popularity_' + code
    popularity_val = REDIS_CLIENT.get(popularity_key)
    if popularity_val:
        popularity_val = int(popularity_val)
    else:
        popularity_val = 0
    url = 'http://39.108.142.204:8001/emit_select/'
    data = {
        'code': code,
        'is_msg': '0',
        'popularity': popularity_val,
        'select': select_val
    }
    r = requests.post(url, data=data)
    if r.content == b'000000':
        return True
    else:
        return False


def last_price_ratio(code):
    try:
        wine = WineInfo.objects.get(code=code)
    except Exception:
        return 0, '0.00%'
    deals = Deal.objects.filter(wine=wine).order_by('-create_at')
    if deals.count() == 0:
        return 0, '0.00%'
    last_price = deals[0].price
    if deals.count() < 2:
        return last_price, '0.00%'
    pre_price = deals[1].price
    if pre_price == 0:
        return last_price, '0.00%'
    return last_price, '{:.2f}%'.format(
        (last_price - pre_price) / pre_price * 100)