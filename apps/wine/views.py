# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps.account.models import Jh_User
from apps.wine.models import WineInfo
from apps import get_response_data
import logging

_logger = logging.getLogger('wineinfo')


def set_optional(request):
    wine_code = request.POST.get('code')
    if not wine_code:
        res = get_response_data('000002')
        return JsonResponse(res)
    jh_user = Jh_User.objects.get(user=request.user)
    personal_select = jh_user.personal_select
    personal_select_list = personal_select.split(';')
    if wine_code in personal_select_list:
        res = get_response_data('000009')
        return JsonResponse(res)
    personal_select += wine_code + ';'
    jh_user.personal_select = personal_select
    jh_user.save()
    res = get_response_data('000000')
    return JsonResponse(res)


def get_optional(request):
    jh_user = Jh_User.objects.get(user=request.user)
    personal_select = jh_user.personal_select
    options = personal_select.split(';')
    data = []
    for wine_code in options:
        try:
            wine = WineInfo.objects.get(code=wine_code, is_delete=False)
        except:
            _logger.info('wine {0} not found'.format(wine_code))
            continue
        wine_json = wine.to_json()
        wine_json['quote_change'] = '0.00%'  # 待后续补充计算方法
        data.append(wine_json)
    res = get_response_data('000000', data)
    return JsonResponse(res)


def search_wine(request):
    key = request.POST.get('key')
    data = []
    if not key:
        wine_info = WineInfo.objects.all()[:10]
        for wine in wine_info:
            data.append(wine.to_json())
    else:
        wine_info = WineInfo.objects.filter(name__contains=key)
        for wine in wine_info:
            data.append(wine.to_json())
    res = get_response_data('000000', data)
    return JsonResponse(res)
