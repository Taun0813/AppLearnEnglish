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
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap


class WelcomeScreen(QWidget):
    def __init__(self, start_callback):
        super().__init__()
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #5D7B6F;
                color: white;
                font-size: 18px;
                padding: 12px 24px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #B0D4B8;
                color: #333;
            }
        """
        )  # Apply button styles
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.banner = QLabel()
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setPixmap(QPixmap("assets/banner.png").scaledToWidth(600, Qt.SmoothTransformation))
        self.banner.setContentsMargins(20, 20, 20, 20)  # Add padding around the image
        self.layout.addWidget(self.banner)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(start_callback)
        self.layout.addWidget(self.start_button)
