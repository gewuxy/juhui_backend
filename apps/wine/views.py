# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps.account.models import Jh_User
from apps.wine.models import WineInfo
from apps.wine.models import Commission, Deal, Position
from apps import get_response_data
import logging

_logger = logging.getLogger('wineinfo')
OPTINOAL_PAGE = 1  # 自选列表默认页码
OPTINOAL_PAGE_NUM = 10  # 自选列表默认页长


def set_optional(request):
    wine_code = request.POST.get('code')
    if not wine_code:
        res = get_response_data('000002')
        return JsonResponse(res)
    jh_user = Jh_User.objects.get(user=request.user)
    personal_select = jh_user.personal_select
    personal_select_list = personal_select.split(';')
    # personal_select_list = list(set(personal_select_list))
    if wine_code in personal_select_list:
        res = get_response_data('100001')
        return JsonResponse(res)
    if personal_select:
        personal_select += ';' + wine_code
    else:
        personal_select = wine_code
    # personal_select += wine_code + ';'
    jh_user.personal_select = personal_select
    jh_user.save()
    res = get_response_data('000000')
    return JsonResponse(res)


def get_optional(request):
    jh_user = Jh_User.objects.get(user=request.user)
    personal_select = jh_user.personal_select
    options = personal_select.split(';')
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    data = []
    start = (page - 1) * page_num
    end = page * page_num
    for wine_code in options[start:end]:
        try:
            wine = WineInfo.objects.get(code=wine_code, is_delete=False)
        except Exception as e:
            _logger.info('wine {0} not found'.format(wine_code))
            continue
        wine_json = wine.to_json()
        wine_json['quote_change'] = '0.00%'  # 待后续补充计算方法
        data.append(wine_json)
    res = get_response_data('000000', data)
    return JsonResponse(res)


def search_wine(request):
    key = request.POST.get('key')
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    data = []
    start = (page - 1) * page_num
    end = page * page_num
    if not key:
        wine_info = WineInfo.objects.all()[start:end]
        for wine in wine_info:
            data.append(wine.to_json())
    else:
        wine_info = WineInfo.objects.filter(name__contains=key)[start:end]
        for wine in wine_info:
            data.append(wine.to_json())
    res = get_response_data('000000', data)
    return JsonResponse(res)


def del_optional(request):
    codes = request.POST.get('code')
    if not codes:
        return get_response_data('000002')
    jh_user = Jh_User.objects.get(user=request.user)
    personal_select = jh_user.personal_select.split(';')
    del_codes = list(set(codes.split(';')))
    new_codes = [code for code in personal_select if code not in del_codes]
    data = []
    start = (OPTINOAL_PAGE - 1) * OPTINOAL_PAGE_NUM
    end = OPTINOAL_PAGE * OPTINOAL_PAGE_NUM
    for wine_code in new_codes[start:end]:
        try:
            wine = WineInfo.objects.get(code=wine_code, is_delete=False)
        except Exception as e:
            _logger.info('wine {0} not found'.format(wine_code))
            continue
        wine_json = wine.to_json()
        wine_json['quote_change'] = '0.00%'  # 待后续补充计算方法
        data.append(wine_json)
    new_codes = ';'.join(new_codes)
    jh_user.personal_select = new_codes
    jh_user.save()
    res = get_response_data('000000', data)
    return JsonResponse(res)


def sell(request):
    wine_code = request.POST.get('code')
    price = request.POST.get('price')
    num = request.POST.get('num')
    if wine_code and price and num:
        try:
            wine = WineInfo.objects.get(code=wine_code)
            price = float(price)
            num = int(num)
        except Exception as e:
            _logger.info('error msg is {0}'.format(e))
            return JsonResponse(get_response_data('000002'))
    else:
        return JsonResponse(get_response_data('000002'))

    jh_user = Jh_User.objects.get(user=request.user)
    try:
        position = Position.objects.get(user=jh_user, wine=wine)
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('100002'))
    if position.num < num:
        return JsonResponse(get_response_data('100002'))
    commission_order = Commission(
        wine=wine,
        trade_direction=1,
        price=price,
        num=num,
        user=jh_user,
        status=0
    )
    commission_order.save()

    # 查询买入委托单，检测该卖出委托单可否成交
    other_comm_orders = Commission.objects.filter(
        wine=wine,
        trade_direction=0,
        status=0,
        price__gte=price
    ).order_by('create_at')
    if not other_comm_orders:
        return JsonResponse(get_response_data('000000'))
    for order in other_comm_orders:
        if num <= 0:
            break
        if order.num <= num:
            order.status = 2  # 将该委托置为成交状态
            order.save()
            deal = Deal(  # 生成成交记录
                wine=wine,
                buyer=order.user,
                seller=jh_user,
                price=order.price,
                num=order.num
            )
            deal.save()
            '''
            成交后修改资产变动，待插入
            '''
            num = num - order.num
        else:
            order.num = order.num - num
            order.save()
            deal = Deal(  # 生成成交记录
                wine=wine,
                buyer=order.user,
                seller=jh_user,
                price=order.price,
                num=num
            )
            deal.save()
            '''
            成交后修改资产变动，待插入
            '''
            num = 0
            break
    if num > 0:
        commission_order.num = num
    else:
        commission_order.status = 2
    commission_order.save()
    return JsonResponse(get_response_data('000000'))
