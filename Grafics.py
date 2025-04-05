from curses.ascii import isdigit
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTextEdit, QComboBox, QLabel, QLineEdit,
                               QStackedWidget, QScrollArea, QMessageBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from OOP1 import Shifrator
from OOP2 import Transformator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Мультитул')
        self.resize(700, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.btn_style = """
            QPushButton { background-color: #FCA300; border-radius: 2px; border: none; }
            QPushButton:hover { background-color: #A04602; }
        """
        self.btn_active_style = """
            QPushButton { background-color: #A04602; }
        """
        self.btn_inactive_style = """
            QPushButton { background-color: #FCA300;}
        """
        
        self.setStyleSheet(self.btn_style)

        self.up_layout = QHBoxLayout()
        self.btn_shifr = QPushButton()
        self.btn_shifr.setStyleSheet(
            '''QPushButton:{border-radius: 2px; border: none}''')
        self.btn_shifr.setIcon(QIcon.fromTheme("document-encrypt"))
        self.btn_shifr.setFixedSize(40, 40)
        self.up_layout.addWidget(self.btn_shifr)

        self.btn_transf = QPushButton('1011')
        self.btn_transf.setFixedSize(40, 40)
        
        
        self.up_layout.addWidget(self.btn_transf)
        self.up_layout.addStretch()
        
        self.main_layout.addLayout(self.up_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFixedHeight(1)
        self.main_layout.addWidget(separator)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.shifr_page()
        self.transf_page()

        self.btn_shifr.clicked.connect(self.show_shifr_p)
        self.btn_transf.clicked.connect(self.show_transf_p)

    def show_shifr_p(self):
        self.stack.setCurrentIndex(0)
        self.setStyleSheet(self.btn_style)
        self.btn_shifr.setStyleSheet(self.btn_active_style)
        self.btn_transf.setStyleSheet(self.btn_inactive_style)

    def show_transf_p(self):
        self.stack.setCurrentIndex(1)
        self.setStyleSheet(self.btn_style)
        self.btn_transf.setStyleSheet(self.btn_active_style)
        self.btn_shifr.setStyleSheet(self.btn_inactive_style)

    def shifr_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('Введите текст')
        layout.addWidget(self.input_text)

        input_deystv = QLabel('Выберите действие (шифровка или дешифровка):')
        layout.addWidget(input_deystv)

        self.combo_deystv = QComboBox()
        self.combo_deystv.addItem('Шифровать')
        self.combo_deystv.addItem('Дешифровать')
        layout.addWidget(self.combo_deystv)

        input_tip = QLabel('Выберите шифр (Цезарь или Виженер):')
        layout.addWidget(input_tip)

        self.combo_tip = QComboBox()
        self.combo_tip.addItem('Цезарь')
        self.combo_tip.addItem('Виженер')
        layout.addWidget(self.combo_tip)

        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText('Введите ключ')
        layout.addWidget(self.input_key)

        btn = QPushButton('Выполнить')
        btn.clicked.connect(self.btn_shifr_click)
        layout.addWidget(btn)

        self.res_output = QTextEdit()
        self.res_output.setPlaceholderText('Результат')
        self.res_output.setReadOnly(True)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.res_output)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        self.stack.addWidget(page)

    def btn_shifr_click(self):
        stor = self.combo_deystv.currentText()
        tip = self.combo_tip.currentText()
        text = self.input_text.toPlainText()
        key = self.input_key.text()
        if not text or not stor or not tip or not key:
            QMessageBox.warning(self, 'Ошибка!',
                                'Ошибка!\nЗаполните все поля!')
            return
        if tip == 'Цезарь' and not isdigit(key):
            QMessageBox.warning(self, 'Ошибка!',
                                'Ошибка!\nКлюч для цезаря всегда целое число!')
            return
        shifrator = Shifrator(text, key)
        res = shifrator.opred(stor, tip)
        self.res_output.setText(res)

    def btn_transf_click(self):
        nums = self.input_numb1.text().split()
        sp_osn1, sp_osn2 = list(map(int, self.input_osn1.text().split())), list(
            map(int, self.input_osn2.text().split()))
        if not nums or not sp_osn1 or not sp_osn2:
            QMessageBox.warning(self, 'Ошибка!',
                                'Ошибка!\nЗаполните все поля!')
            return
        if (len(sp_osn1) != len(sp_osn2) or len(sp_osn1) != len(nums) or len(nums) != len(sp_osn2)) and len(sp_osn2) != 1:
            QMessageBox.warning(
                self, 'Ошибка!', 'Ошибка\nКол-во первых оснований должно быть равно\nКол-ву вторых оснований и кол-ву чисел')
            return
        if any(i > 35 or i < 2 for i in sp_osn1) or any(i > 35 or i < 2 for i in sp_osn2):
            QMessageBox.warning(
                self, 'Ошибка!', 'Ошибка\nМаксимальная доступная система 35\nА минимальная 2')
            return
        transf = Transformator()
        result = transf.transform(nums, sp_osn1, len(nums) * sp_osn2)
        self.res.setText(" ".join(result))

    def transf_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout1 = QHBoxLayout()

        self.input_numb1 = QLineEdit()
        self.input_numb1.setPlaceholderText('Введите число(а)')
        
        self.input_osn1 = QLineEdit()
        self.input_osn1.setPlaceholderText('Введите Основание(я) 1')
        
        self.input_osn2 = QLineEdit()
        self.input_osn2.setPlaceholderText('Введите Основание(я) 2')
        
        btn = QPushButton('Ввод')
        self.res = QLineEdit('Результат')
        
        self.res.setReadOnly(True)
        btn.clicked.connect(self.btn_transf_click)

        layout1.addWidget(self.input_numb1)
        layout1.addWidget(self.input_osn1)
        layout1.addWidget(self.input_osn2)
        layout1.addWidget(btn)
        layout1.addWidget(self.res)

        layout.addLayout(layout1)
        layout.addSpacing(20)

        math_layout = QHBoxLayout()
        self.m_num1 = QLineEdit()
        self.m_num1.setPlaceholderText('Введите число')
        math_layout.addWidget(self.m_num1)

        self.m_base1 = QLineEdit()
        self.m_base1.setPlaceholderText('Введите основание')
        math_layout.addWidget(self.m_base1)
        
        self.operation = QComboBox()
        self.operation.addItems(["+", "-", "×", "÷"])
        self.operation.setFixedWidth(50)
        math_layout.addWidget(self.operation)
        
        self.m_num2 = QLineEdit()
        self.m_num2.setPlaceholderText('Введите число')
        math_layout.addWidget(self.m_num2)

        self.m_base2 = QLineEdit()
        self.m_base2.setPlaceholderText('Введите основание')
        math_layout.addWidget(self.m_base2)
        
        self.math_btn = QPushButton('Выполнить')
        self.math_btn.clicked.connect(self.math_btn_click)
        math_layout.addWidget(self.math_btn)
        
        self.res_base = QLineEdit()
        self.res_base.setPlaceholderText('Основание ответа')
        self.res_base.setFixedWidth(50)
        math_layout.addWidget(self.res_base)
        
        self.res_math = QLineEdit("Результат")
        self.res_math.setReadOnly(True)
        self.res_math.setFixedWidth(100)
        math_layout.addWidget(self.res_math)
        
        
        layout.addLayout(math_layout)
        layout.addStretch()
        self.stack.addWidget(page)
        
    def math_btn_click(self):
        numb1, numb2 = str(self.m_num1.text().strip()), str(self.m_num2.text().strip())
        res_base, base1, base2 = self.res_base.text(), str(self.m_base1.text()), str(self.m_base2.text())
        
        operation = self.operation.currentText()

        if not numb1 or not numb2:
            QMessageBox.warning(
                self, "Ошибка!", "Введите оба числа!")
            return
        try:
            if not self.res_base:
                res_base = 10
            if not base1 or not base2:
                digits = set(numb1 + numb2)
                max_digit = max([int(d, 16) for d in digits if d.isalnum()])
                auto_base = max_digit + 1
                base1 = auto_base if not base1 else int(base1)
                base2 = auto_base if not base2 else int(base2)
            else:
                res_base = int(res_base)
                base1 = int(base1)
                base2 = int(base2)
            if base1 < 2 or base2 < 2 or res_base < 2:
                QMessageBox.warning(self, "Ошибка!", "Система счисления должна быть >= 2!")
                return
            num1 = int(numb1, base1)
            num2 = int(numb2, base2)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка!", f"Неправильный ввод: {str(e)}")
            return

        if operation == "÷" and num2 == 0:
            QMessageBox.warning(
                self, "Ошибка!", "Деление на ноль!")
            return
        oper = {"×": '*', '+': '+', '-': "-", '÷': '/'}
        math = Transformator()
        result = str(math.math_oper(num1, base1, oper[operation], num2, base2))
        self.res_math.setText(result)

if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
