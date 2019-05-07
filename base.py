import time
import win32api
import win32con
import win32gui
from PIL import ImageGrab
from math import ceil

dc = win32gui.GetDC(0)

tracking = False

print('[@] Aimbot PXC')

blacklist = {1052688, 10329501, 2829099, 6973536, 3948353, 790287, 790544, 1844270, 1844010, 11974326}
data = set()

def show_enemy(cords):
    for cord in cords:
        win32gui.SetPixel(dc, cord[0], cord[1], win32api.RGB(255, 0, 255))

def reshape(index):
    ncol = fov * 2
    lin = (ceil((((index + 1) / ncol)))) - 1
    col = ((index + 1) % ncol) - 1
    if col == -1:
        col = ncol - 1
    return col, lin


def loadConfig():
    file_whitelist = open('whitelist.txt', 'r')
    file_blacklist = open('blacklist.txt', 'r')
    for line in file_whitelist:
        data.add(int(line.strip('\n')))
    for line in file_blacklist:
        blacklist.add(int(line.strip('\n')))
    file_blacklist.close()
    file_whitelist.close()
    print('Loaded!')

def saveConfig():
    file_whitelist = open('whitelist.txt', 'w')
    file_blacklist = open('blacklist.txt', 'w')

    for x in data:
        file_whitelist.write(str(x) + '\n')
    for y in blacklist:
        file_blacklist.write(str(y) + '\n')

    file_blacklist.close()
    file_whitelist.close()

def rgb_2_int(rgb):
    RGBint = rgb[0]
    RGBint = (RGBint << 8) + rgb[1]
    RGBint = (RGBint << 8) + rgb[2]
    return RGBint

def newSearchColor(x, y, fov):
    precision = 120
    screen = ImageGrab.grab((x - fov, y - fov, x + fov, y + fov))
    im_int = list(map(rgb_2_int, list(screen.getdata())))
    result = list(filter(lambda x: x in data and x not in blacklist, im_int))
    if len(result) >= precision:
        coords = list(map(lambda x: im_int.index(x), result))
        fov_cords = list(map(reshape, coords))
        abs_cords = list(map(lambda r: (((x - fov) + r[0]), ((y - fov) + r[1])), fov_cords))
        show_enemy(abs_cords)

def trainingData(x, y, fov):
    precision = 250 #(145*fov)/25
    screen = ImageGrab.grab((x - fov, y - fov, x + fov, y + fov))
    im = list(screen.getdata())
    confidence = 0
    for l in im:
        intcolor = rgb_2_int(l)
        if intcolor in data and intcolor not in blacklist :
            confidence += 1
        if confidence >= precision:
            if (win32api.GetAsyncKeyState(win32con.VK_DELETE)):
                blacklist.add(intcolor)
        elif (win32api.GetAsyncKeyState(win32con.VK_INSERT)):
            data.add(intcolor)

loadConfig()
fov = 25
print('WDataSize\t'+ str(len(data)) + '\nBDataSize\t' + str(len(blacklist)) + '\nFOV\t' + str(fov) + '\nPrecision\t145')

while True:

    if (win32api.GetAsyncKeyState(win32con.VK_F4)):
        saveConfig()
        print('Save!')

    if (win32api.GetAsyncKeyState(win32con.VK_HOME)):
        time.sleep(0.2)
        if (tracking):
            tracking = False
            print('[-] NO Tracking')
        else:
            tracking = True
            print('[!] Tracking')

    if (tracking):
        x, y = win32api.GetCursorPos()
        #trainingData(x, y, fov)
        newSearchColor(x, y, fov)

    time.sleep(.1)