# -*- coding: utf8 -*-
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.contrib.auth.models import User

from apps import RESPONSE_DATA
from apps.account.models import Jh_User
import logging

_logger = logging.getLogger('register')


def is_valid(body, params_list):
    _logger.info('request.bosy: {0}'.format(body))
    body = json.loads(body)
    for i in params_list:
        if i not in body.keys():
            return False, 'param {0} is required'.format(i)
    return True, body


def register(request):
    '''
    用户注册
    '''
    is_check, body = is_valid(request.body, ['mobile', 'password', 'code'])
    # 验证码校验 start...
    # code
    # 验证码校验 end
    if not is_check:
        RESPONSE_DATA['code'] = '000002'
        RESPONSE_DATA['msg'] = body
        return JsonResponse(RESPONSE_DATA)
    users = User.objects.filter(username=body['mobile'])
    if len(users) > 0:
        RESPONSE_DATA['code'] = '000003'
        RESPONSE_DATA['msg'] = '用户已注册'
        return JsonResponse(RESPONSE_DATA)
    user = User.objects.create_user(
        username=body['mobile'],
        password=body['password']
        )
    user.save()
    jh_user = Jh_User(
        user=user,
        mobile=body['mobile'],
    )
    jh_user.save()

    return RESPONSE_DATA

