from math import sqrt

base = [[1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]]


cptr = [[1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]]

'''
cptr = [[0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]
'''

def display(img):
    for l in img:
        print(l)


def get_cords(matrix):
    coords = []
    for i in range(0, 5):
        for j in range(0, 5):
            # print(matrix[i][j], end=', ')
            if matrix[i][j] == 1:
                coords.append((i, j))
    return coords

            
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
    perimeter = 1.4
    
    print(similarity_points)

    n_points = 0

    for x in values:
        if x <= perimeter:
            n_points += 1
    
    print(n_points)

    if n_points > similarity_points:
        print('YES')
    else:
        print('NO')


print('IMG_BASE')
display(base)
print('\nIMG_2_COMPARE')
display(cptr)

base_coords = get_cords(base)
cptr_coords = get_cords(cptr)

# print('\nBase coords: ' + str(base_coords))
# print('Image coords: ' + str(cptr_coords))

distances = compute_distance(base_coords, cptr_coords)

match = list(distances.values())

print('\nsimilarity degree: ' + str(abs(1 - (sum(match)/100))))

check_similarity(distances.values(), len(base_coords))
