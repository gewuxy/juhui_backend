# -*- coding: utf8 -*-
from apps.wine.models import Deal, WineInfo, Position
from django.http import JsonResponse
from apps import get_response_data
import time
import datetime
import calendar


def up_ratio(code=None):
    if code:
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
    else:
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
                wine=wine, create_at__date=yesterday).order_by('-create_at')
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
    data = []
    try:
        now_date = datetime.datetime.fromtimestamp(now).date()
        wine = WineInfo.objects.get(code=wine_code)
        count = int(count)
    except Exception:
        return JsonResponse(get_response_data('000002'))
    if period == '5d':
        delta = 5
    elif period == '7d':
        delta = 7
    elif period == '30d':
        delta = 30
    else:
        delta = 1
    start_date = now_date - datetime.timedelta(days=delta * count)
    start_at = datetime.datetime.combine(start_date, datetime.time.min)
    end_at = datetime.datetime.combine(now_date, datetime.time.min)
    all_position = Position.objects.all()
    all_wine_coount = 0
    for position in all_position:
        all_wine_coount += position.num
    for deal in Deal.objects.filter(
            wine=wine,
            create_at__gte=start_at,
            create_at__lt=end_at).order_by('-create_at'):
        print('======price=====')
        print('{0}'.format(deal.price))
        if delta == 30:
            last_day_num = calendar.monthrange(
                deal.create_at.year, deal.create_at.month)[1]
            create_at = deal.create_at.replace(day=last_day_num)
            if create_at > end_at:
                date_str = end_at.strftime('%Y-%m-%d')
            else:
                date_str = create_at.strftime('%Y-%m-%d')
        else:
            delta_days = (end_at - deal.create_at).days
            date_str = end_at - datetime.timedelta(
                days=delta_days // delta * delta)
        if not tmp_data.get(date_str):
            tmp_data[date_str] = {}
            tmp_data[date_str]['high_price'] = deal.price
            tmp_data[date_str]['low_price'] = deal.price
            tmp_data[date_str]['deal_count'] = deal.num
            tmp_data[date_str]['date'] = date_str
            if all_wine_coount == 0:
                tmp_data[date_str]['turnover_rate'] = '0.00%'
            else:
                tmp_data[date_str]['turnover_rate'] = '{:.2f}%'.format(
                    deal.num / all_wine_coount * 100)

        else:
            tmp_data[date_str]['deal_count'] += deal.num
            if tmp_data[date_str]['high_price'] < deal.price:
                tmp_data[date_str]['high_price'] = deal.price
            if tmp_data[date_str]['low_price'] > deal.price:
                tmp_data[date_str]['low_price'] = deal.price
            tmp_data[date_str]['date'] = date_str
            if all_wine_coount == 0:
                tmp_data[date_str]['turnover_rate'] = '0.00%'
            else:
                tmp_data[date_str]['turnover_rate'] = '{:.2f}%'.format(
                    tmp_data[date_str]['deal_count'] / all_wine_coount * 100)
        data.append(tmp_data[date_str])
    return JsonResponse(get_response_data('000000', data))


def quotes(request):
    high, low = up_ratio()
    data = {'high_ratio': [], 'low_ratio': []}
    for i in range(10):
        wine = WineInfo.objects.get(code=high[i][0])
        wine_json = wine.to_json()
        wine_json['last_price'] = high[i][2]
        wine_json['ratio'] = '{:.2f}%'.format(high[i][1] * 100)
        data['high_ratio'].append(wine_json)
        wine = WineInfo.objects.get(code=low[i][0])
        wine_json = wine.to_json()
        wine_json['last_price'] = low[i][2]
        wine_json['ratio'] = '{:.2f}%'.format(low[i][1])
        data['low_ratio'].append(wine_json)
    return JsonResponse(get_response_data('000000', data))