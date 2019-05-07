import win32api
import win32con
import win32gui
from PIL import ImageGrab
from time import sleep
from math import ceil

help = ''' 
[@] REAL TIME Training 
[HOME]   Start|Stop Training
[INS]    Add color to set    (Only to not detection)
[DEL]    Rmv color from set  (Only to wrong detection)
[END]    Save configuration  (if not detecting)
'''

dc = win32gui.GetDC(0)

white = set()
black = set()

fov = 25

def show_fov(x, y, fov_color):
    try:
        for j in range(x - fov, x + fov):
            win32gui.SetPixel(dc, j, y - fov, fov_color)
        for i in range(y - fov, y + fov):
            win32gui.SetPixel(dc, x - fov, i, fov_color)
            win32gui.SetPixel(dc, x + fov, i, fov_color)
        for k in range(x - fov, x + fov):
            win32gui.SetPixel(dc, k, y + fov, fov_color)
    except Exception as err:
        print(err)

def reshape(index):
    ncol = fov * 2
    lin = ceil(((index + 1) / ncol)) - 1
    col = ((index + 1) % ncol) - 1
    if col == -1:
        col = ncol - 1
    return col, lin

def save_config():
    with open('config.txt', 'w') as cfg:
        config = list(map(lambda x: x not in black, white))
        for data in config:
            cfg.write(str(data) + '\n')


def load_config():
    try:
        with open('config.txt', 'r') as cfg:
            for data in cfg:
                white.add(int(data.strip('\n')))
    except Exception as err:
        print(err)


def rgb_2_int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int


def training_data(x, y):
    precision = 250
    confidence = 0
    screen = ImageGrab.grab((x - fov, y - fov, x + fov, y + fov))
    im_int = list(map(rgb_2_int, list(screen.getdata())))
    for color in im_int:
        if color in white and color not in black:
            confidence += 1
        if confidence >= precision:
            show_fov(x, y, win32api.RGB(255, 0, 0))
            l,c = reshape(im_int.index(color))
            win32gui.SetPixel(dc, x - fov + c, y - fov + l, win32api.RGB(255, 0, 0))
            if win32api.GetAsyncKeyState(win32con.VK_DELETE):
                black.add(color)
        elif win32api.GetAsyncKeyState(win32con.VK_INSERT):
            white.add(color)

def init():

    print(help)

    load_config()

    detection = False
    while True:

        if win32api.GetAsyncKeyState(win32con.VK_HOME):
            if detection:
                detection = False
                print('[-] Detection Stop')
            else:
                detection = True
                print('[+] Start Detection')
            sleep(.2)

        if win32api.GetAsyncKeyState(win32con.VK_END):
            save_config()
            print('[:] Configuration Saved')
            sleep(.2)

        if detection:
            x, y = win32api.GetCursorPos()
            training_data(x, y)


init()
