# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps.account.models import Jh_User
from apps.wine.models import WineInfo
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
