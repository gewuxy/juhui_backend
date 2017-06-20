# -*- coding: utf8 -*-
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib import auth

from apps import RESPONSE_DATA
from apps.account.models import Jh_User
import logging
import top  # taobao SDK
from config.settings.common import ALIDAYU_KEY, ALIDAYU_SECRET

_logger = logging.getLogger('userinfo')


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

    return JsonResponse(RESPONSE_DATA)


def login(request):
    """
    登录
    """
    is_check, body = is_valid(request.body, ['mobile', 'password'])
    if not is_check:
        RESPONSE_DATA['code'] = '000002'
        RESPONSE_DATA['msg'] = body
        return JsonResponse(RESPONSE_DATA)
    try:
        u = User.objects.get(username=body['mobile'])
    except:
        RESPONSE_DATA['code'] = '000004'
        RESPONSE_DATA['msg'] = 'account not found'
        return JsonResponse(RESPONSE_DATA)
    user = auth.authenticate(username=u.username, password=body['password'])
    auth.login(request, user)

    return JsonResponse(RESPONSE_DATA)


def resetpassword(request):
    '''
    重置密码
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
        user = users[0]
        user.password = body['password']
    else:
        user = User.objects.create_user(
            username=body['mobile'],
            password=body['password']
            )
    user.save()

    return JsonResponse(RESPONSE_DATA)


def logout(request):
    '''
    退出登录
    '''
    auth.logout(request)
    return JsonResponse(RESPONSE_DATA)


def send_sms(request):
    '''
    发送验证码短信(阿里大于)
    '''
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(ALIDAYU_KEY, ALIDAYU_SECRET))

    # req.extend = "123456"  # 回传参数
    req.sms_type = "normal"  # 短信
    req.sms_free_sign_name = "小秋".encode('utf8')  # 短信签名
    req.sms_param = "{\"code\":\"1234\",\"time\":\"5\"}"
    req.rec_num = "15913152794"
    req.sms_template_code = "SMS_71530021"
    resp = req.getResponse()
    RESPONSE_DATA['data'].append(resp)
    return JsonResponse(RESPONSE_DATA)

    RESPONSE_DATA['code'] = '000005'
    RESPONSE_DATA['msg'] = '发送验证码短信失败'
    return JsonResponse(RESPONSE_DATA)
