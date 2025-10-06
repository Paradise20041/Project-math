# ui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QHBoxLayout, QWidget, QPushButton, QToolBar
)
from PyQt5.QtCore import Qt
from ui.sidebar import Sidebar
from ui.calculator_widget import CalculatorWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project-math")
        self.setGeometry(100, 100, 1100, 700)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Сайдбар СЛЕВА
        self.sidebar = Sidebar()
        self.sidebar.on_module_select = self.calculator_widget_switch_to
        self.sidebar.hide()
        main_layout.addWidget(self.sidebar)

        # Контент справа
        self.calculator_widget = CalculatorWidget()
        main_layout.addWidget(self.calculator_widget)

        central.setLayout(main_layout)

        # Тулбар
        toolbar = QToolBar("Меню")
        self.addToolBar(toolbar)
        menu_btn = QPushButton("≡")
        menu_btn.setFixedSize(40, 40)
        menu_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        menu_btn.clicked.connect(self.toggle_sidebar)
        toolbar.addWidget(menu_btn)

    def calculator_widget_switch_to(self, module):
        self.calculator_widget.switch_to(module)

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_M:
            self.toggle_sidebar()
        else:
            super().keyPressEvent(event)