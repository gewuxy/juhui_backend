# -*- coding: utf8 -*-
from django.http import JsonResponse
from django.db.models import Q
from apps.account.models import Jh_User
from apps.wine.models import WineInfo
from apps.wine.models import Commission, Deal, Position
from apps.wine.wine_view_lib import last_price_ratio
from apps import get_response_data
from apps.wine.wine_view_lib import price_emit, change_price, select_emit, REDIS_CLIENT

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import datetime
import time
import logging


_logger = logging.getLogger('wineinfo')
OPTINOAL_PAGE = 1  # 自选列表默认页码
OPTINOAL_PAGE_NUM = 10  # 自选列表默认页长
MAX_PAGE_NUM = 100


def get_wine_list(codes_str, start=0, end=MAX_PAGE_NUM):
    '''
    :param codes_str: 个人信息中的自选列表
    :param start: 开始索引
    :param end: 结尾索引
    :return: 根据自选列表信息中的code返回自选酒的详细信息列表
    '''
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


# 添加自选
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
    # 推送最新自选信息
    rval = select_emit(wine_code, 'add')
    if rval:
        _logger.info('推送最新自选信息<<<成功>>>!')
    else:
        _logger.info('推送最新自选信息<<<失败>>>!')
    res = get_response_data('000000')
    return JsonResponse(res)


# 获取自选列表
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_optional(request):
    jh_user = Jh_User.objects.get(user=request.user)
    personal_select = jh_user.personal_select
    options = personal_select.split(';')
    try:
        page = int(request.GET.get('page', OPTINOAL_PAGE))
        page_num = int(request.GET.get('page_num', OPTINOAL_PAGE_NUM))
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
        last_price, ratio = last_price_ratio(wine_code)
        wine_json['quote_change'] = ratio  # 待后续补充计算方法
        wine_json['last_price'] = last_price
        # wine_json['proposed_price'] = last_price
        wine_json['sort_no'] = sort_no
        data.append(wine_json)
        sort_no += 1
    res = get_response_data('000000', data)
    return JsonResponse(res)


# 搜索
# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def search_wine(request):
    key = request.POST.get('key')
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    try:
        jh_user = Jh_User.objects.get(user=request.user)
        select_codes = jh_user.personal_select.split(';')
    except Exception:
        select_codes = []
    data = []
    start = (page - 1) * page_num
    end = page * page_num
    if not key:
        wine_info = WineInfo.objects.all()[start:end]
        for wine in wine_info:
            wine_json = wine.to_json()
            last_price, ratio = last_price_ratio(wine.code)
            wine_json['last_price'] = last_price
            if wine.code in select_codes:
                wine_json['is_select'] = True
            else:
                wine_json['is_select'] = False
            data.append(wine_json)
    else:
        # wine_info = WineInfo.objects.filter(name__contains=key)[start:end]
        wine_info = WineInfo.objects.filter(Q(name__contains=key) | Q(code__contains=key))[start:end]
        for wine in wine_info:
            wine_json = wine.to_json()
            last_price, ratio = last_price_ratio(wine.code)
            wine_json['last_price'] = last_price
            if wine.code in select_codes:
                wine_json['is_select'] = True
            else:
                wine_json['is_select'] = False
            data.append(wine_json)
    res = get_response_data('000000', data)
    return JsonResponse(res)


# 删除自选
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
    # 推送最新自选信息
    for del_code in del_codes:
        rval = select_emit(del_code, 'delete')
        if rval:
            _logger.info('code: {0}, 推送最新自选信息<<<成功>>>!'.format(del_code))
        else:
            _logger.info('code: {0}, 推送最新自选信息<<<失败>>>!'.format(del_code))
    res = get_response_data('000000', data)
    return JsonResponse(res)


# 对自选数据排序
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


# 卖出
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
    position.num -= num
    position.save()
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
        price__gte=price,
        create_at__date=datetime.datetime.now().date()
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
            # 修改WineInfo中的价格proposed_price
            res_change = change_price(wine.code, order.price)
            if res_change:
                _logger.info('修改价格成功！')
            else:
                _logger.info('修改价格失败！')
            # 广播最新价格
            timestamp = str(int(time.time() * 1000))
            res_emit = price_emit(wine.code, timestamp)
            if res_emit:
                _logger.info('最新价格广播成功！')
            else:
                _logger.info('最新价格广播失败！')
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
            # 修改WineInfo中的价格proposed_price
            res_change = change_price(wine.code, order.price)
            if res_change:
                _logger.info('修改价格成功！')
            else:
                _logger.info('修改价格失败！')
            # 广播最新价格
            timestamp = str(int(time.time() * 1000))
            res = price_emit(wine.code, timestamp)
            if res:
                _logger.info('最新价格广播成功！')
            else:
                _logger.info('最新价格广播失败！')
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


# 买入
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
        status=0,
        create_at__date=datetime.datetime.now().date()
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
            # 修改WineInfo中的价格proposed_price
            res_change = change_price(wine.code, order.price)
            if res_change:
                _logger.info('修改价格成功！')
            else:
                _logger.info('修改价格失败！')
            # 广播最新价格
            timestamp = str(int(time.time() * 1000))
            res = price_emit(wine.code, timestamp)
            if res:
                _logger.info('最新价格广播成功！')
            else:
                _logger.info('最新价格广播失败！')
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
            # 修改WineInfo中的价格proposed_price
            res_change = change_price(wine.code, order.price)
            if res_change:
                _logger.info('修改价格成功！')
            else:
                _logger.info('修改价格失败！')
            # 广播最新价格
            timestamp = str(int(time.time() * 1000))
            res = price_emit(wine.code, timestamp)
            if res:
                _logger.info('最新价格广播成功！')
            else:
                _logger.info('最新价格广播失败！')
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


# 详情页数据
def detail(request):
    lastest_price = 0  # 最新价
    highest_price = 0  # 最高价
    lowest_price = 0  # 最低价
    turnover_rate = ''  # 换手率
    ratio = 0.00  # 量比
    deal_count = 0  # 成交量
    total_market_value = 0  # 总市值
    amplitude = ''  # 振幅
    wine_code = request.POST.get('code')
    if not wine_code:
        return JsonResponse(get_response_data('000002'))
    try:
        wine = WineInfo.objects.get(code=wine_code)
    except Exception:
        _logger.info('wine {0} not found'.format(wine_code))
        return JsonResponse(get_response_data('000002'))

    # 最新价／最高价／最低价计算
    deals = Deal.objects.filter(wine=wine).order_by('create_at')
    for deal in deals:
        lastest_price = deal.price
        if deal_count == 0:
            highest_price = deal.price
            lowest_price = deal.price
            deal_count = deal.num
        else:
            deal_count += deal.num
            if highest_price < deal.price:
                highest_price = deal.price
            if lowest_price > deal.price:
                lowest_price = deal.price

    # 换手率计算
    all_position = Position.objects.all()
    all_wine_coount = 0
    for position in all_position:
        all_wine_coount += position.num
    if all_wine_coount == 0:
        turnover_rate = '0.00%'
    else:
        turnover_rate = '{:.2f}%'.format(
            deal_count / all_wine_coount * 100)

    # 总市值计算
    total_market_value = all_wine_coount * lastest_price

    # 量比计算
    today = datetime.datetime.now()
    deals_today = Deal.objects.filter(create_at__date=today.date())
    deals_today_account = 0
    today_high_price = 0
    today_low_price = 0
    yesterday_last_price = 0
    for deal in deals_today:
        if deals_today_account == 0:
            today_high_price = deal.price
            today_low_price = deal.price
        else:
            if today_high_price < deal.price:
                today_high_price = deal.price
            if today_low_price > deal.price:
                today_low_price = deal.price
        deals_today_account += deal.num
    deals_5_days_account = 0
    end_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
    start_day = end_day - datetime.timedelta(days=5)
    deals_5_days = Deal.objects.filter(
        create_at__gt=start_day, create_at__lt=end_day).order_by('create_at')
    for deal in deals_5_days:
        deals_5_days_account += deal.num
    if deals_5_days_account > 0:
        yesterday_last_price = deal.price
    if deals_5_days_account == 0:
        ratio = 0.00
    else:
        if today.minute == 0:
            ratio = deals_today_account / (
                deals_5_days_account / 5 / 60)
        else:
            ratio = deals_today_account / (
                deals_5_days_account / 5 / 60 * today.minute)
        ratio = round(ratio, 2)

    # 振幅计算
    if yesterday_last_price == 0:
        amplitude = '0.00%'
    else:
        amplitude = '{:.2f}%'.format(
            (today_high_price - today_low_price) / yesterday_last_price)

    # 五档
    sell_5_level = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    buy_5_level = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    count = 0
    for comm in Commission.objects.filter(
            wine=wine,
            trade_direction=1,
            status=0,
            create_at__date=datetime.datetime.now().date()).order_by('price'):
        if count == 5:
            break
        if count == 0:
            sell_5_level[count] = (comm.price, comm.num)
            count += 1
        elif comm.price == sell_5_level[count - 1][0]:
            sell_5_level[count] = (
                comm.price,
                comm.num + sell_5_level[count][1])
        else:
            sell_5_level[count] = (comm.price, comm.num)
            count += 1
    count = 0
    for comm in Commission.objects.filter(
            wine=wine,
            trade_direction=0,
            status=0,
            create_at__date=datetime.datetime.now().date()).order_by('-price'):
        if count == 5:
            break
        if count == 0:
            buy_5_level[count] = (comm.price, comm.num)
            count += 1
        elif comm.price == buy_5_level[count - 1][0]:
            buy_5_level[count] = (
                comm.price,
                comm.num + buy_5_level[count][1])
        else:
            buy_5_level[count] = (comm.price, comm.num)
            count += 1

    data = {
        'lastest_price': lastest_price,
        'highest_price': highest_price,
        'lowest_price': lowest_price,
        'turnover_rate': turnover_rate,
        'ratio': ratio,
        'deal_count': deal_count,
        'total_market_value': total_market_value,
        'amplitude': amplitude,
        'sell_5_level': sell_5_level,
        'buy_5_level': buy_5_level
    }
    return JsonResponse(get_response_data('000000', data))


# 当日成交
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def today_deal(request):
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        return JsonResponse(get_response_data('000007'))
    start = (page - 1) * page_num
    end = page * page_num
    today = datetime.datetime.now().date()
    deals = Deal.objects.filter(Q(create_at__date=today), Q(buyer=jh_user) | Q(seller=jh_user))[start:end]
    deals_json = []
    for deal in deals:
        deals_json.append(deal.to_json())
    return JsonResponse(get_response_data('000000', deals_json))


# 历史成交
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def history_deal(request):
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        return JsonResponse(get_response_data('000007'))
    start = (page - 1) * page_num
    end = page * page_num
    today = datetime.datetime.now().date()
    deals = Deal.objects.filter(Q(buyer=jh_user) | Q(seller=jh_user))[start:end]
    deals_json = []
    for deal in deals:
        deals_json.append(deal.to_json())
    return JsonResponse(get_response_data('000000', deals_json))


# 当日委托
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def today_commission(request):
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        return JsonResponse(get_response_data('000007'))
    start = (page - 1) * page_num
    end = page * page_num
    today = datetime.datetime.now().date()
    commissions = Commission.objects.filter(create_at__date=today, user=jh_user)[start:end]
    commissions_json = []
    for commission in commissions:
        commissions_json.append(commission.to_json())
    return JsonResponse(get_response_data('000000', commissions_json))


# 历史委托
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def history_commission(request):
    try:
        page = int(request.POST.get('page', OPTINOAL_PAGE))
        page_num = int(request.POST.get('page_num', OPTINOAL_PAGE_NUM))
    except Exception as e:
        _logger.info('error msg is {0}'.format(e))
        return JsonResponse(get_response_data('000002'))
    try:
        jh_user = Jh_User.objects.get(user=request.user)
    except Exception:
        return JsonResponse(get_response_data('000007'))
    start = (page - 1) * page_num
    end = page * page_num
    today = datetime.datetime.now().date()
    commissions = Commission.objects.filter(user=jh_user)[start:end]
    commissions_json = []
    for commission in commissions:
        commissions_json.append(commission.to_json())
    return JsonResponse(get_response_data('000000', commissions_json))