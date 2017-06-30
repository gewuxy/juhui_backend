# -*- coding: utf8 -*-
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
import random
import time

from apps import get_response_data
from apps.account.models import Jh_User
import logging
import top  # taobao SDK
from config.settings.common import ALIDAYU_KEY, ALIDAYU_SECRET, CODE_EXPIRE
from config.settings.common import REDIS

import redis
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from oauth2_provider.models import AccessToken, RefreshToken

_logger = logging.getLogger('userinfo')
TIMEOUT = 5


def is_valid(body, params_list):
    _logger.info('request.POST: {0}'.format(body))
    for i in params_list:
        if i not in body.keys():
            return False, 'param {0} is required'.format(i)
    return True, body


def check_sms_code(mobile, code):
    redis_client = redis.StrictRedis(
        host=REDIS['HOST'], port=REDIS['PORT'], db=1)
    code_in_redis = redis_client.get('juhui_sms_code_' + mobile)
    if code_in_redis is None:
        return False
    if code_in_redis.decode('utf8') != code:
        return False
    else:
        return True


def get_access_token(url, username, password, client_id, client_secret):
    data = {
        'url': url,
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret
    }
    redis_client = redis.StrictRedis(
        host=REDIS['HOST'], port=REDIS['PORT'], db=1)
    redis_client.publish('token', data)
    timeout = TIMEOUT
    break_time = int(time.time()) + timeout
    token = {}
    pre_token = redis_client.get('juhui_access_token_' + username)
    while True:
        if int(time.time()) > break_time:
            break
        token = redis_client.get('juhui_access_token_' + username)
        if token != pre_token:
            token = json.loads(token.decode('utf8').replace('\'', '\"'))
            break
    return token


def register(request):
    '''
    用户注册
    '''
    is_check, body = is_valid(request.POST, ['mobile', 'password', 'code'])
    if not is_check:
        return JsonResponse(get_response_data('000002'))
    # 验证码校验 start...
    if not check_sms_code(body['mobile'], body['code']):
        return JsonResponse(get_response_data('000009'))
    # 验证码校验 end
    users = User.objects.filter(username=body['mobile'])
    if len(users) > 0:
        return JsonResponse(get_response_data('000003'))
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
    return JsonResponse(get_response_data('000000'))


def login(request):
    """
    登录
    """
    is_check, body = is_valid(
        request.POST, ['mobile', 'password', 'client_id', 'client_secret'])
    if not is_check:
        return JsonResponse(get_response_data('000002'))
    try:
        oauth2_info = get_access_token(
            request.build_absolute_uri('/o/token/'), body['mobile'],
            body['password'], body['client_id'], body['client_secret'])
    except Exception:
        return JsonResponse(get_response_data('000010'))
    if oauth2_info.get('error'):
        if oauth2_info.get('error') == 'invalid_client':
            return JsonResponse(get_response_data('000011'))
        else:
            return JsonResponse(get_response_data('000006'))
    token = oauth2_info.get('access_token')
    if not token:
        return JsonResponse(get_response_data('000010'))
    jh_user = Jh_User.objects.get(mobile=body['mobile'])
    jh_user_json = jh_user.to_json()
    jh_user_json['token'] = token
    _logger.info('login info: {0}'.format(jh_user_json))
    return JsonResponse(get_response_data('000000', jh_user_json))


def resetpassword(request):
    '''
    重置密码
    '''
    is_check, body = is_valid(request.POST, ['mobile', 'password', 'code'])
    if not is_check:
        res = get_response_data('000002')
        return JsonResponse(res)
    # 验证码校验 start...
    if not check_sms_code(body['mobile'], body['code']):
        return JsonResponse(get_response_data('000009'))
    # 验证码校验 end
    users = User.objects.filter(username=body['mobile'])
    if len(users) > 0:
        user = users[0]
        user.set_password(body['password'])
        user.save()
        res = get_response_data('000000')
        return JsonResponse(res)
    else:
        res = get_response_data('000004')
        return JsonResponse(res)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def logout(request):
    '''
    退出登录
    '''
    _logger.info('logout access_token is {0}'.format(
        request.META.get('HTTP_AUTHORIZATION')))
    token = request.META.get('HTTP_AUTHORIZATION').split('Bearer ')[1]
    access_token = AccessToken.objects.get(token=token)
    refresh_token = RefreshToken.objects.get(access_token_id=access_token.id)
    refresh_token.delete()
    access_token.delete()
    res = get_response_data('000000')
    return JsonResponse(res)


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
        res = get_response_data('000002')
        return JsonResponse(res)

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
    except Exception:
        res = get_response_data('000005')
        return JsonResponse(res)
    redis_client = redis.StrictRedis(
        host=REDIS['HOST'], port=REDIS['PORT'], db=1)
    redis_key = 'juhui_sms_code_' + mobile
    redis_client.set(redis_key, param_code)
    redis_client.expire(redis_key, param_expire)

    resp = _SendSms(extend, sms_type, sign_name, param, mobile, sms_template)
    res = get_response_data('000000')
    if isinstance(resp, str):
        if resp.find('ERROR_MESSAGE') == 0:
            res = get_response_data('000005')
    return JsonResponse(res)


class InfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            jh_user = Jh_User.objects.get(user=request.user)
        except Exception:
            res = get_response_data('000004')
            return JsonResponse(res)
        _logger.info('account info: {0}'.format(jh_user.to_json()))
        res = get_response_data('000000', jh_user.to_json())
        return Response(res)

    def post(self, request, *args, **kwargs):
        try:
            jh_user = Jh_User.objects.get(user=request.user)
        except Exception:
            res = get_response_data('000004')
            return JsonResponse(res)
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
        res = get_response_data('000000', jh_user.to_json())
        return JsonResponse(res)
