# encoding: utf8
from django.http import JsonResponse

RESPONSE_DATA = {
    'code': '000000',
    'msg': 'SUCCESS',
    'data': []
}


class Middleware(object):
    def process_request(self, request):
        green_path = ['/api/account/register/', '/api/account/login/', '/api/account/sendsms/']
        if request.path in green_path:
            return
        if not request.user.is_authenticated:
            return JsonResponse(
                {'code': '000007',
                 'msg': '请先登录',
                 'data': []})


def index(request):
    return JsonResponse({'code': '000000', 'msg': 'index SUCCESS', 'data': []})
