# math_tools/interactive_2d.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import re

class Interactive2DPlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ввод функции
        input_layout = QHBoxLayout()
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText("f(x) = x**2, sin(x), log(x) и т.д.")
        self.plot_btn = QPushButton("Построить")
        self.plot_btn.clicked.connect(self.plot)
        input_layout.addWidget(QLabel("Функция:"))
        input_layout.addWidget(self.expr_input)
        input_layout.addWidget(self.plot_btn)
        layout.addLayout(input_layout)

        # Поиск точки
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите X или Y")
        self.search_mode = "x"  # 'x' или 'y'
        self.mode_btn = QPushButton("Режим: X")
        self.mode_btn.clicked.connect(self.toggle_search_mode)
        self.find_btn = QPushButton("Найти")
        self.find_btn.clicked.connect(self.find_point)
        self.point_label = QLabel("Точка: —")
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.mode_btn)
        search_layout.addWidget(self.find_btn)
        search_layout.addWidget(self.point_label)
        layout.addLayout(search_layout)

        # График
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.ax = self.figure.add_subplot(111)
        self.current_expr = ""
        self.x_data = None
        self.y_data = None

    def toggle_search_mode(self):
        if self.search_mode == "x":
            self.search_mode = "y"
            self.mode_btn.setText("Режим: Y")
            self.search_input.setPlaceholderText("Введите Y")
        else:
            self.search_mode = "x"
            self.mode_btn.setText("Режим: X")
            self.search_input.setPlaceholderText("Введите X")

    def plot(self):
        expr = self.expr_input.text().strip()
        if not expr:
            return

        self.current_expr = expr
        self.ax.clear()

        expr_safe = expr.replace('^', '**')
        expr_safe = re.sub(r'\b(ln|log10|sqrt|sin|cos|tan|asin|acos|atan|sinh|cosh|tanh)\b', r'np.\1', expr_safe)
        expr_safe = expr_safe.replace('pi', 'np.pi').replace('e', 'np.e')

        try:
            x = np.linspace(-50, 50, 5000)
            safe_dict = {"np": np, "__builtins__": {}}
            y = eval(expr_safe, safe_dict, {"x": x})
            mask = np.isfinite(y)
            self.x_data = x[mask]
            self.y_data = y[mask]
            self.ax.plot(self.x_data, self.y_data, 'b-', linewidth=1.5)
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.set_xlim(-10, 10)
            self.ax.set_ylim(-10, 10)
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Ошибка: {e}", transform=self.ax.transAxes,
                         ha='center', va='center', fontsize=12, color='red')

        self.canvas.draw()

    def find_point(self):
        if self.x_data is None:
            self.point_label.setText("Сначала постройте график!")
            return

        try:
            val = float(self.search_input.text())
            if self.search_mode == "x":
                # Найти ближайшую точку по X
                idx = (np.abs(self.x_data - val)).argmin()
                x_found = self.x_data[idx]
                y_found = self.y_data[idx]
                self.point_label.setText(f"Точка: ({x_found:.4f}, {y_found:.4f})")
                self.ax.plot(x_found, y_found, 'ro', markersize=8)
            else:
                # Найти все точки, где y ≈ val (простой поиск)
                tol = 0.1
                indices = np.where(np.abs(self.y_data - val) < tol)[0]
                if len(indices) > 0:
                    x_found = self.x_data[indices[0]]
                    y_found = self.y_data[indices[0]]
                    self.point_label.setText(f"Точка: ({x_found:.4f}, {y_found:.4f})")
                    self.ax.plot(x_found, y_found, 'go', markersize=8)
                else:
                    self.point_label.setText("Точка не найдена")
            self.canvas.draw()
        except Exception as e:
            self.point_label.setText(f"Ошибка: {e}")