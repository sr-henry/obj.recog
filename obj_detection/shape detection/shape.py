import time
import numpy as np
from PIL import Image
import sys
from colorama import Fore, init, AnsiToWin32

init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream


def rgb_2_int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int


def image_2_matrix(im):
    base = np.asarray(im).reshape(400, 3)
    mapped = np.array(list(map(rgb_2_int, base))).reshape((20, 20))

    x, y = np.where(mapped == 0)

    mapped = mapped[min(x):max(x), min(y):max(y)] 

    return mapped


def get_coords(matrix):
    x, y = np.where(matrix == 0)
    coords = np.hstack((x.reshape(x.size, 1), y.reshape(y.size, 1)))
    return coords


def distance(array, point):
    diff = array - point
    dx = diff[:, 0]
    dy = diff[:, 1]
    euclidean = np.sqrt((dx**2 + dy**2))
    return min(euclidean)


def compute_distance(c1, c2):
    return np.array(list(map(lambda point: distance(c2, point), c1)))


def similarity(values1, values2):
    #print(values1)
    print(len(values1[np.where(values1 < 1.1)])) 
    #print()
    #print(values2)
    print(len(values2[np.where(values2 < 1.1)]))


def similarity_degree(values1, values2):
    d1 = np.average(values1)
    d2 = np.average(values2)
    std1 = np.std(values1)
    std2 = np.std(values2)

    print('\n[1] M(A, B): ' + str(d1) + '\tstd: ' + str(std1))
    print('[2] M(B, A): ' + str(d2) + '\tstd: ' + str(std2))

    return (d1 + d2) / 2


def hausdorff(values1, values2):
    H = max(max(values1), max(values2))
    return H


start = time.time()

im_base = Image.open("base.png")
im_cptr = Image.open("erro.png")

base = image_2_matrix(im_base)
cptr = image_2_matrix(im_cptr)

base_coords = get_coords(base)
cptr_coords = get_coords(cptr)

distances_1 = compute_distance(base_coords, cptr_coords)
distances_2 = compute_distance(cptr_coords, base_coords)

degree = similarity_degree(distances_1, distances_2)

print('\naverage: ' + str(degree))

print()

H = hausdorff(distances_1, distances_2)

print('hausdorff: ' + str(H))

print()

print((H + degree)/2)

if degree <= 1.3 and H <= 3.5:
    print(Fore.GREEN + 'similar images', file=stream)
else:
    print(Fore.RED + 'non-similar images', file=stream)

end = time.time()

print(Fore.YELLOW + '\ntime: ' + str(end - start), file=stream)

