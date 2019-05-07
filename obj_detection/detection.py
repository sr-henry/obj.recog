from math import ceil
from time import sleep
from win32api import GetAsyncKeyState, GetCursorPos, RGB
from win32gui import GetDC
from PIL import ImageGrab
from win32con import VK_HOME, VK_F4
import overlay

help = '''
[@] REAL TIME Detection 
[HOME]  Start|Stop Detection
'''

_overlay = overlay.Overlay(GetDC(0))

config = set()

fov = 30

def check_neighbors(reshape_array):
    nhsize = 5
    neighbors = 0
    for c in reshape_array:
        for x in range(c[0] - nhsize, c[1] - nhsize):
            for y in range(c[0] + nhsize, c[1] + nhsize):
                if (x, y) in reshape_array:
                    neighbors += 1
        if neighbors < nhsize**2:
            reshape_array.remove(c)
    return reshape_array


def load_config():
    try:
        with open('config.txt', 'r') as cfg:
            for data in cfg:
                config.add(int(data.strip('\n')))
            return True
    except Exception as err:
        print(err)
        return False

def rgb_2_int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int

def reshape(index):
    ncol = fov * 2
    lin = ceil(((index + 1) / ncol)) - 1
    col = ((index + 1) % ncol) - 1
    if col == -1:
        col = ncol - 1
    return col, lin

def detection(x, y):
    precision = 150
    screen = ImageGrab.grab((x - fov, y - fov, x + fov, y + fov))
    im_int = list(map(rgb_2_int, list(screen.getdata())))
    result = list(filter(lambda el: el in config, im_int))
    if len(result) >= precision:
        coords = list(map(lambda i: im_int.index(i), result))
        fov_cords = list(map(reshape, coords))
        abs_cords = list(map(lambda r: (((x - fov) + r[0]), ((y - fov) + r[1])), fov_cords))
        #Overlay
        #_overlay.create_pixelmap(abs_cords, RGB(0, 255, 0))
        list_x = list(map(lambda x: x[0], abs_cords))
        list_y = list(map(lambda y: y[1], abs_cords))
        _overlay.create_box((min(list_x), min(list_y), max(list_x), max(list_y)), RGB(255, 0, 0))


print(help)

tracking = False
if load_config():
    while True:
        if GetAsyncKeyState(VK_HOME):
            if tracking:
                tracking = False
                print('[-] NO Tracking')
            else:
                tracking = True
                print('[!] Tracking')
            sleep(.2)

        if tracking:
            current_x, current_y = GetCursorPos()
            detection(current_x, current_y)

        if GetAsyncKeyState(VK_F4):
            break

        sleep(.1)
