from re import findall
import tkinter as tk
import pyperclip

alpha = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890")
MatrixLength = 3
MatrixMod = len(alpha)
MatrixSquare = MatrixLength * MatrixLength

def checkErrors(key):
    if len(key) != MatrixSquare:
        return "Error: len(key) != %d" % MatrixSquare
    elif not getDeter(sliceto(key)):
        return "Error: det(Key) = 0"
    elif not getDeter(sliceto(key)) % MatrixMod:
        return "Error: det(Key) mod len(alpha) = 0"
    else:
        return None

def regular(text):
    template = r".{%d}" % MatrixLength
    return findall(template, text)

def encode(matrix):
    for x in range(len(matrix)):
        for y in range(MatrixLength):
            matrix[x][y] = alpha.index(matrix[x][y].upper())
    return matrix

def decode(matrixM, matrixK, message=""):
    matrixF = []
    for z in range(len(matrixM)):
        temp = [0 for _ in range(MatrixLength)]
        for x in range(MatrixLength):
            for y in range(MatrixLength):
                temp[x] += matrixK[x][y] * matrixM[z][y]
            temp[x] = alpha[temp[x] % MatrixMod]
        matrixF.append(temp)
    for string in matrixF:
        message += "".join(string)
    return message

def sliceto(text):
    matrix = []
    for three in regular(text):
        matrix.append(list(three))
    return encode(matrix)

def iDet(det):
    for num in range(MatrixMod):
        if num * det % MatrixMod == 1:
            return num

def algebratic(x, y, det, key):
    matrix = sliceto(key)
    matrix.remove(matrix[x])
    for z in range(2):
        matrix[z].remove(matrix[z][y])
    det2x2 = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return (pow(-1, x + y) * det2x2 * iDet(det)) % MatrixMod

def getDeter(matrix):
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[1][0] * matrix[2][1] * matrix[0][2]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[1][2] * matrix[2][1] * matrix[0][0]
    )

def getAlgbr(det, key):
    algbrs = [0 for _ in range(MatrixSquare)]
    index = 0  # Инициализируем index перед циклом
    for string in range(MatrixLength):
        for column in range(MatrixLength):
            algbrs[index] = algebratic(string, column, det, key)  # Передать ключ в algebratic
            index += 1
    return algbrs


def getIMatr(algbr):
    return [
        [algbr[0], algbr[3], algbr[6]],
        [algbr[1], algbr[4], algbr[7]],
        [algbr[2], algbr[5], algbr[8]]
    ]

def encryptDecrypt(mode, message, key):
    MatrixMessage, MatrixKey = sliceto(message), sliceto(key)
    if mode == 'E':
        final = decode(MatrixMessage, MatrixKey)
    else:
        algbr = getAlgbr(getDeter(MatrixKey), key)
        final = decode(MatrixMessage, getIMatr(algbr))
    return final

def on_encrypt():
    startMessage = input_message.get().upper()
    key_value = key.get().upper()  # Получить значение ключа из виджета
    if checkErrors(key_value):
        output_message.set(checkErrors(key_value))
    else:
        for symbol in startMessage:
            if symbol not in alpha:
                startMessage = startMessage.replace(symbol, '')
        while len(startMessage) % MatrixLength != 0:
            startMessage += startMessage[-1]
        result = encryptDecrypt('E', startMessage, key_value)  # Передать ключ напрямую
        output_message.set(result)

def on_decrypt():
    startMessage = input_message.get().upper()
    key_value = key.get().upper()  # Получить значение ключа из виджета
    if checkErrors(key_value):
        output_message.set(checkErrors(key_value))
    else:
        for symbol in startMessage:
            if symbol not in alpha:
                startMessage = startMessage.replace(symbol, '')
        while len(startMessage) % MatrixLength != 0:
            startMessage += startMessage[-1]
        result = encryptDecrypt('D', startMessage, key_value)  # Передать ключ напрямую
        output_message.set(result)

def on_copy():
    result = output_message.get()
    pyperclip.copy(result)


root = tk.Tk()
root.title("Matrix Cipher")

frame = tk.Frame(root, padx=10, pady=10)  # Добавляем отступы
frame.pack(pady=20)

input_label = tk.Label(frame, text="Message:")
input_label.pack()

input_message = tk.StringVar()
input_entry = tk.Entry(frame, textvariable=input_message)
input_entry.pack()

key_label = tk.Label(frame, text="Key:")
key_label.pack()

key = tk.StringVar()
key.set("SECRETKEY")
key_entry = tk.Entry(frame, textvariable=key)
key_entry.pack()

encrypt_button = tk.Button(frame, text="Encrypt", command=on_encrypt)
encrypt_button.pack()

decrypt_button = tk.Button(frame, text="Decrypt", command=on_decrypt)
decrypt_button.pack()

copy_button = tk.Button(frame, text="Copy Result", command=on_copy)
copy_button.pack()

output_message = tk.StringVar()
output_label = tk.Label(frame, textvariable=output_message)
output_label.pack()

root.mainloop()