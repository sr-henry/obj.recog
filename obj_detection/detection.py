import numpy as np
from win32api import GetCursorPos, RGB, GetAsyncKeyState
from PIL import ImageGrab
from time import sleep
import overlay
from win32gui import GetDC
import win32con

_overlay = overlay.Overlay(GetDC(0))

fov = 20
confidence = 120


def have_neighbors(matrix, point):
    nhs = 5
    x0, y0 = (point[0]-nhs, point[1]-nhs)
    x1, y1 = (point[0]+nhs, point[1]+nhs)
    neighbor_hood = matrix[x0:x1+1, y0:y1+1]
    result = np.count_nonzero(neighbor_hood)
    if result < nhs*2 - 3:
        return True
    return False


def rgb2int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int


def detection(x, y, config):
    screen_shot = ImageGrab.grab((x - fov, y - fov, x + fov, y + fov))
    image = np.asarray(screen_shot).reshape((fov*2)**2, 3)
    mapped = np.array(list(map(rgb2int, image))).reshape((fov * 2), (fov * 2))
    result = np.asarray(np.intersect1d(mapped, config))
    if result.size >= confidence:
        mask = np.isin(mapped, result)
        _x, _y = np.where(mask)
        coords = np.hstack((_y.reshape(_y.size, 1), _x.reshape(_x.size, 1)))
        zeros = np.zeros(mapped.shape, dtype=int)
        np.place(zeros, mask, result)

        filter_coords = np.array(list(filter(lambda k: have_neighbors(zeros, k), coords)))

        # OVERLAY
        p1 = np.amin(filter_coords, axis=0)
        p2 = np.amax(filter_coords, axis=0)
        box = (p1[0]+(x - fov), p1[1]+(y - fov), p2[0]+(x - fov), p2[1]+(y - fov))
        _overlay.create_box(box, RGB(255, 0, 255))


def main():
    try:
        config = np.loadtxt('config.txt', dtype=int, delimiter='\n')
        print('Loaded')
    except Exception as err:
        print(err)
        return

    is_on = False

    while True:
        if GetAsyncKeyState(win32con.VK_HOME):
            if is_on:
                is_on = False
                print('Detection Stoped')
            else:
                is_on = True
                print('Detection Started')
            sleep(.2)

        if GetAsyncKeyState(win32con.VK_END):
            break

        if is_on:
            current_x, current_y = GetCursorPos()
            detection(current_x, current_y, config)
        sleep(.1)


main()

