from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QGridLayout, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt
from core.calculator import evaluate
from solvers.equation_solver import solve_equation
from converters.base_converter import int_to_base, base_to_int
from converters.unit_converter import convert_unit, UNITS
# УДАЛЕНО: from math_tools.plotter import plot_2d, plot_3d ← ЭТОЙ СТРОКИ БОЛЬШЕ НЕТ!
from math_tools.matrix_ops import matrix_add, matrix_mult, matrix_det, matrix_inv

class CalculatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_module = "calc"
        self.content_layout = QVBoxLayout()
        self.setLayout(self.content_layout)
        self.switch_to("calc")

    def switch_to(self, module):
        # Очищаем старый контент
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.current_module = module

        if module == "calc":
            self.create_calculator_view()
        elif module == "eq":
            self.create_equation_view()
        elif module == "base":
            self.create_base_converter_view()
        elif module == "units":
            self.create_unit_converter_view()
        elif module == "plot2d":
            self.create_plot2d_view()
        elif module == "plot3d":
            self.create_plot3d_view()
        elif module == "matrix":
            self.create_matrix_view()
        elif module == "history":
            self.create_history_view()

    # ========== КАЛЬКУЛЯТОР ==========
    def create_calculator_view(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.calc_display = QLineEdit()
        self.calc_display.setReadOnly(True)
        self.calc_display.setAlignment(Qt.AlignRight)
        self.calc_display.setStyleSheet("font-size: 20px; padding: 10px;")
        layout.addWidget(self.calc_display)

        grid = QGridLayout()
        buttons = [
            ('C', '(', ')', '÷'),
            ('7', '8', '9', '×'),
            ('4', '5', '6', '-'),
            ('1', '2', '3', '+'),
            ('0', '.', '±', '='),
            ('x²', '√', 'π', 'e'),
            ('sin', 'cos', 'tan', 'log'),
            ('ln', '1/x', '|x|', '^')
        ]
        self.calc_expr = ""
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn = QPushButton(text)
                btn.clicked.connect(lambda _, t=text: self.calc_button_click(t))
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 18px;
                        padding: 15px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        background-color: #fafafa;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
                grid.addWidget(btn, i, j)
        layout.addLayout(grid)
        widget.setLayout(layout)
        self.content_layout.addWidget(widget)

    def calc_button_click(self, symbol):
        if symbol == 'C':
            self.calc_expr = ""
        elif symbol == '=':
            try:
                result = evaluate(self.calc_expr)
                self.calc_expr = str(result)
            except Exception as e:
                self.calc_expr = f"Ошибка: {e}"
        elif symbol == '÷':
            self.calc_expr += '/'
        elif symbol == '×':
            self.calc_expr += '*'
        elif symbol == 'x²':
            self.calc_expr += '**2'
        elif symbol == '√':
            self.calc_expr += 'sqrt('
        elif symbol == 'π':
            self.calc_expr += 'pi'
        elif symbol == 'e':
            self.calc_expr += 'e'
        elif symbol == '^':
            self.calc_expr += '**'
        elif symbol == '±':
            if self.calc_expr and self.calc_expr[0] == '-':
                self.calc_expr = self.calc_expr[1:]
            else:
                self.calc_expr = '-' + self.calc_expr
        elif symbol == '1/x':
            self.calc_expr += '1/'
        elif symbol == '|x|':
            self.calc_expr += 'abs('
        elif symbol in ('sin', 'cos', 'tan', 'log', 'ln'):
            self.calc_expr += symbol + '('
        else:
            self.calc_expr += symbol
        self.calc_display.setText(self.calc_expr)

    # ========== УРАВНЕНИЯ ==========
    def create_equation_view(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Введите уравнение или систему (по одной на строку):")
        self.eq_input = QTextEdit()
        self.eq_input.setPlaceholderText("Пример:\nx + y = 5\nx - y = 1")
        self.eq_result = QTextEdit()
        self.eq_result.setReadOnly(True)
        solve_btn = QPushButton("Решить")
        solve_btn.clicked.connect(self.solve_equation)
        layout.addWidget(label)
        layout.addWidget(self.eq_input)
        layout.addWidget(solve_btn)
        layout.addWidget(self.eq_result)
        widget.setLayout(layout)
        self.content_layout.addWidget(widget)

    def solve_equation(self):
        eq = self.eq_input.toPlainText()
        sols = solve_equation(eq)
        self.eq_result.setPlainText("\n".join(sols))

    # ========== СИСТЕМЫ СЧИСЛЕНИЯ ==========
    def create_base_converter_view(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.base_num = QLineEdit()
        self.from_base = QLineEdit("10")
        self.to_base = QLineEdit("2")
        convert_btn = QPushButton("Перевести")
        convert_btn.clicked.connect(self.convert_base)
        self.base_result = QTextEdit()
        self.base_result.setReadOnly(True)
        layout.addWidget(QLabel("Число:"))
        layout.addWidget(self.base_num)
        layout.addWidget(QLabel("Из основания:"))
        layout.addWidget(self.from_base)
        layout.addWidget(QLabel("В основание:"))
        layout.addWidget(self.to_base)
        layout.addWidget(convert_btn)
        layout.addWidget(self.base_result)
        widget.setLayout(layout)
        self.content_layout.addWidget(widget)

    def convert_base(self):
        try:
            num_str = self.base_num.text().strip()
            from_b = int(self.from_base.text())
            to_b = int(self.to_base.text())
            if from_b == 10:
                num = int(num_str)
                res = int_to_base(num, to_b)
            else:
                num = base_to_int(num_str, from_b)
                res = int_to_base(num, to_b) if to_b != 10 else str(num)
            self.base_result.setPlainText(f"Результат: {res}")
        except Exception as e:
            self.base_result.setPlainText(f"Ошибка: {e}")

    # ========== КОНВЕРТЕР ==========
    def create_unit_converter_view(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.unit_category = QComboBox()  # ← Теперь QComboBox доступен!
        self.unit_category.addItems(list(UNITS.keys()))
        self.unit_value = QLineEdit()
        self.from_unit = QComboBox()
        self.to_unit = QComboBox()
        convert_btn = QPushButton("Конвертировать")
        convert_btn.clicked.connect(self.convert_units)
        self.unit_result = QTextEdit()
        self.unit_result.setReadOnly(True)
        self.unit_category.currentTextChanged.connect(self.update_unit_options)
        layout.addWidget(QLabel("Категория:"))
        layout.addWidget(self.unit_category)
        layout.addWidget(QLabel("Значение:"))
        layout.addWidget(self.unit_value)
        layout.addWidget(QLabel("Из:"))
        layout.addWidget(self.from_unit)
        layout.addWidget(QLabel("В:"))
        layout.addWidget(self.to_unit)
        layout.addWidget(convert_btn)
        layout.addWidget(self.unit_result)
        widget.setLayout(layout)
        self.content_layout.addWidget(widget)
        self.update_unit_options()

    def update_unit_options(self):
        cat = self.unit_category.currentText()
        units = list(UNITS[cat].keys())
        self.from_unit.clear()
        self.to_unit.clear()
        self.from_unit.addItems(units)
        self.to_unit.addItems(units)

    def convert_units(self):
        try:
            cat = self.unit_category.currentText()
            val = self.unit_value.text()
            from_u = self.from_unit.currentText()
            to_u = self.to_unit.currentText()
            res = convert_unit(cat, val, from_u, to_u)
            self.unit_result.setPlainText(f"= {res:.6g} {to_u}")
        except Exception as e:
            self.unit_result.setPlainText(f"Ошибка: {e}")

    # ========== 2D ГРАФИК ==========
    def create_plot2d_view(self):
        from math_tools.interactive_2d import Interactive2DPlot
        widget = Interactive2DPlot()
        self.content_layout.addWidget(widget)

    def plot_2d(self):
        try:
            plot_2d(self.plot2d_input.text())
        except Exception as e:
            self.plot2d_input.setText(f"Ошибка: {e}")

    # ========== 3D ГРАФИК ==========
    def create_plot3d_view(self):
        from math_tools.interactive_3d import Interactive3DPlot
        widget = Interactive3DPlot()
        self.content_layout.addWidget(widget)

    def plot_3d(self):
        try:
            plot_3d(self.plot3d_input.text())
        except Exception as e:
            self.plot3d_input.setText(f"Ошибка: {e}")

    # ========== МАТРИЦЫ ==========
    def create_matrix_view(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.mat_a = QLineEdit()
        self.mat_b = QLineEdit()
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Сложить")
        mult_btn = QPushButton("Умножить")
        det_btn = QPushButton("Опр. A")
        inv_btn = QPushButton("Обратн. A")
        add_btn.clicked.connect(lambda: self.matrix_op('add'))
        mult_btn.clicked.connect(lambda: self.matrix_op('mult'))
        det_btn.clicked.connect(lambda: self.matrix_op('det'))
        inv_btn.clicked.connect(lambda: self.matrix_op('inv'))
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(mult_btn)
        btn_layout.addWidget(det_btn)
        btn_layout.addWidget(inv_btn)
        self.matrix_result = QTextEdit()
        self.matrix_result.setReadOnly(True)
        layout.addWidget(QLabel("Матрица A: [[1,2],[3,4]]"))
        layout.addWidget(self.mat_a)
        layout.addWidget(QLabel("Матрица B (если нужно):"))
        layout.addWidget(self.mat_b)
        layout.addLayout(btn_layout)
        layout.addWidget(self.matrix_result)
        widget.setLayout(layout)
        self.content_layout.addWidget(widget)

    def matrix_op(self, op):
        try:
            A = self.mat_a.text()
            if op in ('add', 'mult'):
                B = self.mat_b.text()
                res = matrix_add(A, B) if op == 'add' else matrix_mult(A, B)
            elif op == 'det':
                res = matrix_det(A)
            elif op == 'inv':
                res = matrix_inv(A)
            self.matrix_result.setPlainText(str(res))
        except Exception as e:
            self.matrix_result.setPlainText(f"Ошибка: {e}")

    # ========== ИСТОРИЯ ==========
    def create_history_view(self):
        widget = QWidget()
        layout = QVBoxLayout()
        from core.calculator import get_history
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        hist = get_history()
        self.history_display.setPlainText("\n".join(hist))
        layout.addWidget(self.history_display)
        widget.setLayout(layout)
        self.content_layout.addWidget(widget)