# from gui.ui import ui_config
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
# from PyQt5.QtCore import Qt, QSize
# from PyQt5.QtGui import QPixmap
#
# class WelcomeScreen(QWidget):
#     def __init__(self, start_callback):
#         super().__init__()
#         self.setStyleSheet(ui_config.app_stylesheet)
#         self.layout = QVBoxLayout(self)
#         self.layout.setAlignment(Qt.AlignCenter)
#
#         self.banner = QLabel()
#         self.banner.setAlignment(Qt.AlignCenter)
#         self.banner.setPixmap(QPixmap("assets/banner.png").scaledToWidth(600, Qt.SmoothTransformation))
#         self.banner.setContentsMargins(20, 20, 20, 20)  # Add padding around the image
#         self.layout.addWidget(self.banner)
#
#         self.start_button = QPushButton("Start")
#         self.start_button.clicked.connect(start_callback)
#         self.layout.addWidget(self.start_button)
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QPixmap
#
# class WelcomeScreen(QWidget):
#     def __init__(self, start_callback):
#         super().__init__()
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignCenter)
#
#         banner = QLabel()
#         banner.setAlignment(Qt.AlignCenter)
#         banner.setPixmap(QPixmap("assets/banner.png").scaledToWidth(600))
#         layout.addWidget(banner)
#
#         start_button = QPushButton("Start")
#         start_button.clicked.connect(start_callback)
#         layout.addWidget(start_button)
#
#         self.setLayout(layout)
from gui.ui import ui_config
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap

class WelcomeScreen(QWidget):
    def __init__(self, start_callback):
        super().__init__()
        self.setStyleSheet(ui_config.app_stylesheet)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.banner = QLabel()
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setPixmap(QPixmap("Img/banner.png").scaledToWidth(700, Qt.SmoothTransformation))
        self.banner.setContentsMargins(20, 20, 20, 20)  # Add padding around the image
        self.layout.addWidget(self.banner)

        self.start_button = QPushButton("Start")
        self.start_button.setContentsMargins(30, 15, 30, 15)
        self.start_button.clicked.connect(start_callback)
        self.layout.addWidget(self.start_button)
        self.start_button.setFixedWidth(200)

