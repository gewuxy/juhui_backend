# encoding: utf8
from django.http import JsonResponse

RESPONSE_DATA = {
    'code': '000000',
    'msg': 'SUCCESS',
    'data': []
}


class Middleware(object):
    def process_request(self, request):
        if request.method != 'POST':
            return JsonResponse(
                {'code': '000001',
                 'msg': 'request method must be POST',
                 'data': []})


def index(request):
    return JsonResponse({'code': '000000', 'msg': 'index SUCCESS', 'data': []})


def login(request):
    return JsonResponse({'code': '000000', 'msg': 'LOGIN SUCCESS', 'data': []})


def register(request):
    return JsonResponse(
        {'code': '000000', 'msg': 'REGISTER SUCCESS', 'data': []})


def change_pw(request):
    return JsonResponse(
        {'code': '000000', 'msg': 'CHANGE_PW SUCCESS', 'data': []})
