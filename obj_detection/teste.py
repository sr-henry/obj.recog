import numpy as np


def draw_line(mat, p0, p1):
    if p0 == p1:
        return mat
    transpose = abs(p1[0] - p0[0]) < abs(p1[1] - p0[1])
    if transpose:
        mat = mat.T
        p0, p1 = p0[::-1], p1[::-1]
    if p0[0] > p1[0]:
        p0, p1 = p1, p0
    x = np.arange(p0[0] + 1, p1[0])
    y = np.round(((p1[1] - p0[1]) / (p1[0] - p0[0])) * (x - p0[0]) + p0[1]).astype(x.dtype)
    mat[x, y] = 1
    return mat if not transpose else mat.T


print(draw_line(np.zeros((5, 5)), (4, 2), (0, 3)))

