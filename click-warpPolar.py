#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import math
import argparse
from collections import deque

import cv2 as cv
import numpy as np

from utils import CvFpsCalc


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--file", type=str, default=None)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--warp_polar_width", type=int, default=500)
    parser.add_argument("--warp_polar_height", type=int, default=150)
    parser.add_argument("--initial_angle", type=int, default=-90)

    args = parser.parse_args()

    return args


def mouse_callback(event, x, y, flags, param):
    global click_points
    if event == cv.EVENT_LBUTTONDOWN:
        click_points.append([x, y])


def calc_circle_info(point01, point02, point03):
    x1 = point01[0]
    y1 = point01[1]
    x2 = point02[0]
    y2 = point02[1]
    x3 = point03[0]
    y3 = point03[1]

    d = 2 * ((y1 - y3) * (x1 - x2) - (y1 - y2) * (x1 - x3))
    x = ((y1 - y3) * (y1**2 - y2**2 + x1**2 - x2**2) - (y1 - y2) *
         (y1**2 - y3**2 + x1**2 - x3**2)) / d
    y = ((x1 - x3) * (x1**2 - x2**2 + y1**2 - y2**2) - (x1 - x2) *
         (x1**2 - x3**2 + y1**2 - y3**2)) / -d
    r = math.sqrt((x - x1)**2 + (y - y1)**2)

    return x, y, r


def exec_warp_polar(
    image,
    points,
    initial_angle,
    warp_polar_width,
    warp_polar_height,
):
    x, y, r = calc_circle_info(points[0], points[1], points[2])

    lin_polar_image = cv.warpPolar(
        image, (warp_polar_height, warp_polar_width), (int(x), int(y)), int(r),
        cv.INTER_CUBIC + cv.WARP_FILL_OUTLIERS + cv.WARP_POLAR_LINEAR)

    lin_polar_image = cv.rotate(lin_polar_image, cv.ROTATE_90_COUNTERCLOCKWISE)

    scroll_x = int(lin_polar_image.shape[1] * (-1) * (initial_angle / 360))
    lin_polar_image = np.roll(lin_polar_image, scroll_x, axis=1)

    return lin_polar_image, x, y, r


def main():
    global click_points

    # コマンドライン引数
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    filepath = args.file

    warp_polar_width = args.warp_polar_width
    warp_polar_height = args.warp_polar_height

    initial_angle = args.initial_angle

    # GUI準備
    window_name = 'Click warpPolar'
    cv.namedWindow(window_name)
    cv.setMouseCallback(window_name, mouse_callback)

    # カメラ準備
    cap = None
    if filepath is None:
        cap = cv.VideoCapture(cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
    else:
        cap = cv.VideoCapture(filepath)

    # 対象座標 格納用
    click_points = deque(maxlen=3)

    # FPS計測モジュール
    cvFpsCalc = CvFpsCalc(buffer_len=10)

    while True:
        # キー入力(ESC:プログラム終了)
        key = cv.waitKey(int(1000 / 30))
        if key == 27:  # ESC
            break

        # FPS計測
        display_fps = cvFpsCalc.get()

        # カメラキャプチャ
        ret, frame = cap.read()
        if not ret:
            print('Error : cap.read()')
        if filepath is None:
            resize_frame = cv.resize(frame, (int(cap_width), int(cap_height)))
        else:
            resize_frame = copy.deepcopy(frame)

        # 極座標変換
        lin_polar_image = None
        if len(click_points) == 3:
            lin_polar_image, x, y, r = exec_warp_polar(
                resize_frame,
                click_points,
                initial_angle,
                warp_polar_width,
                warp_polar_height,
            )

        # デバッグ情報描画
        for click_point in click_points:
            cv.circle(resize_frame, (click_point[0], click_point[1]),
                      5, (0, 255, 0),
                      thickness=-1)
        if len(click_points) == 3:
            cv.circle(resize_frame, (int(x), int(y)),
                      int(r), (0, 255, 0),
                      thickness=2)
        cv.putText(resize_frame, "FPS:" + str(display_fps), (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv.LINE_AA)

        # 描画更新
        cv.imshow(window_name, resize_frame)
        if lin_polar_image is not None:
            cv.imshow('warpPolar', lin_polar_image)

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
