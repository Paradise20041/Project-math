# main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def apply_global_style(app):
    app.setStyleSheet("""
        QWidget { font-size: 16px; }
        QPushButton {
            font-size: 18px;
            padding: 14px 24px;
            border-radius: 10px;
            background-color: #e3f2fd;
        }
        QPushButton:hover { background-color: #bbdefb; }
        QLineEdit, QTextEdit, QComboBox {
            font-size: 16px;
            padding: 10px;
            border: 2px solid #90caf9;
            border-radius: 8px;
        }
        QLabel { font-size: 16px; }
    """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_global_style(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())