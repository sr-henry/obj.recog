import numpy as np
from win32api import GetCursorPos, RGB
from PIL import ImageGrab
from time import sleep
from math import ceil
import overlay
from win32gui import GetDC

_overlay = overlay.Overlay(GetDC(0))

fov = 25

def have_neighbors(matrix, point):
    nhs = 5
    x0, y0 = (point[0]-nhs, point[1]-nhs)
    x1, y1 = (point[0]+nhs, point[1]+nhs)
    neighbor_hood = matrix[x0:x1+1, y0:y1+1]
    result = np.count_nonzero(neighbor_hood)
    if result < nhs**2:
        return False
    return True

def reshape(index):
    ncol = fov * 2
    lin = ceil(((index + 1) / ncol)) - 1
    col = ((index + 1) % ncol) - 1
    if col == -1:
        col = ncol - 1
    return col, lin

def rgb2int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int

def detection(x, y, config):
    screen_shot = ImageGrab.grab((x - fov, y - fov, x + fov, y + fov))
    image = np.asarray(screen_shot).reshape((fov*2)**2, 3)
    #?
    mapped = np.array(list(map(rgb2int, image))).reshape((fov * 2), (fov * 2))
    result = np.asarray(np.intersect1d(mapped, config))
    if result.size >= 200:
        mask = np.isin(mapped, result)
        _x, _y = np.where(mask)
        coords = np.hstack((_y.reshape(_y.size, 1), _x.reshape(_x.size, 1)))
        zeros = np.zeros(mapped.shape, dtype=int)
        np.place(zeros, mask, result)
        for c in coords:
             if not have_neighbors(zeros, c):
                 np.delete(coords, c)
        #OVERLAY
        pxmap = list(map(lambda r: (((x - fov) + r[0]), ((y - fov) + r[1])), coords.tolist()))
        _overlay.create_pixelmap(pxmap, RGB(0, 255, 0))


def main():

    try:
        config = np.loadtxt('config.txt', dtype=int, delimiter='\n')
        print('Loaded')
    except Exception as err:
        print(err)
        return

    while True:
        current_x, current_y = GetCursorPos()
        detection(current_x, current_y, config)
        sleep(.1)


main()


