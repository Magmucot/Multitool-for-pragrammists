from PyQt5.QtWidgets import *


def deshifrv(tekst, key, alfavit):
    result = ''
    for i, k in enumerate(tekst):
        ind = alfavit.index(k)
        ind_cur = alfavit.index(key[i % len(key)])
        y = alfavit[(ind - ind_cur) % 44]
        result += y
    return result


def shifrv(tekst, key, alfavit):
    result = ''
    for i, h in enumerate(tekst):
        ind = alfavit.index(h)
        key_ind = alfavit.index(key[i % len(key)])
        y = alfavit[(ind + key_ind) % 44]
        result += y
    return result


def deshifrc(tekst, key, alfavit):
    result = ''
    for i, k in enumerate(tekst):
        cur = alfavit.index(k)
        y = alfavit[(cur - key) % 44]
        result += y
    return result


def shifrc(tekst, key, alfavit):
    result = ''
    for i, h in enumerate(tekst):
        ind = alfavit.index(h)
        y = alfavit[(ind + key) % 44]
        result += y
    return result


def opred(text, stor, tip, key):
    alfavit = ['e', 'u', 'Z', 'з', '9', '-', '^', 'Е', 'S', '"', 'Б', 'В', 'v', 'ю', 'М', 'q', 'P', 'j', ')', 'r', ']',
               '|', '3', '.', 'ш', 'V', 'К', 'h', 'i', 'z', 'N', 'X', 'Л', 'д', '0', 'y', 'ч', 'ф', 'M', 'А', 'ж', '╕',
               'Р', 'И', '?', 'У', 'Ч', '/', 'p', '4', 'n', 'w', '&', "'", 'З', 'Ь', 'э', 'a', 'I', 'я', 'Ж', 'Ы', '#',
               '5', 'Q', '}', 'f', 'ы', 'g', 'b', 'F', 'г', 'Ф', 'м', 's', '$', '>', 'х', 'т', '<', 'Ц', 'l', 'П', '=',
               'Т', 'Г', 'О', '!', 'н', 'ъ', 'Ш', 'ц', 'o', 'Ю', 'H', 'O', 'K', 'в', 'x', 'U', 'Ё', 'к', 'с', '8', ' ',
               '2', 'W', 'R', 'E', ',', 'Э', 'L', 'Я', 'J', 'k', 'щ', '1', 'р', '7', 'm', 'е', '6', '%', 'c', '[', 'D',
               'Д', 'ё', '(', 'и', '@', 'й', 'Щ', 'б', 'у', 'T', 'Ъ', '{', '+', 'а', 'C', 'B', 'о', 'С', 'd', 't', '_',
               'ь', '*', 'Й', 'Н', 'A', 'G', 'Y', '\\', 'п', 'Х', 'л']
    if stor == 'Дешифровать':
        if tip == 'Цезарь':
            result = deshifrc(text, int(key), alfavit)
        else:
            result = deshifrv(text, key, alfavit)
    else:
        if tip == 'Цезарь':
            result = shifrc(text, int(key), alfavit)
        else:
            result = shifrv(text, key, alfavit)
    return result


app = QApplication([])
app.setStyle('Fusion')
window = QWidget()
window.setWindowTitle('Шифрование/Дешифрование')
layout = QVBoxLayout()

input_text = QTextEdit()
input_text.setPlaceholderText('Введите текст')

input_deystv = QLabel('Выберите действие (шифровка или дешифровка):')

combo_tip = QComboBox(window)
combo_tip.addItem('Шифровать')
combo_tip.addItem('Дешифровать')

input_key = QLineEdit()
input_key.setPlaceholderText('Введите ключ')

input_tip = QLabel('Выберите шифр (Цезарь или Виженер):')
combo_deystv = QComboBox(window)
combo_deystv.addItem('Цезарь')
combo_deystv.addItem('Виженер')

btn = QPushButton('Выполнить')

res_output = QTextEdit()
res_output.setPlaceholderText('Результат')
res_output.setReadOnly(True)
scroll_area = QScrollArea()
scroll_area.setWidget(res_output)
scroll_area.setWidgetResizable(True)

layout.addWidget(input_text)
layout.addWidget(input_deystv)
layout.addWidget(combo_deystv)
layout.addWidget(input_tip)
layout.addWidget(combo_tip)

layout.addWidget(input_key)

layout.addWidget(btn)
layout.addWidget(scroll_area)
window.setLayout(layout)


def on_button_clicked():
    stor = combo_deystv.currentText()
    tip = combo_tip.currentText()
    text = input_text.toPlainText()
    key = input_key.text()
    if not text or not stor or not tip or not key:
        QMessageBox.warning(window, 'Ошибка!', 'Ошибка!\nЗаполните все поля!')
        return
    else:
        res = opred(text, stor, tip, key)
    res_output.setText(res)


btn.clicked.connect(on_button_clicked)

window.show()
app.exec_()
