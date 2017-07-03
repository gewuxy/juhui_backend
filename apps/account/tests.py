# -*- coding: utf8 -*-
import requests
import json
import time
from django.http import JsonResponse
from apps import get_response_data
import redis
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from apps.account.models import Jh_User
from apps.wine.models import Position, WineInfo, Commission
from random import choice, randint


def test_register():
    mobile = str(time.time())[:11]
    print(mobile)
    # return
    password = '123456'
    code = '1234'
    data = {'mobile': mobile, 'password': password, 'code': code}
    url = 'http://127.0.0.1:9991/apis/account/register/'
    r = requests.post(url=url, data=json.dumps(data))
    print(r)
    print(r.text)


def test_login():
    mobile = '15913152794'
    print(mobile)
    # return
    password = '123456'
    code = '1234'
    data = {'mobile': mobile, 'password': password, 'code': code}
    url = 'http://127.0.0.1:9991/apis/account/login/'
    r = requests.post(url=url, data=json.dumps(data))
    print(r)
    print(r.text)


# 【测试】创建100个测试用户
@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def create_user(request):
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)
    url = request.build_absolute_uri('/api/account/register/')
    code = '123456'
    password = '12345678'
    for i in range(100):
        mobile = str(15800000000 + i)
        redis_client.set('juhui_sms_code_' + mobile, code)
        redis_client.expire('juhui_sms_code_' + mobile, 60)
        data = {'mobile': mobile, 'password': password, 'code': code}
        r = requests.post(url=url, data=data)
        print('=====第{0}个用户的注册结果：====='.format(i + 1))
        print(r.json())
    return JsonResponse(get_response_data('000000'))


# 【测试】给用户随机分配持仓量, 账户资金
@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def distrib_position(request):
    for user in Jh_User.objects.all():
        wine = choice(WineInfo.objects.all())
        price = randint(100, 1000)
        num = randint(1, 100)
        position = Position(user=user, wine=wine, price=price, num=num)
        position.save()
        user.funds = randint(100, 1000) * randint(1, 100)
        user.save()
        print('=====给用户{0}分配的资产信息是：====='.format(user.mobile))
        print('wine: {0}, num: {1}, funds: {2}'.format(
            wine.code, num, user.funds))
    return JsonResponse(get_response_data('000000'))


# 【测试】给用户生成卖出委托单
@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def create_commission_1(request):
    for user in Jh_User.objects.all():
        try:
            position = Position.objects.get(user=user)
        except Exception:
            continue
        wine = position.wine
        trade_direction = 1
        price = position.price + 10
        num = position.num / 2
        status = 0
        commission = Commission(
            user=user,
            wine=wine,
            trade_direction=trade_direction,
            price=price,
            num=num,
            status=status
        )
        commission.save()
    return JsonResponse(get_response_data('000000'))


# 【测试】给用户生成买入委托单
@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def create_commission_0(request):
    for user in Jh_User.objects.all():
        wine = choice(WineInfo.objects.all())
        trade_direction = 0
        price = randint(100, 1000)
        num = randint(1, 100)
        status = 0
        commission = Commission(
            user=user,
            wine=wine,
            trade_direction=trade_direction,
            price=price,
            num=num,
            status=status
        )
        commission.save()
    return JsonResponse(get_response_data('000000'))


if __name__ == '__main__':
    # test_login()
    print('test...')
