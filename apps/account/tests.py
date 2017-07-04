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
from apps.wine.models import Position, WineInfo, Commission, Deal
from random import choice, randint
import datetime


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
# @api_view(['GET'])
def create_commission_1(request):
    for user in Jh_User.objects.filter(mobile__contains='1580000'):
        # 登录获取token
        mobile = user.mobile
        password = '12345678'
        client_id = 'tNLzffNGNVNhUKYgB58edo2pplyUx47ZvgeS6TeS'
        client_secret = 'SVsdE9ccpgqa9KyONrReeEbu8nql439Dp0ydsMVG0PfevOxw3mS4EZ0PkNBpyuC6aDrBWs1WHWS96yw7Luno8UMfLOJkiKEOKHFxLBCA4p0vHkXxhe5qwLkAL7T5juIr'
        data = {
            'mobile': mobile,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret
        }
        login_url = request.build_absolute_uri('/api/account/login/')
        r = requests.post(url=login_url, data=data)
        print('======login result is ======')
        print(r.json())
        token = r.json()['data']['token']

        # 请求卖出接口
        sell_url = request.build_absolute_uri('/api/wine/sell/')
        headers = {'Authorization': 'Bearer {0}'.format(token)}
        data = {'code': '', 'price': '', 'num': ''}
        try:
            position = Position.objects.get(user=user)
        except Exception:
            continue
        data['code'] = position.wine.code
        data['price'] = float(position.price) + 10
        data['num'] = int(position.num) // 2
        r = requests.post(url=sell_url, data=data, headers=headers)
        print('========sell result is========')
        print(r.json())

    return JsonResponse(get_response_data('000000'))


# 【测试】给用户生成买入委托单
def create_commission_0(request):
    for user in Jh_User.objects.filter(mobile__contains='1580000'):
        # 登录获取token
        mobile = user.mobile
        password = '12345678'
        client_id = 'tNLzffNGNVNhUKYgB58edo2pplyUx47ZvgeS6TeS'
        client_secret = 'SVsdE9ccpgqa9KyONrReeEbu8nql439Dp0ydsMVG0PfevOxw3mS4EZ0PkNBpyuC6aDrBWs1WHWS96yw7Luno8UMfLOJkiKEOKHFxLBCA4p0vHkXxhe5qwLkAL7T5juIr'
        data = {
            'mobile': mobile,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret
        }
        login_url = request.build_absolute_uri('/api/account/login/')
        r = requests.post(url=login_url, data=data)
        print('======login result is ======')
        print(r.json())
        token = r.json()['data']['token']

        # 请求买入接口
        sell_url = request.build_absolute_uri('/api/wine/buy/')
        headers = {'Authorization': 'Bearer {0}'.format(token)}
        data = {'code': '', 'price': '', 'num': ''}
        wine = choice(WineInfo.objects.all())
        try:
            position = Position.objects.get(wine=wine)
        except Exception:
            continue
        data['code'] = wine.code
        data['price'] = float(position.price) + randint(-10, 10)
        data['num'] = int(position.num) // 2
        r = requests.post(url=sell_url, data=data, headers=headers)
        print('========sell result is========')
        print(r.json())

    return JsonResponse(get_response_data('000000'))


def _rand_datetime():
    year = choice([2016, 2017])
    if year == 2016:
        month = choice(range(1, 13))
    else:
        month = choice(range(1, 7))
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = choice(range(1, 32))
    elif month == 2:
        day = choice(range(1, 29))
    else:
        day = choice(range(1, 31))
    hour = choice(range(0, 23))
    minute = choice(range(0, 59))
    second = choice(range(0, 59))
    microsecond = choice(range(0, 1000000))
    now = datetime.datetime.now()
    rand_now = now.replace(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond
    )
    return rand_now


# 【测试】生成成交单
@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def create_deal(request):
    number = request.GET.get('number', 100)
    number = int(number)
    for i in range(number):
        wine = choice(WineInfo.objects.all())
        buyer = choice(Jh_User.objects.all())
        seller = choice(Jh_User.objects.all())
        price = randint(100, 1000)
        num = randint(1, 100)
        create_at = _rand_datetime()
        deal = Deal(
            wine=wine,
            buyer=buyer,
            seller=seller,
            price=price,
            num=num,
            create_at=create_at
        )
        deal.save()
    return JsonResponse(get_response_data('000000'))


if __name__ == '__main__':
    # test_login()
    print('test...')
