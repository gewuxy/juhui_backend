# -*- coding: utf8 -*-
import subprocess
from config.settings.common import FFMPEG_BIN_PATH
import os
from apps.account.models import Jh_User
import redis
from django.http import JsonResponse
from apps import get_response_data

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=1)
# FFMPEG_BIN_PATH = '/usr/local/bin/ffmpeg'

def set_video_img_1(from_path, to_path):
    process = subprocess.Popen(
        [FFMPEG_BIN_PATH, '-ss', '00:00:02', '-i', from_path, '-vframes', '1', '-q:v', '2', '-f',
         'image2', 'pipe:1', to_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if os.path.exists(to_path):
        return True
    else:
        return False


# 自选信息初始化接口
def first_set_select_redis(request):
    select_data = {}
    for user in Jh_User.objects.all():
        codes = user.personal_select
        if not codes:
            continue
        for code in codes.split(';'):
            if select_data.get(code):
                select_data[code] += 1
            else:
                select_data[code] = 1
    for key, val in select_data.items():
        select_key = 'juhui_chat_select_' + key
        REDIS_CLIENT.set(select_key, val)
    return JsonResponse(get_response_data('000000'))