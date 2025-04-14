from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class ListeningTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)

        title = QLabel("🎧 Luyện Nghe")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.start_button = QPushButton("Bắt đầu luyện nghe")
        self.start_button.clicked.connect(self.start_listening)

        layout.addWidget(title)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def start_listening(self):
        print("Listening started...")
