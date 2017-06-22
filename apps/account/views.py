# -*- coding: utf8 -*-
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.views.generic import View
import json
import random

from apps import RESPONSE_DATA
from apps.account.models import Jh_User
import logging
import top  # taobao SDK
from config.settings.common import ALIDAYU_KEY, ALIDAYU_SECRET, CODE_EXPIRE
from config.settings.common import REDIS

import redis

_logger = logging.getLogger('userinfo')


def is_valid(body, params_list):
    _logger.info('request.POST: {0}'.format(body))
    for i in params_list:
        if i not in body.keys():
            return False, 'param {0} is required'.format(i)
    return True, body


def register(request):
    '''
    用户注册
    '''
    is_check, body = is_valid(request.POST, ['mobile', 'password', 'code'])
    # 验证码校验 start...
    # code
    # 验证码校验 end
    if not is_check:
        RESPONSE_DATA['code'] = '000002'
        RESPONSE_DATA['msg'] = body
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)
    users = User.objects.filter(username=body['mobile'])
    if len(users) > 0:
        RESPONSE_DATA['code'] = '000003'
        RESPONSE_DATA['msg'] = '用户已注册'
        RESPONSE_DATA['data'] = []
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
    RESPONSE_DATA['code'] = '000000'
    RESPONSE_DATA['msg'] = 'SUCCESS'
    RESPONSE_DATA['data'] = []
    return JsonResponse(RESPONSE_DATA)


def login(request):
    """
    登录
    """
    is_check, body = is_valid(request.POST, ['mobile', 'password'])
    if not is_check:
        RESPONSE_DATA['code'] = '000002'
        RESPONSE_DATA['msg'] = body
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)
    try:
        u = User.objects.get(username=body['mobile'])
    except:
        RESPONSE_DATA['code'] = '000004'
        RESPONSE_DATA['msg'] = 'account not found'
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)
    user = auth.authenticate(username=u.username, password=body['password'])
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            token, is_created = Token.objects.get_or_create(user=user)
            RESPONSE_DATA['code'] = '000000'
            RESPONSE_DATA['msg'] = 'SUCCESS'
            jh_user = Jh_User.objects.get(mobile=user.username)
            jh_user_json = jh_user.to_json()
            jh_user_json['token'] = token.key
            RESPONSE_DATA['data'] = [jh_user_json]
        else:
            RESPONSE_DATA['code'] = '000006'
            RESPONSE_DATA['msg'] = 'disable account'
            RESPONSE_DATA['data'] = []
    else:
        RESPONSE_DATA['code'] = '000006'
        RESPONSE_DATA['msg'] = 'password error'
        RESPONSE_DATA['data'] = []
    return JsonResponse(RESPONSE_DATA)


def resetpassword(request):
    '''
    重置密码
    '''
    is_check, body = is_valid(request.POST, ['mobile', 'password', 'code'])
    # 验证码校验 start...
    # code
    # 验证码校验 end
    if not is_check:
        RESPONSE_DATA['code'] = '000002'
        RESPONSE_DATA['msg'] = body
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)
    users = User.objects.filter(username=body['mobile'])
    if len(users) > 0:
        user = users[0]
        user.set_password(body['password'])
        user.save()
        RESPONSE_DATA['code'] = '000000'
        RESPONSE_DATA['msg'] = 'SUCCESS'
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)
    else:
        RESPONSE_DATA['code'] = '000004'
        RESPONSE_DATA['msg'] = 'account not found'
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)


def logout(request):
    '''
    退出登录
    '''
    auth.logout(request)
    RESPONSE_DATA['code'] = '000000'
    RESPONSE_DATA['msg'] = 'SUCCESS'
    RESPONSE_DATA['data'] = []
    return JsonResponse(RESPONSE_DATA)


def _SendSms(extend, sms_type, sign, param, num, template):
    '''
    阿里大于发送短信
    '''
    _logger.info('function _SendSms request params: {0}'.format(
        (extend, sms_type, sign, param, num, template)))
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(ALIDAYU_KEY, ALIDAYU_SECRET))

    if extend:
        req.extend = extend  # 回传参数
    req.sms_type = sms_type  # 短信
    req.sms_free_sign_name = sign  # 短信签名
    req.sms_param = param
    req.rec_num = num
    req.sms_template_code = template
    try:
        resp = req.getResponse()
    except Exception as e:
        resp = 'ERROR_MESSAGE: {0}'.format(e)
    _logger.info('function _SendSms response: {0}'.format(resp))
    return resp


def send_sms(request):

    '''
    发送验证码短信(阿里大于)
    '''
    is_check, body = is_valid(request.POST, ['mobile'])
    if not is_check:
        RESPONSE_DATA['code'] = '000002'
        RESPONSE_DATA['msg'] = body
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)

    extend = body.get('extend', '')
    sms_type = body.get('sms_type', 'normal')
    sign_name = body.get('sign_name', '小秋')
    mobile = body['mobile']
    sms_template = body.get('sms_template', 'SMS_71530021')
    param = body.get('param')
    if not param:
        code = str(random.randint(100000, 999999))
        param = json.dumps({'code': code, 'time': str(CODE_EXPIRE)})

    # 将验证码存入redis中
    try:
        param_dict = json.loads(param)
        param_code = param_dict['code']
        param_expire = int(param_dict['time'])
    except:
        RESPONSE_DATA['code'] = '000005'
        RESPONSE_DATA['msg'] = '参数param错误'
        RESPONSE_DATA['data'] = []
        return JsonResponse(RESPONSE_DATA)
    redis_client = redis.StrictRedis(host=REDIS['HOST'], port=REDIS['PORT'], db=1)
    redis_key = 'juhui_sms_code_' + mobile
    redis_client.set(redis_key, param_code)
    redis_client.expire(redis_key, param_expire)

    resp = _SendSms(extend, sms_type, sign_name, param, mobile, sms_template)
    if isinstance(resp, str):
        if resp.find('ERROR_MESSAGE') == 0:
            RESPONSE_DATA['code'] = '000005'
    else:
        RESPONSE_DATA['code'] = '000000'
    RESPONSE_DATA['msg'] = str(resp)
    RESPONSE_DATA['data'] = []
    return JsonResponse(RESPONSE_DATA)


class InfoView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            print('true11111111111111')
        else:
            print('flase2222222222222')
        mobile = request.GET.get('mobile')
        if not mobile:
            RESPONSE_DATA['code'] = '000002'
            RESPONSE_DATA['msg'] = 'param mobile is required'
            RESPONSE_DATA['data'] = []
            return JsonResponse(RESPONSE_DATA)
        try:
            jh_user = Jh_User.objects.get(mobile=mobile)
        except:
            RESPONSE_DATA['code'] = '000004'
            RESPONSE_DATA['msg'] = 'account not found'
            RESPONSE_DATA['data'] = []
            return JsonResponse(RESPONSE_DATA)
        _logger.info('account {0} info: {1}'.format(mobile, jh_user.to_json()))
        RESPONSE_DATA['code'] = '000000'
        RESPONSE_DATA['msg'] = 'SUCCESS'
        RESPONSE_DATA['data'] = [jh_user.to_json()]
        return JsonResponse(RESPONSE_DATA)

    def post(self, request, *args, **kwargs):
        mobile = request.POST.get('mobile')
        if not mobile:
            RESPONSE_DATA['code'] = '000002'
            RESPONSE_DATA['msg'] = 'param mobile is required'
            RESPONSE_DATA['data'] = []
            return JsonResponse(RESPONSE_DATA)
        try:
            jh_user = Jh_User.objects.get(mobile=mobile)
        except:
            RESPONSE_DATA['code'] = '000004'
            RESPONSE_DATA['msg'] = 'account not found'
            RESPONSE_DATA['data'] = []
            return JsonResponse(RESPONSE_DATA)
        nickname = request.POST.get('nickname')
        if nickname:
            jh_user.nickname = nickname
        img_url = request.POST.get('img_url')
        if img_url:
            jh_user.img_url = img_url
        email = request.POST.get('email')
        if email:
            jh_user.email = email
        jh_user.save()
        RESPONSE_DATA['code'] = '000000'
        RESPONSE_DATA['msg'] = 'SUCCESS'
        RESPONSE_DATA['data'] = [jh_user.to_json()]
        return JsonResponse(RESPONSE_DATA)
