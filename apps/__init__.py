# encoding: utf8
from django.http import JsonResponse


def index(request):
    return JsonResponse({'code': '000000', 'msg': 'index SUCCESS', 'data': []})


def login(request):
    return JsonResponse({'code': '000000', 'msg': 'LOGIN SUCCESS', 'data': []})


def register(request):
    return JsonResponse({'code': '000000', 'msg': 'REGISTER SUCCESS', 'data': []})


def change_pw(request):
    return JsonResponse({'code': '000000', 'msg': 'CHANGE_PW SUCCESS', 'data': []})
