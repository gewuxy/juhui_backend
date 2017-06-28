# encoding: utf8
from django.http import JsonResponse
import logging

_logger = logging.getLogger('apps-init')

RESPONSE_DATA = {
    'code': '000000',
    'msg': 'SUCCESS',
    'data': []
}

ERROR_MSG = {
    '000000': '成功',
    '000001': '请求方法错误',
    '000002': '参数错误',
    '000003': '用户已注册',
    '000004': '用户未注册',
    '000005': '发送验证码失败',
    '000006': '账号或密码错误',
    '000007': '请先登录',
    '000008': '无效用户',
    '000009': '验证码错误',
    '000010': '获取access_token错误',
    '000011': 'client数据错误',
    '100001': '已添加',
    '100002': '持仓量不足',
    '999999': '未知错误'
}


def get_response_data(code, data=False):
    RESPONSE_DATA['code'] = code
    RESPONSE_DATA['msg'] = ERROR_MSG.get(code, '')
    RESPONSE_DATA['data'] = data if data else {}
    return RESPONSE_DATA


class Middleware(object):
    def process_request(self, request):
        green_path = [
            '/api/account/register/', '/api/account/login/',
            '/api/account/sendsms/', '/api/account/resetpw/'
        ]
        if request.path in green_path:
            return
        if not (request.GET.get('token') or request.POST.get('token')):
            return JsonResponse(get_response_data('000002'))

        if not request.user.is_authenticated:
            return JsonResponse(get_response_data('000007'))
        _logger.info('current user is {0}'.format(
            request.user.username))


def index(request):
    return JsonResponse(
        {'code': '000000', 'msg': 'This is the testPage.', 'data': {}})
