from time import sleep
import win32api
import win32con
import win32gui
from PIL import ImageGrab
import overlay

_help = '''
    [HOME]      Start|Stop Training
    [INSERT]    Add to white set
    [DELETE]    Add to black set 
    [END]       Exit
'''

white = set()
black = set()

_overlay = overlay.Overlay(win32gui.GetDC(0))

fov = 20
confidence = 120


def rgb2int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int


def training(x, y, fx, fy):
    _overlay.create_box((x - fx, y - fy, x + fx, y + fy), win32api.RGB(255, 0, 0))
    result = 0
    screen_shot = ImageGrab.grab((x - fx, y - fy, x + fx, y + fy))
    image = list(screen_shot.getdata())
    mapped = list(map(rgb2int, image))

    for px in mapped:
        if px in white and px not in black:
            result += 1
    
    if result >= confidence:
        _overlay.create_box((x - fx, y - fy, x + fx, y + fy), win32api.RGB(0, 255, 0))
        if win32api.GetAsyncKeyState(win32con.VK_DELETE):
            black.update(mapped)
    elif win32api.GetAsyncKeyState(win32con.VK_INSERT):
        white.update(mapped)


print(_help)

is_on = False

FX = 20
FY = 20

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
        break

    if win32api.GetAsyncKeyState(win32con.VK_UP):
        FY += 2
    if win32api.GetAsyncKeyState(win32con.VK_DOWN):
        FY -= 2
    if win32api.GetAsyncKeyState(win32con.VK_RIGHT):
        FX += 2
    if win32api.GetAsyncKeyState(win32con.VK_LEFT):
        FX -= 2

    if is_on:
        cx, cy = win32api.GetCursorPos()
        training(cx, cy, FX, FY)
    sleep(.1)
