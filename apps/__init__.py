# encoding: utf8
from django.http import JsonResponse

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
    '000009': '已选择'
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
        if not request.user.is_authenticated:
            return JsonResponse(
                {'code': '000007',
                 'msg': ERROR_MSG['000007'],
                 'data': {}})


def index(request):
    return JsonResponse({'code': '000000', 'msg': 'This is the testPage.', 'data': {}})
