import time
import numpy as np
from PIL import Image
import sys


def compare_imgs(i1, i2, hausdorff = False):
    coords1 = get_coords(i1)
    coords2 = get_coords(i2)
    distances_1 = compute_distance(coords1, coords2)
    distances_2 = compute_distance(coords2, coords1)
    degree = similarity_degree(distances_1, distances_2)
    if hausdorff:
        H = max(max(distances_1), max(distances_2))
        return degree, H
    return degree


def funct(im, imgs):
    return np.array(list(map(lambda m: compare_imgs(im, m), imgs)))


def compare_sub(matrix1, matrix2):
    section = 2
    f_imgs1 = get_sub_imgs(matrix1, section)
    f_imgs2 = get_sub_imgs(matrix2, section)
    return np.array(list(map(lambda img: funct(img, f_imgs2), f_imgs1)))


def get_sub_imgs(matrix, section):
    lines = np.split(matrix, section)
    split_imgs = np.array(list(map(lambda lin: np.split(lin, section, 1), lines)))
    imgs = np.concatenate(split_imgs)
    f_imgs = list(filter(lambda x: x[np.where(x == 0)].size > 0, imgs))
    return f_imgs


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
    euclidean_distance = np.linalg.norm((array - point), axis=1)
    return np.ndarray.min(euclidean_distance)


def compute_distance(c1, c2):
    return np.array(list(map(lambda point: distance(c2, point), c1)))


def similarity_degree(values1, values2):
    d1 = np.average(values1)
    d2 = np.average(values2)
    std1 = np.std(values1)
    std2 = np.std(values2)
    print('\n[1] M(A, B): ' + str(d1) + '\tstd: ' + str(std1))
    print('[2] M(B, A): ' + str(d2) + '\tstd: ' + str(std2))
    return np.average([d1, d2])


img_name = sys.argv[1]

start = time.time()

matrix_base = image_2_matrix(Image.open("base.png"))
matrix_cptr = image_2_matrix(Image.open(img_name))


# ======================================================================
dist_matrix = compare_sub(matrix_base, matrix_cptr)
print('\n' + str(dist_matrix) + '\n')

minimum = np.array(list(map(lambda el: np.ndarray.min(el), dist_matrix)))
#minimum = list(filter(lambda x: x <= 1.35, minimum))
print('minimum per line:' + str(minimum))
diagonal = dist_matrix.diagonal()
print('diagonal: ' + str(diagonal))

print('\ndiagonal_mean: ' + str(np.average(diagonal)))

print('____________________________________________________')
# ======================================================================


degree, H = compare_imgs(matrix_base, matrix_cptr, True)

print('\naverage: ' + str(degree) + '\n')

print('hausdorff: ' + str(H) + '\n')

if degree <= 1.35 and H <= 4:
    print('similar images')
else:
    print('non-similar images')


end = time.time()

print('\ntime: ' + str(end - start))
