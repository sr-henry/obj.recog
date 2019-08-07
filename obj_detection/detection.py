import time
import win32api
from win32gui import GetDC
from PIL import ImageGrab
import numpy as np
import overlay


def filter_detection_result(matrix, result):
    mask = np.isin(matrix, result)
    detection_matrix = np.zeros(matrix.shape, dtype=int)
    np.place(detection_matrix, mask, result)
    return detection_matrix


def rgb_2_int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int


def img_2_matrix(img):
    rgb_matrix = np.asarray(img).reshape((radius * 2) ** 2, 3)
    int_matrix = np.array(list(map(rgb_2_int, rgb_matrix)))
    return int_matrix.reshape((radius * 2), (radius * 2))


def detection(field_of_view):
    matrix = img_2_matrix(ImageGrab.grab(field_of_view))
    result = np.asarray(np.intersect1d(matrix, config))
    if result.size >= 120:
        detected_matrix = filter_detection_result(matrix, result)
        i, j = np.where(detected_matrix != 0)
        print(i)
        _overlay.create_box(fov, win32api.RGB(255, 0, 0))


_overlay = overlay.Overlay(GetDC(0))

radius = 20

try:
    config = np.loadtxt('config.txt', dtype=int, delimiter='\n')
    print('[+] loaded')
except Exception as err:
    print(err)

while True:
    x, y = win32api.GetCursorPos()
    fov = (x - radius, y - radius, x + radius, y + radius)
    detection(fov)
    time.sleep(.15)
