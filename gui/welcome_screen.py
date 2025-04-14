from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class WelcomeScreen(QWidget):
    def __init__(self, start_callback):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        banner = QLabel()
        banner.setAlignment(Qt.AlignCenter)
        banner.setPixmap(QPixmap("assets/banner.png").scaledToWidth(600))
        layout.addWidget(banner)

        start_button = QPushButton("Start")
        start_button.clicked.connect(start_callback)
        layout.addWidget(start_button)

        self.setLayout(layout)
