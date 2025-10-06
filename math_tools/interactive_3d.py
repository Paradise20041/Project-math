# math_tools/interactive_3d.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import re

class Interactive3DPlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText("f(x,y) = x**2 + y**2, sin(x)*cos(y) и т.д.")
        self.plot_btn = QPushButton("Построить 3D")
        self.plot_btn.clicked.connect(self.plot)
        input_layout.addWidget(QLabel("Функция:"))
        input_layout.addWidget(self.expr_input)
        input_layout.addWidget(self.plot_btn)
        layout.addLayout(input_layout)

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.ax = None

    def plot(self):
        expr = self.expr_input.text().strip()
        if not expr:
            return

        expr_safe = expr.replace('^', '**')
        expr_safe = re.sub(r'\b(sin|cos|tan|sqrt|log|exp)\b', r'np.\1', expr_safe)
        expr_safe = expr_safe.replace('pi', 'np.pi').replace('e', 'np.e')

        try:
            self.figure.clear()
            self.ax = self.figure.add_subplot(111, projection='3d')

            x = np.linspace(-5, 5, 50)
            y = np.linspace(-5, 5, 50)
            X, Y = np.meshgrid(x, y)
            safe_dict = {"np": np, "__builtins__": {}}
            Z = eval(expr_safe, safe_dict, {"x": X, "y": Y})

            surf = self.ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')
            self.figure.colorbar(surf, ax=self.ax, shrink=0.5)
        except Exception as e:
            self.ax = self.figure.add_subplot(111)
            self.ax.text(0.5, 0.5, f"Ошибка: {e}", transform=self.ax.transAxes,
                         ha='center', va='center', fontsize=12, color='red')

        self.canvas.draw()