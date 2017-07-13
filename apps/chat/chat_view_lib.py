# -*- coding: utf8 -*-
import cv2


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

