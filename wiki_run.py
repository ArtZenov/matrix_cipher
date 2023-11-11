import numpy as np

alphEng = "abcdefghijklmnopqrstuvwxyz"
keyword = 'ASDF'
mat_size = int(len(keyword) ** 0.5)
text = 'cats'


def word_to_code(word, alph, mat_height, key_f=0):
    word_code = []
    for i in word.casefold():
        if i in alph:
            word_code.append(alph.index(i))
        else:
            # если символ отсутствует в словаре, то выводим сообщение и прекращаем работу
            print('В словаре нет такого символа:', i)
            exit()
    word_code = np.array(word_code)
    if not key_f:
        np_word_code_matx = word_code[:mat_height].reshape(mat_height, 1)
        count = 0
        for i in range(int(len(word)/mat_height)-1):
            count += 1
            np_word_code_matx = np.append(np_word_code_matx, np.array(
                word_code[mat_height*count:(mat_height*count)+mat_height]
            ).reshape(mat_height, 1), axis=1)
        word_code = np_word_code_matx
    return word_code


def code_word_f(code, alph):  # преобразуем массив чисел в массив букв по словарю
    word_code = []
    lst_alph = list(alph)
    for i in range(len(code[0])):
        for j in code[:, i]:
            word_code.append(lst_alph[int(j)])
    return word_code

def extended_gcd(a, b):  # функция расширенного алгоритма Евклида
    # на вход подаём определитель матрицы ключа и длину алфавита
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y


def propper_matrix(unproptext, mat_size):  # Добавляем пустые ячейки в массив текста для создания
    while len(unproptext) % mat_size != 0:  # квадратной матрицы
        unproptext += ' '
    return unproptext


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

    return np.array(transposed_matrix)


def shifr(alph, main_text, keyword, mat_size):
    keyword_check = (len(keyword) ** 0.5) % 1  # проверяем длинну ключа на возможность
    # формирования квадратной матрицы
    if keyword_check == 0:
        print('Ключевое слово подходит по размеру.')
    else:
        print('Используйте другое слово, с нужной размерностью.')
        exit()

    keyword_matrix = word_to_code(keyword, alph, mat_size, 1).reshape(mat_size, mat_size)
    corrected_text = propper_matrix(text, mat_size)
    text_matrix = (
        word_to_code(corrected_text, alph, mat_size)
        .reshape(mat_size, int(len(corrected_text) / mat_size))
    )
    shifr_code = (keyword_matrix.dot(text_matrix)) % len(alph)
    shifr_as_txt = ''.join(code_word_f(shifr_code, alph)).upper()
    print(shifr_code)
    print(shifr_as_txt)
    return shifr_as_txt, keyword_matrix, shifr_code


def deshifr(alph, keyword_mat, shifr_as_txt):
    shifr_matrix = (
        word_to_code(shifr_as_txt, alph, mat_size)
        .reshape(mat_size, int(len(shifr_as_txt) / mat_size))
    )
    det_kw_mx = np.linalg.det(keyword_mat)
    if det_kw_mx == 0:
        print('Нулевой определитель матрицы. Продолжение невозможно. Программа закрывается.')
        exit()
    x = np.ndarray.tolist(keyword_mat)
    inverce_kw_mx = (
            np.array(transpose_matrix(np.ndarray.tolist(keyword_mat)) / (1.0 / (det_kw_mx % len(alph)))) % len(alph)
    )
    print(shifr_matrix)
    deshifr_matxx = (inverce_kw_mx.dot(shifr_matrix)) % len(alph)
    desh_text = ''.join(code_word_f(deshifr_matxx, alph))
    print(deshifr_matxx)
    print(desh_text)


sh, keyword_mat, shifr_code = shifr(alphEng, text, keyword, mat_size)

deshifr(alphEng, keyword_mat, sh)
