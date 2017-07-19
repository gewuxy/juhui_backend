# -*- coding: utf8 -*-
import subprocess
from config.settings.common import FFMPEG_BIN_PATH
import os

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