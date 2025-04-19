from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot
import json
import core.speech_assessment as speech_assessment  # Assume this module exists
import time


class SpeakingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_topics()
        self.current_topic_data = None
        self.current_sentence_index = 0
        self.score_list = []
        self.dialogue = []

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        # Title
        title_label = QLabel("🗣️ Luyện Nói Theo Chủ Đề")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Topic selection
        topic_layout = QHBoxLayout()
        topic_label = QLabel("Chọn chủ đề:")
        self.topic_combobox = QComboBox()
        self.topic_combobox.currentIndexChanged.connect(self.on_topic_selected)
        topic_layout.addWidget(topic_label)
        topic_layout.addWidget(self.topic_combobox)
        main_layout.addLayout(topic_layout)

        # Sentence display
        self.sentence_label = QLabel("Câu hội thoại sẽ hiển thị ở đây.")
        self.sentence_label.setAlignment(Qt.AlignCenter)
        self.sentence_label.setWordWrap(True)
        self.sentence_label.setStyleSheet("font-size: 18px;")
        main_layout.addWidget(self.sentence_label)

        # Buttons
        button_layout = QHBoxLayout()
        self.next_button = QPushButton("Câu Tiếp Theo")
        self.next_button.clicked.connect(self.next_sentence)
        button_layout.addWidget(self.next_button)
        main_layout.addLayout(button_layout)

        self.score_label = QLabel("Điểm số: ")
        main_layout.addWidget(self.score_label)

        self.feedback_label = QLabel("Nhận xét: ")
        main_layout.addWidget(self.feedback_label)

        self.setLayout(main_layout)

    def load_topics(self):
        with open("data/speaking.json", "r", encoding="utf-8") as f:
            self.speaking_data = json.load(f)
        for url, data in self.speaking_data.items():
            self.topic_combobox.addItem(data["topic"], url)

    @pyqtSlot()
    def on_topic_selected(self):
        selected_url = self.topic_combobox.currentData()
        self.current_topic_data = self.speaking_data[selected_url]
        self.current_sentence_index = 0
        self.display_sentence()

    def display_sentence(self):
        if not self.current_topic_data:
            return

        if self.current_sentence_index >= len(self.current_topic_data["dialogue"]):
            self.summarize_results()
            return

        sentence_data = self.current_topic_data["dialogue"][self.current_sentence_index]

        if sentence_data["speaker"] == "B":
            self.sentence_label.setText(f"Bạn: {sentence_data['text']}")

    def next_sentence(self):
        if not self.current_topic_data:
            return

        if self.current_sentence_index >= len(self.current_topic_data["dialogue"]):
            self.summarize_results()
            return

        sentence_data = self.current_topic_data["dialogue"][self.current_sentence_index]
        if sentence_data["speaker"] == "A":
            print(sentence_data["text"])
            # ... (Play the audio for speaker A)
            audio_data = "..."
            sentence_data = self.current_topic_data["dialogue"][self.current_sentence_index + 1]
            # ... (Record the user's response for speaker B)
            user_audio_data = "..."
            result = speech_assessment.assess_pronunciation(user_audio_data, sentence_data["text"])
            self.score_list.append(result['score'])
            self.feedback_label.setText(f"Nhận xét: {result['feedback']}")
            self.score_label.setText(f"Điểm số: {result['score']}")
        else:
            print("Chờ câu A")

        self.current_sentence_index += 1
        self.display_sentence()

    def summarize_results(self):
        total_score = sum(self.score_list)
        average_score = total_score / len(self.score_list) if self.score_list else 0
        QMessageBox.information(self, "Kết quả", f"Bạn đã hoàn thành chủ đề này!\nĐiểm trung bình: {average_score:.2f}")
        self.score_list = []
        self.current_sentence_index = 0
        self.on_topic_selected()
        self.feedback_label.setText("Nhận xét: ")
        self.score_label.setText("Điểm số: ")

