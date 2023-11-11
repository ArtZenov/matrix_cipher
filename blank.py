import numpy as np


def transpose_matrix(matrix):
    # Функция для вычисления алгебраических дополнений
    def cofactor(matrix, i, j):
        submatrix = [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]
        sign = (-1) ** (i + j)
        return determinant(submatrix) * sign

    # Функция для вычисления определителя матрицы
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for j in range(len(matrix[0])):
                det += matrix[0][j] * cofactor(matrix, 0, j)
            return det

    n = len(matrix)
    transposed_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            transposed_matrix[j][i] = cofactor(matrix, i, j)

    return transposed_matrix


a = np.array([[0, 2], [1, 0], [1, 1]])  # матрица текста
b = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])  # матрица ключа
# c = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
# d = np.array([[0], [2], [19]])
# a = d
# b = c

mod_size = 26
shifr_mat = b.dot(a) % mod_size

det_key = round(np.linalg.det(b))
transpose_key = np.array(transpose_matrix(np.ndarray.tolist(b))) % mod_size
part = (1.0 / (det_key % mod_size))
invar_key = transpose_key * part
text_matrix = (invar_key.dot(shifr_mat)) % mod_size
print('end')


detC = np.linalg.det(np.array(c))
print(detC % 26)

c = np.array(c)
print(c[:, [0]])

c = np.ndarray.tolist(c)

k = np.array(transpose_matrix(c)) / (1.0 / (detC % 26)) % 26
print(k, '\n')

print((k.dot(np.array(d))) % 26)


d = [1, 2, 3, 4, 5, 6]  # [[1, 4], [2, 5], [3, 6]]

# d = np.array(d[:3]).reshape(3, 1)
d = np.append(np.array(d[:3]).reshape(3, 1), np.array(d[3:]).reshape(3, 1), axis=1)
print(d)
