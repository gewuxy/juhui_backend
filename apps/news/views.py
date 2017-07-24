# -*- coding: utf8 -*-
from django.http import JsonResponse
from apps import get_response_data
from apps.news.models import NewsInfo

from bs4 import BeautifulSoup
import requests
import datetime


# 资讯入库
def insert_news(request):
    title = request.POST.get('title')
    thumb_img = request.POST.get('thumb_img')
    news_time = request.POST.get('news_time')
    href = request.POST.get('href')
    if not (title and href):
        return JsonResponse(get_response_data('000002'))
    try:
        news_time = datetime.datetime.strptime(news_time, '%Y-%m-%d %H:%M')
    except Exception:
        news_time = datetime.datetime.now()
    news_info = NewsInfo(title=title, href=href, thumb_img=thumb_img, news_time=news_time)
    news_info.save()
    return JsonResponse(get_response_data('000000'))


# 读取资讯
def get_news(request):
    try:
        num = int(request.POST.get('num', 15))
    except Exception:
        return JsonResponse(get_response_data('000002'))
    news = NewsInfo.objects.all().order_by('-news_time')
    data = []
    titles = []
    for n in news:
        if len(data) == num:
            break
        if n.title in titles:
            continue
        data.append(n.to_json())
        titles.append(n.title)
    return JsonResponse(get_response_data('000000', data))
