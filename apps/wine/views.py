# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps.account.models import Jh_User
from apps.wine.models import WineInfo
from apps.wine.models import Commission, Deal, Position
from apps import get_response_data
import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

_logger = logging.getLogger('wineinfo')
OPTINOAL_PAGE = 1  # 自选列表默认页码
OPTINOAL_PAGE_NUM = 10  # 自选列表默认页长
MAX_PAGE_NUM = 100


def get_wine_list(codes_str, start=0, end=MAX_PAGE_NUM):
    codes_list = codes_str.split(';')
    data = []
    sort_no = start
    for wine_code in codes_list[start:end]:
        try:
            wine = WineInfo.objects.get(code=wine_code, is_delete=False)
        except Exception as e:
            _logger.info('wine {0} not found'.format(wine_code))
            continue
        wine_json = wine.to_json()
        wine_json['quote_change'] = '0.00%'  # 待后续补充计算方法
        wine_json['sort_no'] = sort_no
        data.append(wine_json)
        sort_no += 1
    return data


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
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


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
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
    sort_no = start
    for wine_code in options[start:end]:
        try:
            wine = WineInfo.objects.get(code=wine_code, is_delete=False)
        except Exception as e:
            _logger.info('wine {0} not found'.format(wine_code))
            continue
        wine_json = wine.to_json()
        wine_json['quote_change'] = '0.00%'  # 待后续补充计算方法
        wine_json['sort_no'] = sort_no
        data.append(wine_json)
        sort_no += 1
    res = get_response_data('000000', data)
    return JsonResponse(res)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def search_wine(request):
    key = request.POST.get('key')
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    jh_user = Jh_User.objects.get(user=request.user)
    select_codes = jh_user.personal_select.split(';')
    data = []
    start = (page - 1) * page_num
    end = page * page_num
    if not key:
        wine_info = WineInfo.objects.all()[start:end]
        for wine in wine_info:
            wine_json = wine.to_json()
            if wine.code in select_codes:
                wine_json['is_select'] = True
            else:
                wine_json['is_select'] = False
            data.append(wine_json)
    else:
        wine_info = WineInfo.objects.filter(name__contains=key)[start:end]
        for wine in wine_info:
            wine_json = wine.to_json()
            if wine.code in select_codes:
                wine_json['is_select'] = True
            else:
                wine_json['is_select'] = False
            data.append(wine_json)
    res = get_response_data('000000', data)
    return JsonResponse(res)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
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


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def sort_optional(request):
    sort_type = request.POST.get('sort_type', '1')
    page = request.POST.get('page', str(OPTINOAL_PAGE))
    page_num = request.POST.get('page_num', str(OPTINOAL_PAGE_NUM))
    if not (page.isdigit() and page_num.isdigit()):
        return JsonResponse(get_response_data('000002'))
    page = int(page)
    page_num = int(page_num)
    jh_user = Jh_User.objects.get(user=request.user)
    personal_select = jh_user.personal_select
    if sort_type == '1':  # 移动单个选项
        wine_code = request.POST.get('code', '')
        sort_no = request.POST.get('sort_no', '')
        if wine_code and sort_no.isdigit():
            sort_no = int(sort_no)
            personal_select_list = personal_select.split(';')
            if (sort_no >= len(personal_select_list)) or (
                    wine_code not in personal_select_list):  # 移到末尾
                tmp = ';'.join(personal_select.split(wine_code + ';'))
                jh_user.personal_select = tmp + ';' + wine_code
                jh_user.save()
            else:
                origin_no = personal_select_list.index(wine_code)
                if origin_no < sort_no:  # 往后移
                    for i in range(origin_no, sort_no):
                        personal_select_list[i] = personal_select_list[i + 1]
                else:  # 往前移
                    for j in range(origin_no, sort_no, -1):
                        personal_select_list[j] = personal_select_list[j - 1]
                personal_select_list[sort_no] = wine_code
                jh_user.personal_select = ';'.join(personal_select_list)
                jh_user.save()
            data = get_wine_list(
                jh_user.personal_select,
                (page - 1) * page_num,
                page * page_num)
            return JsonResponse(get_response_data('000000', data))
        else:
            return JsonResponse(get_response_data('000002'))
    else:  # 全局排序
        sort_codes = request.POST.get('sort_codes')
        if not sort_codes:
            return JsonResponse(get_response_data('000002'))
        data = get_wine_list(
            sort_codes, (page - 1) * page_num, page * page_num)
        return JsonResponse(get_response_data('000000', data))


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
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


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def buy(request):
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
    '''
    是否需要考虑账户资金情况，待补充
    '''
    # 生成委托单
    commission_order = Commission(
        wine=wine,
        trade_direction=0,
        price=price,
        num=num,
        user=jh_user,
        status=0
    )
    commission_order.save()

    # 查询卖出委托单，检测该买入委托单可否成交
    other_comm_orders = Commission.objects.filter(
        wine=wine,
        trade_direction=1,
        status=0,
        price__lte=price
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
                seller=order.user,
                buyer=jh_user,
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
                seller=order.user,
                buyer=jh_user,
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
