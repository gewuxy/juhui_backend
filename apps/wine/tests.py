# -*- coding: utf8 -*-
import random
from apps.wine.models import WineInfo
from django.http import JsonResponse
from apps import get_response_data


def insert_wine(request):
    for i in range(20):
        name = '正牌木桐干红{0}'.format(random.randint(1900, 2000))
        code = '{0}'.format(random.randint(100000, 999999))
        winery = '{0}号庄园'.format(random.randint(1, 20))
        proposed_price = float(random.randint(10000, 99999))
        wine = WineInfo(name=name, code=code, winery=winery,
                        proposed_price=proposed_price)
        wine.save()
    return JsonResponse(get_response_data('000000'))


if __name__ == '__main__':
    insert_wine()
