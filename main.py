# Вариант 1. Матричный шифр
# Основной исполняемый файл
import func as sd

# Задаём переменные "словарей", ключевого слова и его матричной размерности
alphRus = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя., ?'
alphEng = "abcdefghijklmnopqrstuvwxyz"
keyword = 'альпинизм'
# keyword = 'adulthood'
mat_size = int(len(keyword) ** 0.5)


def file(textfile):  # функция чтения данных из текстовых файлов
    # (основного и зашифрованного текста)
    with open(textfile, mode='r') as f:
        text = f.read()
        if textfile == 'main_text.txt':
            text_in_work = text[19:]
        else:
            text_in_work = text[24:]
    if text_in_work[0].lower() in alphRus:  # Распознание языка основного текста или зашифрованного
        alph = alphRus
        print('Определён язык - Русский')
        return alph, text_in_work
    elif text_in_work[0].lower() in alphEng:
        alph = alphEng
        print('Определён язык - Английский')
        return alph, text_in_work


def main():  # Основная исполняемая функция
    button = input("Шифровать или расшифровать? (1/2): ")  # Выбираем, шифруем или расшифровываем
    print('Ключевое слово:', keyword)
    if button == '1':  # извлекаем основной текст и алфавит нужного языка
        alph, main_text = file('main_text.txt')
        print("Рабочий текст:\n" + main_text)
        # запускаем алгоритм шифрования из модуля func.py
        print("Зашифрованный текст:\n" + sd.main_scypher(alph, main_text, keyword, mat_size))
    elif button == '2':
        alph, shifr_text = file('shifr_text.txt')
        print("Рабочий текст:", shifr_text)
        # запускаем алгоритм дешифрования из модуля func.py
        print('Расшифрованный текст:\n' + sd.main_descypher(alph, shifr_text, keyword, mat_size))


main()
