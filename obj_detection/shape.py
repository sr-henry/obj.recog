from math import sqrt
from PIL import Image
import numpy as np
from statistics import mean

def image_2_matrix(im):
    base = np.asarray(im).reshape((20)**2, 3)
    mapped = np.array(list(map(rgb2int, base))).reshape((20, 20))
    return mapped


def rgb2int(rgb):
    rgb_int = rgb[0]
    rgb_int = (rgb_int << 8) + rgb[1]
    rgb_int = (rgb_int << 8) + rgb[2]
    return rgb_int 


def gambiarra(m_list):
    n_list = []
    for el in m_list:
        n_list.append((el[0], el[1]))
    return n_list


def get_cords(matrix):
    x, y = np.where(matrix == 0)
    coords = np.hstack((x.reshape(x.size, 1), y.reshape(y.size, 1)))
    return gambiarra(coords.tolist())


def euclidean_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return sqrt(dx**2 + dy**2)


def compute_distance(c1, c2):
    distances = dict()
    minimum = dict()

    for i in c1:
        for j in c2:
            distances[(i, j)] = euclidean_distance(i, j)
            # print('(' + str(i) + ', ' + str(j) + ') : ' + str(euclidean_distance(i, j)))
        for key, value in distances.items():
            if value == min(distances.values()):
                # print('\n#' + str(key) + ' : ' + str(value))
                minimum[key] = value
                break
        distances.clear()
        # print('=========================')
    return minimum


def check_similarity(values, key_points):
    similarity_points = (key_points/2) + (key_points/4)
    perimeter = 2

    print('\nminimum similarity points : ' + str(similarity_points))

    n_points = 0

    for x in values:
        if x <= perimeter:
            n_points += 1

    print('matching points : ' + str(n_points))


def similarity_degree(values1, values2):
    d1 = mean(values1)
    d2 = mean(values2)

    print('\n[1] similarity degree: ' + str(d1))
    print('[2] similarity degree: ' + str(d2))

    return (d1 + d2) / 2 


base = image_2_matrix(Image.open("base.png"))
cptr = image_2_matrix(Image.open("erro.png"))

base_coords = get_cords(base)
cptr_coords = get_cords(cptr)

distances_1 = compute_distance(base_coords, cptr_coords)

distances_2 = compute_distance(cptr_coords, base_coords)

degree = similarity_degree(distances_1.values(), distances_2.values())

print('\naverage: ' + str(degree))

check_similarity(distances_1.values(), len(base_coords))

