import numpy as np
from win32api import GetCursorPos
from PIL import ImageGrab
from time import sleep

fov = 25

config = np.loadtxt('config.txt', dtype=int, delimiter='\n')

def rgb2int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int

def detection(x, y):
    screen_shot = ImageGrab.grab((x - fov, y - fov, x + fov, y + fov))
    image = np.asarray(screen_shot)
    reshape = image.reshape((fov*2)**2, 3)
    mapped = np.array(list(map(rgb2int, reshape)))
    result = np.intersect1d(mapped, config)
    if result.size >= 150:
        print('Detected')


def main():
    while True:
        current_x, current_y = GetCursorPos()
        detection(current_x, current_y)
        sleep(.1)


main()


