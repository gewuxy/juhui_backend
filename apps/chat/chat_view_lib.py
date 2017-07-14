# -*- coding: utf8 -*-
import cv2
import subprocess
from config.settings.common import FFMPEG_BIN_PATH

# FFMPEG_BIN_PATH = '/usr/local/bin/ffmpeg'

def set_video_img(from_path, to_path):
    vc = cv2.VideoCapture(from_path)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
    if rval:
        rval, frame = vc.read()
        cv2.imwrite(to_path, frame)
    vc.release()
    return rval

def set_video_img_1(from_path, to_path):
    process = subprocess.Popen(
        [FFMPEG_BIN_PATH, '-ss', '00:00:02', '-i', from_path, '-vframes', '1', '-q:v', '2', '-f',
         'image2', 'pipe:1', to_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print('[UPLOAD] 制作截图,ret={0}, stderr={1}'.format(process.returncode, stderr))
        return False
    print('[UPLOAD] 制作截图,ret={0}, stdout={1}'.format(process.returncode, stdout))
    return True