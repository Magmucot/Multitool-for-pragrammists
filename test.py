import sys
from PySide6.QtWidgets import (
    QApplication, QLineEdit,
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit,
    QComboBox, QLabel,
    QStackedWidget, QScrollArea,
    QMessageBox, QFrame,
    QGridLayout, QSizePolicy,
)
from PySide6.QtGui import QIcon, QCursor, QAction, QKeySequence
from PySide6.QtCore import QSize, Qt, QEvent
import resources  # noqa: F401
from OOP1 import Shifrator
from OOP2 import Transformator
from OOP3 import Calculator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мультитул")
        self.resize(400, 400)
        self.setMinimumSize(QSize(300, 400))
        self.setWindowIcon(QIcon(':/icons/icon.png'))
        central_widget = QWidget()

        self.setStyleSheet(
            """QWidget {background-color: #121212; color: white; font-family: Work Sans;
                           font-size: 12pt; font-weight: 600;}
                           QPushButton {background-color: #282828; border:none;}
                           QPushButton:hover {background-color: #888;}
                           QPushButton:pressed {background-color: #AAA;}
                           QComboBox {background-color: #282828; border: white 1px;}
                           QLineEdit, QTextEdit {background-color: #282828; border: white 1px;}
                           QLabel {color: #888; border: solid white 1px}"""
        )

        self.btn_active_style = "QPushButton { background-color: #A04602; border-radius: 2px; border: none; }"
        self.btn_inactive_style = "QPushButton { background-color: #FF8C00; border-radius: 2px; border: none; }"

        self.btn_style = (
            "QPushButton {color: black;background-color: #FF8C00; border-radius: 2px; border: none;}"
            "QPushButton:hover {background-color: #E07B00; border: none;}"
            "QPushButton:pressed {background-color: #CC6A00;border: none;}"
        )

        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.ans = 0

        self.up_layout = QHBoxLayout()
        self.btn_shifr = QPushButton()
        self.btn_shifr.setStyleSheet(self.btn_style)
        icon = QIcon(":/icons/fingerprint.png")
        icon1 = QIcon(":/icons/binary.png")
        icon2 = QIcon(":/icons/calculate.png")
        self.btn_shifr.setIcon(icon)
        self.btn_shifr.setIconSize(QSize(32, 32))
        self.btn_shifr.setFixedSize(40, 40)

        self.btn_transf = QPushButton()
        self.btn_transf.setIcon(icon1)
        self.btn_transf.setIconSize(QSize(30, 30))
        self.btn_transf.setFixedSize(40, 40)
        self.btn_transf.setStyleSheet(self.btn_style)
        self.btn_calc = QPushButton()
        self.btn_calc.setIcon(icon2)
        self.btn_calc.setIconSize(QSize(32, 32))
        self.btn_calc.setFixedSize(40, 40)
        self.btn_calc.setStyleSheet(self.btn_style)

        self.up_layout.addWidget(self.btn_shifr)
        self.up_layout.addWidget(self.btn_transf)
        self.up_layout.addWidget(self.btn_calc)
        self.up_layout.addStretch()

        self.main_layout.addLayout(self.up_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        self.main_layout.addWidget(separator)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.shifr_page()
        self.transf_page()
        self.calc_page()

        self.btn_shifr.clicked.connect(self.show_shifr_p)
        self.btn_transf.clicked.connect(self.show_transf_p)
        self.btn_calc.clicked.connect(self.show_calc_p)

    def show_shifr_p(self):
        self.stack.setCurrentIndex(0)
        self.btn_shifr.setStyleSheet(self.btn_active_style)
        self.btn_transf.setStyleSheet(self.btn_inactive_style)
        self.btn_calc.setStyleSheet(self.btn_inactive_style)

    def show_transf_p(self):
        self.stack.setCurrentIndex(1)
        self.btn_transf.setStyleSheet(self.btn_active_style)
        self.btn_shifr.setStyleSheet(self.btn_inactive_style)
        self.btn_calc.setStyleSheet(self.btn_inactive_style)

    def show_calc_p(self):
        self.stack.setCurrentIndex(2)
        self.btn_shifr.setStyleSheet(self.btn_inactive_style)
        self.btn_transf.setStyleSheet(self.btn_inactive_style)
        self.btn_calc.setStyleSheet(self.btn_active_style)
        self.le_enter.setFocus()

    def shifr_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Введите текст")
        layout.addWidget(self.input_text)

        input_deystv = QLabel("Выберите действие (шифровка или дешифровка):")
        layout.addWidget(input_deystv)

        self.combo_deystv = QComboBox()
        self.combo_deystv.addItem("Шифровать")
        self.combo_deystv.addItem("Дешифровать")
        layout.addWidget(self.combo_deystv)

        input_tip = QLabel("Выберите шифр (Цезарь или Виженер):")
        layout.addWidget(input_tip)

        self.combo_tip = QComboBox()
        self.combo_tip.addItem("Цезарь")
        self.combo_tip.addItem("Виженер")
        layout.addWidget(self.combo_tip)

        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText("Введите ключ")
        layout.addWidget(self.input_key)

        btn = QPushButton("Выполнить")
        btn.setFixedHeight(20)
        btn.setStyleSheet(
            """QPushButton {color: black; background-color: #63F113; border-radius: 2px; border: none; }
            QPushButton:hover { background-color: #309112; }"""
        )
        btn.clicked.connect(self.btn_shifr_click)
        layout.addWidget(btn)

        self.res_output = QTextEdit()
        self.res_output.setPlaceholderText("Результат")
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
            QMessageBox.warning(
                self, "Ошибка!", "Ошибка!\nЗаполните все поля!")
            return
        if tip == "Цезарь" and not key.isdigit():
            QMessageBox.warning(
                self, "Ошибка!", "Ошибка!\nКлюч для Цезаря должен быть целым числом!"
            )
            return
        shifrator = Shifrator(text, key)
        res = shifrator.opred(stor, tip)
        self.res_output.setText(res)

    def btn_transf_click(self):
        nums = self.input_numb1.text().split()
        try:
            sp_osn1 = list(map(int, self.input_osn1.text().split()))
            sp_osn2 = list(map(int, self.input_osn2.text().split()))
        except ValueError:
            QMessageBox.warning(
                self, "Ошибка!", "Ошибка!\nОснования должны быть числами!")
            return

        if not nums or not sp_osn1 or not sp_osn2:
            QMessageBox.warning(
                self, "Ошибка!", "Ошибка!\nЗаполните все поля!")
            return
        if (
            len(sp_osn1) != len(nums)
            or (len(sp_osn2) != len(nums) and len(sp_osn2) != 1)
        ):
            QMessageBox.warning(
                self,
                "Ошибка!",
                "Ошибка\nКоличество оснований должно соответствовать количеству чисел\nили быть одним числом для второго основания",
            )
            return
        if any(i > 35 or i < 2 for i in sp_osn1) or any(
            i > 35 or i < 2 for i in sp_osn2
        ):
            QMessageBox.warning(
                self,
                "Ошибка!",
                "Ошибка\nСистема счисления должна быть от 2 до 35",
            )
            return
        transf = Transformator()
        if len(sp_osn2) == 1:
            sp_osn2 = sp_osn2 * len(nums)
        try:
            result = transf.transform(nums, sp_osn1, sp_osn2)
            self.res.setText(" ".join(result))
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка!", f"Ошибка преобразования: {str(e)}")

    def transf_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout1 = QHBoxLayout()

        self.input_numb1 = QLineEdit()
        self.input_numb1.setPlaceholderText("число(а)")
        layout1.addWidget(self.input_numb1)

        self.input_osn1 = QLineEdit()
        self.input_osn1.setPlaceholderText("Основание(я) 1")
        layout1.addWidget(self.input_osn1)

        self.input_osn2 = QLineEdit()
        self.input_osn2.setPlaceholderText("Основание(я) ответа")
        layout1.addWidget(self.input_osn2)

        btn = QPushButton("Ввод")
        btn.clicked.connect(self.btn_transf_click)
        layout1.addWidget(btn)

        self.res = QLineEdit()
        self.res.setPlaceholderText("Результат")
        self.res.setReadOnly(True)
        layout1.addWidget(self.res)

        layout.addLayout(layout1)
        layout.addSpacing(20)

        math_layout = QHBoxLayout()
        self.m_num1 = QLineEdit()
        self.m_num1.setPlaceholderText("Число 1")
        math_layout.addWidget(self.m_num1)

        self.m_base1 = QLineEdit()
        self.m_base1.setPlaceholderText("Основание 1")
        math_layout.addWidget(self.m_base1)

        self.operation = QComboBox()
        self.operation.addItems(["+", "-", "×", "÷"])
        self.operation.setFixedWidth(30)
        math_layout.addWidget(self.operation)

        self.m_num2 = QLineEdit()
        self.m_num2.setPlaceholderText("Число 2")
        math_layout.addWidget(self.m_num2)

        self.m_base2 = QLineEdit()
        self.m_base2.setPlaceholderText("Основание 2")
        math_layout.addWidget(self.m_base2)

        self.math_btn = QPushButton("Ввод")
        self.math_btn.clicked.connect(self.math_btn_click)
        math_layout.addWidget(self.math_btn)

        self.base_res = QLineEdit()
        self.base_res.setPlaceholderText("Основание ответа")
        math_layout.addWidget(self.base_res)

        self.res_math = QLineEdit()
        self.res_math.setPlaceholderText("Результат")
        self.res_math.setReadOnly(True)
        math_layout.addWidget(self.res_math)

        layout.addLayout(math_layout)
        layout.addStretch()
        self.stack.addWidget(page)

    def math_btn_click(self):
        numb1, numb2 = self.m_num1.text().strip(), self.m_num2.text().strip()
        base1_str, base2_str, res_base_str = (
            self.m_base1.text().strip(),
            self.m_base2.text().strip(),
            self.base_res.text().strip(),
        )
        operation = self.operation.currentText()

        if not numb1 or not numb2:
            QMessageBox.warning(self, "Ошибка!", "Введите оба числа!")
            return

        try:
            base1 = int(base1_str) if base1_str else None
            base2 = int(base2_str) if base2_str else None
            res_base = int(res_base_str) if res_base_str else 10
        except ValueError:
            QMessageBox.warning(
                self, "Ошибка!", "Основания должны быть числами!")
            return

        if (
            (base1 and (base1 < 2 or base1 > 35))
            or (base2 and (base2 < 2 or base2 > 35))
            or (res_base < 2 or res_base > 35)
        ):
            QMessageBox.warning(
                self, "Ошибка!", "Система счисления должна быть от 2 до 35!")
            return

        try:
            if not base1:
                max_digit = max(int(d, 36) if d.isalnum() else 0 for d in numb1)
                base1 = max(max_digit + 1, 2)
            if not base2:
                max_digit = max(int(d, 36) if d.isalnum() else 0 for d in numb2)
                base2 = max(max_digit + 1, 2)

            num1 = int(numb1, base1)
            num2 = int(numb2, base2)

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Ошибка!",
                f"Неправильный ввод числа для указанного основания: {str(e)}",
            )
            return

        if operation == "÷" and num2 == 0:
            QMessageBox.warning(self, "Ошибка!", "Деление на ноль!")
            return

        oper = {"×": "*", "+": "+", "-": "-", "÷": "/"}
        math = Transformator()
        try:
            result = math.math_oper(num1, 10, oper[operation], num2, 10)
            if isinstance(result, float) and not result.is_integer():
                self.res_math.setText(str(result))
            else:
                result = math.transform([str(int(result))], [10], [res_base])[0]
                self.res_math.setText(result)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка!", f"Ошибка вычисления: {str(e)}")

    def eventFilter(self, obj, event):
        if obj == self.le_enter and event.type() == QEvent.Type.KeyPress:
            cursor_pos = self.le_enter.cursorPosition()
            text = self.le_enter.text()

            if event.key() == Qt.Key.Key_Left:
                self.le_enter.setCursorPosition(max(0, cursor_pos - 1))
                return True
            elif event.key() == Qt.Key.Key_Right:
                self.le_enter.setCursorPosition(min(len(text), cursor_pos + 1))
                return True
            elif event.key() == Qt.Key.Key_Space:
                self.add_to_expression(" ")
                return True
        return super().eventFilter(obj, event)

    def move_cursor_left(self):
        cursor_pos = self.le_enter.cursorPosition()
        self.le_enter.setCursorPosition(max(0, cursor_pos - 1))

    def move_cursor_right(self):
        cursor_pos = self.le_enter.cursorPosition()
        text = self.le_enter.text()
        self.le_enter.setCursorPosition(min(len(text), cursor_pos + 1))

    def calculate(self):
        calc = Calculator()
        enter = self.le_enter.text()
        enter = enter.replace('Ans', str(self.ans)).replace("π", 'pi')

        enter = self.balance_parentheses(enter)

        for func in ["sin(", "cos(", "tan(", "ctg("]:
            if func in enter:
                start = enter.find(func) + len(func)
                end = enter.find(")", start)
                if end == -1:
                    self.le_enter.setText("Ошибка: Незакрытая тригонометрическая функция")
                    return None
                arg = enter[start:end]
                try:
                    float(arg)
                except ValueError:
                    if arg.strip() == "" or not self.is_valid_expression(arg):
                        self.le_enter.setText("Ошибка: Неверный аргумент тригонометрической функции")
                        return None

        if "log(" in enter:
            start = enter.find("log(") + 4
            end = enter.find(")", start)
            if end == -1:
                self.le_enter.setText("Ошибка: Незакрытый логарифм")
                return None
            log_content = enter[start:end]
            if "," not in log_content:
                self.le_enter.setText("Ошибка: Логарифм требует два аргумента (x,b)")
                return None
            x, b = log_content.split(",", 1)
            x, b = x.strip(), b.strip()
            try:
                x_val = float(x)
                b_val = float(b)
                if x_val <= 0 or b_val <= 0 or b_val == 1:
                    self.le_enter.setText("Ошибка: Неверные аргументы логарифма (x > 0, b > 0, b ≠ 1)")
                    return None
            except ValueError:
                if not self.is_valid_expression(x) or not self.is_valid_expression(b):
                    self.le_enter.setText("Ошибка: Неверные аргументы логарифма")
                    return None

        # Валидация факториала
        if '!' in enter:
            parts = enter.split('!')
            for i, part in enumerate(parts[:-1]):
                try:
                    num = float(part.split()[-1] if ' ' in part else part)
                    if not num.is_integer() or num < 0:
                        self.le_enter.setText("Ошибка: Факториал только для целых неотрицательных чисел")
                        return None
                except ValueError:
                    self.le_enter.setText("Ошибка: Неверный ввод для факториала")
                    return None

        try:
            res = str(calc.combined_calc(enter))
            self.lbl_temp.setText(self.remove_trailing_zeros(res))
            self.ans = float(res) if '.' in res else int(res)
            return res
        except Exception as e:
            self.le_enter.setText("Ошибка")
            return None

    def is_valid_expression(self, expr):
        """Проверяет, является ли строка допустимым выражением"""
        try:
            calc = Calculator()
            calc.combined_calc(expr)
            return True
        except Exception:
            return False

    def balance_parentheses(self, expr):
        res = []
        stack = []
        i = 0
        while i < len(expr):
            if expr[i:i+4] in ["sin(", "cos(", "tan(", "ctg("]:
                res.append(expr[i:i+4])
                stack.append(expr[i:i+4])
                i += 4
            elif expr[i:i+4] == "log(":
                res.append("log(")
                stack.append("log(")
                i += 4
            elif expr[i] == '(':
                res.append('(')
                stack.append('(')
                i += 1
            elif expr[i] == ')':
                if stack:
                    stack.pop()
                    res.append(')')
                i += 1
            else:
                res.append(expr[i])
                i += 1

        # Закрыть незакрытые скобки
        while stack:
            stack.pop()
            res.append(')')

        return ''.join(res)

    def clear_expression(self):
        self.lbl_temp.clear()
        self.le_enter.setText('0')

    def backspace(self):
        current = self.le_enter.text()
        if current != "Ошибка" and len(current) > 1:
            self.le_enter.setText(current[:-1])
        else:
            self.le_enter.setText('0')

    def clear_entry(self):
        self.le_enter.setText('0')

    def add_point(self):
        current = self.le_enter.text()
        if '.' not in current and current != "Ошибка":
            self.le_enter.setText(current + '.')

    def remove_trailing_zeros(self, s: str) -> str:
        try:
            num = float(s)
            return str(int(num)) if num.is_integer() else str(num).rstrip("0").rstrip(".")
        except ValueError:
            return s

    def negate(self):
        text = self.le_enter.text()
        cursor_pos = self.le_enter.cursorPosition()
        if text == "Ошибка" or text == "0":
            return

        start = cursor_pos
        while start > 0 and (text[start-1].isdigit() or text[start-1] in ".−"):
            start -= 1
        end = cursor_pos
        while end < len(text) and (text[end].isdigit() or text[end] == "."):
            end += 1

        number = text[start:end]
        if not number or number == "−":
            return

        if number.startswith("−"):
            new_number = number[1:]
        else:
            new_number = "−" + number

        new_text = text[:start] + new_number + text[end:]
        self.le_enter.setText(new_text)
        self.le_enter.setCursorPosition(start + len(new_number))

    def add_to_expression(self, value):
        cursor_pos = self.le_enter.cursorPosition()
        text = self.le_enter.text()

        if text in ("Ошибка", "0"):
            text, cursor_pos = "", 0

        prev_char = text[cursor_pos-1:cursor_pos] if cursor_pos > 0 else ""
        next_char = text[cursor_pos:cursor_pos+1] if cursor_pos < len(text) else ""
        is_operator = value in ["+", "−", "×", "÷", "//", "%"]
        is_number = value.isdigit() or value == "."
        is_function = value in ["sin(", "cos(", "tan(", "ctg(", "log(", "√(", "∫(", "arc"]

        # Проверка на пустые скобки () или модуль ||
        inside_empty = cursor_pos >= 1 and cursor_pos <= len(text) and (
            text[cursor_pos-1:cursor_pos+1] == "()" or
            text[cursor_pos-1:cursor_pos+1] == "||"
        )
        if inside_empty:
            if text[cursor_pos-1:cursor_pos+1] == "()" and (is_number or is_function or value in ["e", "π", "Ans"]):
                text = text[:cursor_pos-1] + value + text[cursor_pos:]
                self.le_enter.setText(text)
                self.le_enter.setCursorPosition(cursor_pos-1 + len(value))
                return
            if text[cursor_pos-1:cursor_pos+1] == "||" and is_number:
                text = text[:cursor_pos-1] + value + text[cursor_pos:]
                self.le_enter.setText(text)
                self.le_enter.setCursorPosition(cursor_pos-1 + len(value))
                return

        # Проверка, находится ли курсор внутри функции
        open_paren = 0
        comma_pos = -1
        for i in range(cursor_pos):
            if text[i:i+4] in ["sin(", "cos(", "tan(", "ctg("] or text[i:i+3] == "log(":
                open_paren += 1
            elif text[i] == '(':
                open_paren += 1
            elif text[i] == ')':
                open_paren -= 1
            elif text[i] == ',' and open_paren > 0:
                comma_pos = i

        # Закрытие функции перед оператором
        if is_operator and open_paren > 0 and prev_char.isdigit():
            text = text[:cursor_pos] + ")" + text[cursor_pos:]
            cursor_pos += 1
            next_char = ")"

        # Валидация факториала
        if value == "!":
            start = cursor_pos
            while start > 0 and (text[start-1].isdigit() or text[start-1] == "."):
                start -= 1
            try:
                num = float(text[start:cursor_pos])
                if not num.is_integer() or num < 0:
                    return
            except ValueError:
                return

        # Обработка модуля
        if value == "|":
            insert_text = "|" if prev_char == "|" else "||"
            new_pos = cursor_pos + (1 if prev_char == "|" else 1)
            if prev_char != "|":
                self.le_enter.setText(text[:cursor_pos] + insert_text + text[cursor_pos:])
                self.le_enter.setCursorPosition(new_pos)
                return

        # Формирование текста для вставки
        insert_text = (
            "∫(,,)" if value == "∫(" else
            "log(,)" if value == "log(" else
            f" {value} " if is_operator and prev_char not in " +−×÷/%(" and next_char not in " +−×÷/%)" else
            " " if value == " " and prev_char != " " and next_char != " " else
            value
        )

        # Вычисление новой позиции курсора
        new_pos = cursor_pos + (
            2 if value in [",", "^"] else
            5 if value == "arc" else
            2 if value == "∫(" else
            3 if is_operator and insert_text.startswith(" ") else
            len(value) if value in ["sin(", "cos(", "tan(", "ctg(", "log("] else
            1
        )

        self.le_enter.setText(text[:cursor_pos] + insert_text + text[cursor_pos:])
        self.le_enter.setCursorPosition(new_pos)

    def calc_page(self):
        page = QWidget()
        self.verticalLayout = QVBoxLayout(page)
        self.le_enter = QLineEdit(page)
        self.le_enter.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum))
        self.le_enter.setStyleSheet(
            "height: 45px;font-size:20pt;border:none;")
        self.le_enter.setMaxLength(1000)
        self.le_enter.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.le_enter.setReadOnly(True)
        self.le_enter.setText("0")
        self.le_enter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.verticalLayout.addWidget(self.le_enter)

        self.le_enter.installEventFilter(self)

        self.lbl_temp = QLabel(page)
        self.lbl_temp.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum))
        self.lbl_temp.setStyleSheet("color:#888;")
        self.lbl_temp.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout.addWidget(self.lbl_temp)

        self.layout_btns = QGridLayout()
        sp = QSizePolicy(QSizePolicy.Policy.Preferred,
                        QSizePolicy.Policy.Expanding)

        self.btn_C = QPushButton(page)
        self.btn_C.setSizePolicy(sp)
        self.btn_C.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_C.setText("C")
        self.btn_C.setShortcut("C")
        self.btn_C.setStyleSheet(self.btn_style)
        self.layout_btns.addWidget(self.btn_C, 0, 0)

        self.btn_CE = QPushButton(page)
        self.btn_CE.setSizePolicy(sp)
        self.btn_CE.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_CE.setText("CE")
        self.btn_CE.setStyleSheet(self.btn_style)
        self.layout_btns.addWidget(self.btn_CE, 0, 1)

        self.btn_backspace = QPushButton(page)
        self.btn_backspace.setSizePolicy(sp)
        self.btn_backspace.setShortcut('Backspace')
        self.btn_backspace.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_backspace.setStyleSheet(self.btn_style)
        self.btn_backspace.setIcon(QIcon(":/icons/backspace_black.png"))
        self.btn_backspace.setIconSize(QSize(48, 48))
        self.layout_btns.addWidget(self.btn_backspace, 0, 2)

        self.btn_level = QPushButton(page)
        self.btn_level.setSizePolicy(sp)
        self.btn_level.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_level.setText("^")
        self.btn_level.setShortcut("^")
        self.layout_btns.addWidget(self.btn_level, 0, 3)

        self.btn_log = QPushButton(page)
        self.btn_log.setSizePolicy(sp)
        self.btn_log.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_log.setText("log(x,b)")
        self.layout_btns.addWidget(self.btn_log, 0, 4)

        self.btn_ans = QPushButton(page)
        self.btn_ans.setSizePolicy(sp)
        self.btn_ans.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_ans.setText("Ans")
        self.layout_btns.addWidget(self.btn_ans, 0, 6)

        self.btn_left = QPushButton(page)
        self.btn_left.setSizePolicy(sp)
        self.btn_left.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_left.setText("<-")
        self.btn_left.setShortcut(Qt.Key.Key_Left)
        self.btn_left.setStyleSheet(self.btn_style)
        self.layout_btns.addWidget(self.btn_left, 0, 7)

        self.btn_rem = QPushButton(page)
        self.btn_rem.setSizePolicy(sp)
        self.btn_rem.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_rem.setText("%")
        self.btn_rem.setShortcut("%")
        self.layout_btns.addWidget(self.btn_rem, 1, 0)

        self.btn_div_c = QPushButton(page)
        self.btn_div_c.setSizePolicy(sp)
        self.btn_div_c.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_div_c.setText("//")
        self.layout_btns.addWidget(self.btn_div_c, 1, 1)

        self.btn_fact = QPushButton(page)
        self.btn_fact.setSizePolicy(sp)
        self.btn_fact.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_fact.setText("!")
        self.btn_fact.setShortcut("!")
        self.layout_btns.addWidget(self.btn_fact, 1, 2)

        self.btn_root = QPushButton(page)
        self.btn_root.setSizePolicy(sp)
        self.btn_root.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_root.setText("√")
        self.layout_btns.addWidget(self.btn_root, 1, 3)

        self.btn_integr = QPushButton(page)
        self.btn_integr.setSizePolicy(sp)
        self.btn_integr.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_integr.setText("∫")
        self.layout_btns.addWidget(self.btn_integr, 1, 4)

        self.btn_mul = QPushButton(page)
        self.btn_mul.setSizePolicy(sp)
        self.btn_mul.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_mul.setText("×")
        self.btn_mul.setShortcut("*")
        self.layout_btns.addWidget(self.btn_mul, 1, 6)

        self.btn_right = QPushButton(page)
        self.btn_right.setSizePolicy(sp)
        self.btn_right.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_right.setText("->")
        self.btn_right.setShortcut(Qt.Key.Key_Right)
        self.btn_right.setStyleSheet(self.btn_style)
        self.layout_btns.addWidget(self.btn_right, 1, 7)

        self.btn_7 = QPushButton(page)
        self.btn_7.setSizePolicy(sp)
        self.btn_7.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_7.setText("7")
        self.btn_7.setShortcut("7")
        self.layout_btns.addWidget(self.btn_7, 2, 0)

        self.btn_8 = QPushButton(page)
        self.btn_8.setSizePolicy(sp)
        self.btn_8.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_8.setText("8")
        self.btn_8.setShortcut("8")
        self.layout_btns.addWidget(self.btn_8, 2, 1)

        self.btn_9 = QPushButton(page)
        self.btn_9.setSizePolicy(sp)
        self.btn_9.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_9.setText("9")
        self.btn_9.setShortcut("9")
        self.layout_btns.addWidget(self.btn_9, 2, 2)

        self.btn_sin = QPushButton(page)
        self.btn_sin.setSizePolicy(sp)
        self.btn_sin.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_sin.setText("sin")
        self.layout_btns.addWidget(self.btn_sin, 2, 3)

        self.btn_cos = QPushButton(page)
        self.btn_cos.setSizePolicy(sp)
        self.btn_cos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cos.setText("cos")
        self.layout_btns.addWidget(self.btn_cos, 2, 4)

        self.btn_div = QPushButton(page)
        self.btn_div.setSizePolicy(sp)
        self.btn_div.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_div.setText("÷")
        self.btn_div.setShortcut("/")
        self.layout_btns.addWidget(self.btn_div, 2, 6)

        self.btn_e = QPushButton(page)
        self.btn_e.setSizePolicy(sp)
        self.btn_e.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_e.setText("e")
        self.layout_btns.addWidget(self.btn_e, 2, 7)

        self.btn_4 = QPushButton(page)
        self.btn_4.setSizePolicy(sp)
        self.btn_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4.setText("4")
        self.btn_4.setShortcut("4")
        self.layout_btns.addWidget(self.btn_4, 3, 0)

        self.btn_5 = QPushButton(page)
        self.btn_5.setSizePolicy(sp)
        self.btn_5.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_5.setText("5")
        self.btn_5.setShortcut("5")
        self.layout_btns.addWidget(self.btn_5, 3, 1)

        self.btn_6 = QPushButton(page)
        self.btn_6.setSizePolicy(sp)
        self.btn_6.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_6.setText("6")
        self.btn_6.setShortcut("6")
        self.layout_btns.addWidget(self.btn_6, 3, 2)

        self.btn_tan = QPushButton(page)
        self.btn_tan.setSizePolicy(sp)
        self.btn_tan.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_tan.setText("tan")
        self.layout_btns.addWidget(self.btn_tan, 3, 3)

        self.btn_ctg = QPushButton(page)
        self.btn_ctg.setSizePolicy(sp)
        self.btn_ctg.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_ctg.setText("ctg")
        self.layout_btns.addWidget(self.btn_ctg, 3, 4)

        self.btn_neg = QPushButton(page)
        self.btn_neg.setSizePolicy(sp)
        self.btn_neg.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_neg.setText("−")
        self.btn_neg.setShortcut("-")
        self.layout_btns.addWidget(self.btn_neg, 3, 6)

        self.btn_pi = QPushButton(page)
        self.btn_pi.setSizePolicy(sp)
        self.btn_pi.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_pi.setText("π")
        self.layout_btns.addWidget(self.btn_pi, 3, 7)

        self.btn_1 = QPushButton(page)
        self.btn_1.setSizePolicy(sp)
        self.btn_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_1.setText("1")
        self.btn_1.setShortcut("1")
        self.layout_btns.addWidget(self.btn_1, 5, 0)

        self.btn_2 = QPushButton(page)
        self.btn_2.setSizePolicy(sp)
        self.btn_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_2.setText("2")
        self.btn_2.setShortcut("2")
        self.layout_btns.addWidget(self.btn_2, 5, 1)

        self.btn_3 = QPushButton(page)
        self.btn_3.setSizePolicy(sp)
        self.btn_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_3.setText("3")
        self.btn_3.setShortcut("3")
        self.layout_btns.addWidget(self.btn_3, 5, 2)

        self.btn_arc = QPushButton(page)
        self.btn_arc.setSizePolicy(sp)
        self.btn_arc.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_arc.setText("arc")
        self.layout_btns.addWidget(self.btn_arc, 5, 3)

        self.btn_bracel = QPushButton(page)
        self.btn_bracel.setSizePolicy(sp)
        self.btn_bracel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_bracel.setText("(")
        self.btn_bracel.setShortcut("(")
        self.layout_btns.addWidget(self.btn_bracel, 5, 4)

        self.btn_plus = QPushButton(page)
        self.btn_plus.setSizePolicy(sp)
        self.btn_plus.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_plus.setText("+")
        self.btn_plus.setShortcut("+")
        self.layout_btns.addWidget(self.btn_plus, 5, 6)

        self.btn_sign = QPushButton(page)
        self.btn_sign.setSizePolicy(sp)
        self.btn_sign.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_sign.setText("+/−")
        self.layout_btns.addWidget(self.btn_sign, 6, 0)

        self.btn_0 = QPushButton(page)
        self.btn_0.setSizePolicy(sp)
        self.btn_0.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_0.setText("0")
        self.btn_0.setShortcut("0")
        self.layout_btns.addWidget(self.btn_0, 6, 1)

        self.btn_point = QPushButton(page)
        self.btn_point.setSizePolicy(sp)
        self.btn_point.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_point.setText(".")
        self.btn_point.setShortcut(".")
        self.layout_btns.addWidget(self.btn_point, 6, 2)

        self.btn_mod = QPushButton(page)
        self.btn_mod.setSizePolicy(sp)
        self.btn_mod.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_mod.setText("|x|")
        self.btn_mod.setShortcut("|")
        self.layout_btns.addWidget(self.btn_mod, 6, 3)

        self.btn_bracer = QPushButton(page)
        self.btn_bracer.setSizePolicy(sp)
        self.btn_bracer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_bracer.setText(")")
        self.btn_bracer.setShortcut(")")
        self.layout_btns.addWidget(self.btn_bracer, 6, 4)

        self.btn_calcul = QPushButton(page)
        self.btn_calcul.setSizePolicy(sp)
        self.btn_calcul.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_calcul.setText("=")
        self.layout_btns.addWidget(self.btn_calcul, 6, 6)

        calc_action = QAction(self)
        calc_action.setShortcuts([
            QKeySequence("="),
            QKeySequence(Qt.Key.Key_Return),
            QKeySequence(Qt.Key.Key_Enter)
        ])
        calc_action.triggered.connect(self.calculate)
        self.btn_calcul.addAction(calc_action)

        self.btn_0.clicked.connect(lambda: self.add_to_expression("0"))
        self.btn_1.clicked.connect(lambda: self.add_to_expression("1"))
        self.btn_2.clicked.connect(lambda: self.add_to_expression("2"))
        self.btn_3.clicked.connect(lambda: self.add_to_expression("3"))
        self.btn_4.clicked.connect(lambda: self.add_to_expression("4"))
        self.btn_5.clicked.connect(lambda: self.add_to_expression("5"))
        self.btn_6.clicked.connect(lambda: self.add_to_expression("6"))
        self.btn_7.clicked.connect(lambda: self.add_to_expression("7"))
        self.btn_8.clicked.connect(lambda: self.add_to_expression("8"))
        self.btn_9.clicked.connect(lambda: self.add_to_expression("9"))
        self.btn_bracel.clicked.connect(lambda: self.add_to_expression("("))
        self.btn_bracer.clicked.connect(lambda: self.add_to_expression(")"))
        self.btn_level.clicked.connect(lambda: self.add_to_expression("^"))
        self.btn_fact.clicked.connect(lambda: self.add_to_expression("!"))
        self.btn_log.clicked.connect(lambda: self.add_to_expression("log("))
        self.btn_sin.clicked.connect(lambda: self.add_to_expression("sin("))
        self.btn_cos.clicked.connect(lambda: self.add_to_expression("cos("))
        self.btn_tan.clicked.connect(lambda: self.add_to_expression("tan("))
        self.btn_ctg.clicked.connect(lambda: self.add_to_expression("ctg("))
        self.btn_arc.clicked.connect(lambda: self.add_to_expression("arc"))
        self.btn_ans.clicked.connect(lambda: self.add_to_expression(" Ans "))
        self.btn_mod.clicked.connect(lambda: self.add_to_expression("|"))
        self.btn_plus.clicked.connect(lambda: self.add_to_expression("+"))
        self.btn_neg.clicked.connect(lambda: self.add_to_expression("−"))
        self.btn_rem.clicked.connect(lambda: self.add_to_expression("%"))
        self.btn_div.clicked.connect(lambda: self.add_to_expression("÷"))
        self.btn_div_c.clicked.connect(lambda: self.add_to_expression("//"))
        self.btn_mul.clicked.connect(lambda: self.add_to_expression("×"))
        self.btn_root.clicked.connect(lambda: self.add_to_expression("√"))
        self.btn_integr.clicked.connect(lambda: self.add_to_expression("∫("))
        self.btn_e.clicked.connect(lambda: self.add_to_expression("e"))
        self.btn_pi.clicked.connect(lambda: self.add_to_expression("π"))

        self.btn_CE.clicked.connect(self.clear_entry)
        self.btn_backspace.clicked.connect(self.backspace)
        self.btn_C.clicked.connect(self.clear_expression)
        self.btn_point.clicked.connect(self.add_point)
        self.btn_calcul.clicked.connect(self.calculate)
        self.btn_left.clicked.connect(self.move_cursor_left)
        self.btn_right.clicked.connect(self.move_cursor_right)
        self.btn_sign.clicked.connect(self.negate)

        self.verticalLayout.addLayout(self.layout_btns)
        self.stack.addWidget(page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())