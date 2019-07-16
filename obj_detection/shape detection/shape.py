import numpy as np
from PIL import Image


def standard_deviation(values, ma):
    n = len(values)
    dif = np.array(list(map(lambda x: (((x - ma))**2 / n), values)))
    return np.sqrt(np.sum(dif))


def rgb_2_int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int


def image_2_matrix(im):
    base = np.asarray(im).reshape(400, 3)
    mapped = np.array(list(map(rgb_2_int, base))).reshape((20, 20))
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


def similarity_degree(values1, values2):
    d1 = np.average(values1)
    d2 = np.average(values2)

    print('\n[1] similarity degree: ' + str(d1))
    print('[2] similarity degree: ' + str(d2))

    return (d1 + d2) / 2


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

if degree <= 1.34:
    print('similar images')
else:
    print('non-similar images')
