import json
import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt

class VocabularyTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QLabel#title { font-size: 24px; font-weight: bold; }")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(50, 30, 50, 30)

        self.title = QLabel("📚 Từ vựng theo chủ đề")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)

        self.topic_selector = QComboBox()
        self.topic_selector.currentIndexChanged.connect(self.change_topic)

        self.word_list_widget = QListWidget()
        self.start_quiz_button = QPushButton("Bắt đầu Quiz")
        self.start_quiz_button.clicked.connect(self.start_quiz)

        self.mode_label = QLabel("Chế độ: Quiz")
        self.meaning_label = QLabel("Nghĩa tiếng Việt:")
        self.input_label = QLabel("Nhập từ tiếng Anh:")
        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.check_answer)

        self.result_label = QLabel("")
        self.submit_button = QPushButton("Kiểm tra")
        self.submit_button.clicked.connect(self.check_answer)
        self.skip_button = QPushButton("Bỏ qua")
        self.skip_button.clicked.connect(self.skip_word)

        self.layout.addWidget(self.title)
        self.layout.addWidget(QLabel("Chọn chủ đề:"))
        self.layout.addWidget(self.topic_selector)
        self.layout.addWidget(self.word_list_widget)
        self.layout.addWidget(self.start_quiz_button)
        self.layout.addWidget(self.mode_label)
        self.layout.addWidget(self.meaning_label)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.user_input)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.skip_button)

        self.setLayout(self.layout)

        with open("data/vocab.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.current_topic = None
        self.word_index = 0

        self.load_topics()
        self.set_quiz_visible(False)

    def load_topics(self):
        self.correct_words = []
        self.topic_selector.clear()
        for topic in self.data:
            self.topic_selector.addItem(topic["topic"])
        self.change_topic(0)

    def change_topic(self, index):
        self.current_topic = self.data[index]
        self.word_index = 0
        self.correct_words = []
        self.show_word_list()
        self.set_quiz_visible(False)

    def show_word_list(self):
        self.word_list_widget.clear()
        for word in self.current_topic["words"]:
            display = f"{word['word']} ({word['pronunciation']}) - {word['word_type']} - {word['meaning']}"
            self.word_list_widget.addItem(display)

    def start_quiz(self):
        self.set_quiz_visible(True)
        self.show_quiz()

    def set_quiz_visible(self, visible):
        for widget in [self.mode_label, self.meaning_label, self.input_label,
                       self.user_input, self.result_label, self.submit_button, self.skip_button]:
            widget.setVisible(visible)
        self.word_list_widget.setVisible(not visible)
        self.start_quiz_button.setVisible(not visible)

    def show_quiz(self):
        words = self.current_topic["words"]
        remaining_words = [word for word in words if word not in self.correct_words]

        if not remaining_words:
            self.meaning_label.setText("🎉 Bạn đã hoàn thành topic này!")
            self.user_input.setDisabled(True)
            self.submit_button.setDisabled(True)
            self.skip_button.setDisabled(True)
            self.result_label.setText(f"✅ Tổng đúng: {len(self.correct_words)}/{len(words)}")
            return

        self.user_input.setDisabled(False)
        self.submit_button.setDisabled(False)
        self.skip_button.setDisabled(False)

        self.current_word = random.choice(remaining_words)
        self.meaning_label.setText(f"Nghĩa tiếng Việt: {self.current_word['meaning']}")
        self.user_input.clear()
        self.result_label.setText("")

    def check_answer(self):
        user_answer = self.user_input.text().strip().lower()
        correct_answer = self.current_word["word"].strip().lower()

        if user_answer == correct_answer:
            self.result_label.setText("✅ Chính xác!")
            self.correct_words.append(self.current_word)
            self.show_quiz()
        else:
            self.result_label.setText("❌ Sai rồi! Thử lại hoặc bấm 'Bỏ qua'.")

    def skip_word(self):
        self.show_quiz()
