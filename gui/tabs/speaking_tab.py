import os
import json
import tempfile

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal

import sounddevice as sd
import soundfile as sf

import core.speech_assessment as speech_assessment


class RecorderThread(QThread):
    recording_done = pyqtSignal(str)

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def run(self):
        try:
            # Ghi âm và lưu vào file tạm thời
            audio = sd.rec(int(self.duration * 44100), samplerate=44100, channels=1)
            sd.wait()
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            sf.write(audio_path, audio, 44100)
            self.recording_done.emit(audio_path)
        except Exception as e:
            print(f"Error while recording: {e}")
            self.recording_done.emit(None)


class SpeakingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_topics()
        self.current_topic_data = None
        self.current_sentence_index = 0
        self.score_list = []

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        title_label = QLabel("🗣️ Luyện Nói Theo Chủ Đề")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_label)

        topic_layout = QHBoxLayout()
        topic_label = QLabel("Chọn chủ đề:")
        self.topic_combobox = QComboBox()
        self.topic_combobox.currentIndexChanged.connect(self.on_topic_selected)
        topic_layout.addWidget(topic_label)
        topic_layout.addWidget(self.topic_combobox)
        main_layout.addLayout(topic_layout)

        self.dialogue_label = QLabel("Câu hội thoại sẽ hiển thị ở đây.")
        self.dialogue_label.setAlignment(Qt.AlignCenter)
        self.dialogue_label.setWordWrap(True)
        self.dialogue_label.setStyleSheet("font-size: 18px;")
        main_layout.addWidget(self.dialogue_label)

        button_layout = QHBoxLayout()
        self.next_button = QPushButton("Bắt đầu")
        self.next_button.clicked.connect(self.next_pair)
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
        self.score_list = []
        self.dialogue_label.setText("Câu hội thoại sẽ hiển thị ở đây.")
        self.score_label.setText("Điểm số: ")
        self.feedback_label.setText("Nhận xét: ")
        self.next_button.setText("Bắt đầu")

    def next_pair(self):
        if not self.current_topic_data:
            return

        if self.current_sentence_index >= len(self.current_topic_data["dialogue"]) - 1:
            self.summarize_results()
            return

        try:
            # Lấy cặp hội thoại tiếp theo: A → B
            sentence_a = self.current_topic_data["dialogue"][self.current_sentence_index]
            sentence_b = self.current_topic_data["dialogue"][self.current_sentence_index + 1]

            if sentence_a["speaker"] == "A" and sentence_b["speaker"] == "B":
                # Hiển thị đoạn hội thoại
                self.dialogue_label.setText(
                    f"👤 A: {sentence_a['text']}\n🧑 Bạn hãy nói: \"{sentence_b['text']}\""
                )
                QApplication.processEvents()

                # Ghi âm người dùng nói theo câu B trong thread riêng
                self.score_label.setText("🎙️ Đang ghi âm...")
                QApplication.processEvents()

                self.recorder_thread = RecorderThread(duration=5)  # duration là 5 giây
                self.recorder_thread.recording_done.connect(self.on_recording_done)
                self.recorder_thread.start()

            else:
                self.current_sentence_index += 1
                self.next_pair()

        except Exception as e:
            print("❌ Lỗi khi xử lý:", e)
            self.feedback_label.setText("Lỗi khi xử lý cặp câu.")

    def on_recording_done(self, audio_path):
        if audio_path:
            try:
                sentence_b = self.current_topic_data["dialogue"][self.current_sentence_index + 1]
                reference_text = sentence_b["text"]
                result = speech_assessment.evaluate(audio_path, reference_text)

                score = result["score"]
                feedback = result["feedback"]
                user_text = result["user_text"]

                self.score_list.append(score)
                self.score_label.setText(f"Điểm số: {score}")
                self.feedback_label.setText(f"Nhận xét: {feedback} ({user_text})")

                os.remove(audio_path)  # Xoá file sau khi sử dụng
                self.current_sentence_index += 2

            except Exception as e:
                print("❌ Lỗi khi đánh giá:", e)
                self.feedback_label.setText("Không thể đánh giá.")
        else:
            self.feedback_label.setText("Ghi âm không thành công.")

        self.next_pair()

    def summarize_results(self):
        total_score = sum(self.score_list)
        average_score = total_score / len(self.score_list) if self.score_list else 0
        QMessageBox.information(
            self, "Kết quả",
            f"Bạn đã hoàn thành chủ đề này!\nĐiểm trung bình: {average_score:.2f}"
        )
        self.on_topic_selected()
