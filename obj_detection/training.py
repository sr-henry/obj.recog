import numpy as np
from PIL import ImageGrab
from time import sleep
import win32con
import win32api
import win32gui
import overlay

_help = '''
    [HOME]      Start|Stop Training
    [INSERT]    Add to white set
    [DELETE]    Add to black set 
    [END]       Exit
'''

_overlay = overlay.Overlay(win32gui.GetDC(0))

fov = 20
confidence = 120

white = np.array([], dtype=int)
black = np.array([], dtype=int)


def load_config(file_name):
    np.append(white, np.loadtxt(file_name, dtype=int, delimiter='\n'))


def save_config(file_name):
    config = np.delete(white, np.where(np.isin(white, black)))
    np.savetxt(file_name, config, fmt='%d', delimiter='\n')


def rgb2int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int


def training(x, y):
    global white
    global black
    field_of_view = (x - fov, y - fov, x + fov, y + fov)
    _overlay.create_box(field_of_view, win32api.RGB(255, 0, 0))
    screen_shot = ImageGrab.grab(field_of_view)
    image = np.asarray(screen_shot).reshape((fov*2)**2, 3)
    mapped = np.array(list(map(rgb2int, image)))
    config = np.delete(white, np.where(np.isin(white, black)))
    result = mapped[np.where(np.isin(mapped, config))]
    if result.size >= confidence:
        _overlay.create_box(field_of_view, win32api.RGB(0, 255, 0))
        if win32api.GetAsyncKeyState(win32con.VK_DELETE):
            black = np.unique(np.append(black, mapped))
    if win32api.GetAsyncKeyState(win32con.VK_INSERT):
        white = np.unique(np.append(white, mapped))


print(_help)

is_on = False

while True:
    if win32api.GetAsyncKeyState(win32con.VK_HOME):
        if is_on:
            is_on = False
            print('[-] Stop')
        else:
            is_on = True
            print('[+] Start')
        sleep(.2)

    if win32api.GetAsyncKeyState(win32con.VK_END):
        save_config('teste.txt')
        break

    if is_on:
        cx, cy = win32api.GetCursorPos()
        training(cx, cy)
    sleep(.1)
