# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFont
# from gui.ui import ui_config
#
# class MenuScreen(QWidget):
#     def __init__(self, button_callback):
#         super().__init__()
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignCenter)
#
#         title = QLabel("Welcome to English Learning App")
#         title.setFont(ui_config.menu_title_font)
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet(ui_config.title_style+"color: #5D7B6F; margin-bottom: 40px;")
#         layout.addWidget(title, alignment=Qt.AlignCenter)
#
#         buttons = ["Chat AI", "Listening", "Speaking", "Vocabulary"]
#         for i, name in enumerate(buttons):
#             btn = QPushButton(name)
#             btn.setFixedWidth(300)
#             btn.clicked.connect(lambda _, idx=i: button_callback(idx))
#             layout.addWidget(btn)
#             layout.setSpacing(20)
#
#         self.setLayout(layout)
#
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from gui.ui import ui_config


class MenuScreen(QWidget):
    def __init__(self, button_callback):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome to English Learning App")
        title.setFont(ui_config.menu_title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            ui_config.title_style + "color: #5D7B6F; margin-bottom: 40px;"
        )
        self.layout.addWidget(title, alignment=Qt.AlignCenter)

        buttons = ["Chat AI", "Listening", "Speaking", "Vocabulary"]
        for i, name in enumerate(buttons):
            btn = QPushButton(name)
            btn.setFixedWidth(300)
            btn.clicked.connect(lambda _, idx=i: button_callback(idx))
            btn.setStyleSheet("padding: 15px; margin-bottom: 10px;")
            self.layout.addWidget(btn)
            self.layout.setSpacing(20)

        self.setLayout(self.layout)
