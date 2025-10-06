# ui/sidebar.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QScrollArea,
    QHBoxLayout, QLabel
)
from PyQt5.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)  # Увеличили ширину
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Заголовок
        title = QLabel("Модули")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        self.buttons = {}
        modules = [
            ("Калькулятор", "calc"),
            ("Уравнения", "eq"),
            ("Системы сч.", "base"),
            ("Конвертер", "units"),
            ("2D График", "plot2d"),
            ("3D График", "plot3d"),
            ("Матрицы", "matrix"),
            ("История", "history")
        ]

        for name, key in modules:
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self.module_selected(k))
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    padding: 12px 20px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    background-color: #f0f0f0;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QPushButton:checked {
                    background-color: #bbdefb;
                    border: 2px solid #2196f3;
                }
            """)
            self.buttons[key] = btn
            layout.addWidget(btn)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def module_selected(self, module_key):
        # Снимаем выделение со всех кнопок
        for key, btn in self.buttons.items():
            if key != module_key:
                btn.setChecked(False)
        # Сигнал вверх
        if hasattr(self, 'on_module_select'):
            self.on_module_select(module_key)