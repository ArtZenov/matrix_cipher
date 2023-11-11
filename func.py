import numpy as np


def word_code_f(word, alph):  # преобразуем стоку в массив чисел по словарю
    word_code = []
    for i in word.casefold():
        if i in alph:
            word_code.append(alph.index(i))
        else:
            # если символ отсутствует в словаре, то выводим сообщение и прекращаем работу
            print('В основном тексте нет такого символа:', i)
            exit()
    return word_code


def code_word_f(code, alph):  # преобразуем массив чисел в массив букв по словарю
    word_code = []
    lst_alph = list(alph)
    for i in code:  # замена пробелов на нижнее подчёркивание для визуализации вывода
        i = int(i)
        if lst_alph[i] == ' ':
            lst_alph[i] = '_'
        word_code.append(lst_alph[i])
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


def find_cofactor_matrix(matrix):  # находим матрицу алгебраических дополнений
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    cofactor_matrix = []
    for i in range(num_rows):
        cofactor_row = []
        for j in range(num_cols):
            minor = [[matrix[row][col] for col in range(num_cols) if col != j] for row in range(num_rows) if row != i]
            minor_det = np.linalg.det(np.array(minor))
            cofactor = (-1) ** (i + j) * minor_det
            cofactor_row.append(round(cofactor))
        cofactor_matrix.append(cofactor_row)
    return cofactor_matrix


def divide_matrix(matrix, divisor):
    # делим матрицу по модулю на число, без потери минусов при делении
    result = []
    for row in matrix:
        new_row = [value % divisor if value >= 0 else -(-value % divisor) for value in row]
        result.append(new_row)
    return result


# функция зашифровки
def main_scypher(alph, text, keyword, mat_size):
    keyword_limit = [4, 9, 16, 25]  # проверяем длинну ключа на возможность
    # формирования квадратной матрицы
    shifr = ''
    if int(len(keyword)) in keyword_limit:
        print('Ключевое слово подходит по размеру.')
    else:
        print('Используйте другое слово, с нужной размерностью.')
        exit()
    # фрмируем матрицу ключа и матрицу основного текста
    keyword_matrix = np.array(word_code_f(keyword, alph)).reshape(mat_size, mat_size)
    text_matrix = (np.array(word_code_f(propper_matrix(text, mat_size), alph))
                   .reshape(int(len(propper_matrix(text, mat_size)) / mat_size), mat_size))
    # подставляем элементам полученной матрицы значения букв алфавита
    # и соединяем их в строку
    for i in range(len(text_matrix)):
        shifr += ''.join(code_word_f(text_matrix[int(i)].dot(keyword_matrix) % len(alph), alph)).upper()
    return shifr


# функция дешифровки
def main_descypher(alph, shifr, keyword, mat_size):
    deshifr = ''
    rev_det_kw_mx = 0
    keyword_matrix = np.array(word_code_f(keyword, alph)).reshape(mat_size, mat_size)
    shifr_matrix = (np.array(word_code_f(propper_matrix(shifr, mat_size), alph))
                    .reshape(int(len(propper_matrix(shifr, mat_size)) / mat_size), mat_size))
    det_kw_mx = np.linalg.det(keyword_matrix)
    d, x, y = extended_gcd(det_kw_mx, len(alph))
    # находим обратный детерминанту элемент в кольце по модулю len(alph)
    if det_kw_mx < 0 < x or det_kw_mx > 0 < x:
        rev_det_kw_mx = x
    elif det_kw_mx > 0 > x:
        rev_det_kw_mx = len(alph) + x
    elif det_kw_mx < 0 > x:
        rev_det_kw_mx = -x
    # Находим матрицу обратную матрице ключа по модулю len(alph)
    # 1) Находим матрицу алгебраических дополнений
    # 2) Делим полученную матрицу по модулю на 37
    # 3) Умножаем матрицу алгебраических дополнений на обратный детерминанту элемент
    # 4) Делим матрицу по модулю len(alph)
    # 5) Транспонируем её
    # 6) Меняем отрицательные элементы матрицы по формуле len(alph)+(элемент)
    x1 = np.array(divide_matrix(find_cofactor_matrix(keyword_matrix), len(alph))) * rev_det_kw_mx
    x2 = np.array(divide_matrix(x1, len(alph))).transpose()
    for i in range(len(x2)):
        for j in range(len(x2[0])):
            if x2[i, j] < 0:
                x2[i, j] = len(alph) + x2[i, j]
    # подставляем элементам полученной матрицы значения букв алфавита
    # и соединяем их в строку
    for i in range(len(shifr_matrix)):
        deshifr += ''.join(code_word_f(shifr_matrix[int(i)].dot(x2) % len(alph), alph)).upper()
    return deshifr
