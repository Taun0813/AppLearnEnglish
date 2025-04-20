import os
import json
import tempfile
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout, QLabel, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox, QApplication, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal, QSize
from gui.ui import ui_config
import sounddevice as sd
import soundfile as sf
from PyQt5.QtGui import QIcon

class RecorderThread(QThread):
    recording_done = pyqtSignal(str)

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def run(self):
        try:
            # Ghi âm và lưu vào file tạm thời
            audio = sd.rec(int(self.duration * 44100), samplerate=44100, channels=1, dtype='float32')
            sd.wait(timeout=self.duration + 1)  # Add timeout to avoid indefinite waiting
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                audio_path = temp_file.name
                try:
                    sf.write(audio_path, audio, 44100)  # No subtype needed for float32
                except Exception as e:
                    print(f"Error writing to temporary file: {e}")
                    self.recording_done.emit(None)
                    return
                self.recording_done.emit(audio_path)
        except sd.PortAudioError as e:
            print(f"Error with sounddevice: {e}")
            self.recording_done.emit(None)
        except Exception as e:
            print(f"An unexpected error occurred: {type(e).__name__} - {e}")
            self.recording_done.emit(None)


class SpeakingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_topics()
        self.current_topic_data = None
        self.current_sentence_index = 0
        self.score_list = []  # Initialize score list
        self.recorder_thread = None  # Initialize recorder_thread
        self.sentence_count = 0
        self.current_sentence_progress = 0

    def initUI(self):
        # main_layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)  # Reduce margins
        main_layout.setSpacing(15)
        # Create a QFrame for the border
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLineWidth(1)
        frame.setStyleSheet("QFrame { border: 1px solid #ccc; }")  # Light gray border

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)  # Add padding inside the frame
        frame_layout.setSpacing(10)

        # Title layout
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)  # Center align
        title_icon = QLabel("🗣️")
        title_icon.setStyleSheet(ui_config.title_style)
        title_label = QLabel("Luyện Nói Theo Chủ Đề")
        title_label.setStyleSheet(ui_config.title_style)
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        frame_layout.addLayout(title_layout)

        # Topic layout
        topic_layout = QHBoxLayout()
        topic_label = QLabel("Chủ đề:")
        topic_label.setStyleSheet("font-weight: bold; margin-right: 10px;")
        topic_layout.addWidget(topic_label)
        self.topic_combobox = QComboBox()
        self.topic_combobox.currentIndexChanged.connect(self.on_topic_selected)
        self.topic_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        topic_layout.addWidget(self.topic_combobox)
        topic_layout.addStretch()
        frame_layout.addLayout(topic_layout)

        # Dialogue label
        self.dialogue_label = QLabel('Câu hội thoại sẽ hiển thị ở đây.')
        self.dialogue_label.setAlignment(Qt.AlignCenter)
        self.dialogue_label.setWordWrap(True)
        self.dialogue_label.setStyleSheet(ui_config.app_stylesheet + "font-size: 14px; background-color: #E0E0E0; padding: 10px;")
        frame_layout.addWidget(self.dialogue_label)

        # Button layout
        button_layout = QHBoxLayout()
        self.next_button = QPushButton("Bắt Đầu")  # Change text
        self.next_button.clicked.connect(self.next_pair)
        button_layout.addWidget(self.next_button)
        frame_layout.addLayout(button_layout)

        # Score and Feedback layout
        score_feedback_layout = QGridLayout()
        self.score_icon = QLabel()
        self.score_icon.setPixmap(QIcon("./icons/score.png").pixmap(QSize(24, 24)))
        score_label = QLabel("Điểm số:")
        score_label.setStyleSheet("font-weight: bold;")
        self.score_label = QLabel('')
        self.feedback_icon = QLabel()
        self.feedback_icon.setPixmap(QIcon("./icons/feedback.png").pixmap(QSize(24, 24)))
        feedback_label = QLabel("Nhận xét:")
        feedback_label.setStyleSheet("font-weight: bold;")
        self.feedback_label = QLabel('')
        score_feedback_layout.addWidget(self.score_icon, 0, 0)
        score_feedback_layout.addWidget(score_label, 0, 1)
        score_feedback_layout.addWidget(self.score_label, 0, 2)
        score_feedback_layout.addWidget(self.feedback_icon, 1, 0)
        score_feedback_layout.addWidget(feedback_label, 1, 1)
        score_feedback_layout.addWidget(self.feedback_label, 1, 2)
        frame_layout.addLayout(score_feedback_layout)

        # Progress label
        self.progress_label = QLabel('')
        self.progress_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.progress_label)

        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def load_topics(self):
        with open("data/speaking.json", "r", encoding="utf-8") as f:
            self.speaking_data = json.load(f)
        for url, data in self.speaking_data.items():
            self.topic_combobox.addItem(data["topic"], url)

    @pyqtSlot()
    def on_topic_selected(self):
        selected_url = self.topic_combobox.currentData()
        if selected_url:
            try:
                self.current_topic_data = self.speaking_data[selected_url]
                self.sentence_count = len(self.current_topic_data['dialogue'])
                self.current_sentence_index = 0
                self.score_list = []
                self.dialogue_label.setText('Câu hội thoại sẽ hiển thị ở đây.')
                self.score_label.setText('')
                self.feedback_label.setText('')
                self.update_progress_label()
                self.next_button.setText('Tiếp Tục')
            except KeyError as e:
                QMessageBox.critical(self, 'Lỗi', f'Không tìm thấy dữ liệu cho chủ đề: {e}')
            except Exception as e:
                QMessageBox.critical(self, 'Lỗi', f'Lỗi khi tải chủ đề: {e}')

    def update_progress_label(self):
        if self.current_topic_data:
            progress = min(self.current_sentence_index, self.sentence_count)
            self.progress_label.setText(f'Câu {progress // 2 + 1}/{self.sentence_count // 2}')
        else:
            self.progress_label.setText('')

    def next_pair(self):
        if not self.current_topic_data:
            return

        while True:
            if self.current_sentence_index >= len(self.current_topic_data['dialogue']) - 1:
                self.summarize_results()
                return

            try:
                # Check index before accessing list
                if (self.current_sentence_index < 0 or self.current_sentence_index >= len(
                        self.current_topic_data['dialogue']) or
                        self.current_sentence_index + 1 < 0 or self.current_sentence_index + 1 >= len(
                            self.current_topic_data['dialogue'])):
                    raise IndexError('Index out of range')

                sentence_a = self.current_topic_data['dialogue'][self.current_sentence_index]
                sentence_b = self.current_topic_data['dialogue'][self.current_sentence_index + 1]

                if sentence_a['speaker'] == 'A' and sentence_b['speaker'] == 'B':
                    self.current_sentence_progress += 1
                    self.update_progress_label()

                    # Hiển thị đoạn hội thoại
                    self.dialogue_label.setText(f'👤 A: {sentence_a["text"]}\n🧑 Bạn hãy nói: "{sentence_b["text"]}"')
                    # Ghi âm người dùng nói theo câu B trong thread riêng
                    self.score_label.setText('🎙️ Đang ghi âm...')
                    QApplication.processEvents()  # Process events once before recording

                    self.recorder_thread = RecorderThread(duration=5)  # Keep duration as 5 seconds for now
                    self.recorder_thread.recording_done.connect(self.on_recording_done)
                    self.recorder_thread.start()
                    return  # Break out of the loop after starting recording
                else:
                    self.current_sentence_index += 1

            except (IndexError, KeyError) as e:
                QMessageBox.critical(self, 'Lỗi', f'Lỗi khi xử lý cặp câu: {type(e).__name__} - {e}')
                return
            except Exception as e:
                QMessageBox.critical(self, 'Lỗi', f'Lỗi không xác định khi xử lý cặp câu: {type(e).__name__} - {e}')
                return

    def on_recording_done(self, audio_path):
        if self.recorder_thread:
            self.recorder_thread.quit()
            self.recorder_thread.wait()
            self.recorder_thread = None

        if not audio_path:
            self.feedback_label.setText('Ghi âm không thành công.')
            return

        try:
            import core.speech_assessment as speech_assessment  # Import here
            sentence_b = self.current_topic_data['dialogue'][self.current_sentence_index + 1]
            reference_text = sentence_b['text']
            result = speech_assessment.evaluate(audio_path, reference_text)
            self.score_list.append(result['score'])
            self.score_label.setText(f'{result["score"]}')
            self.feedback_label.setText(f'{result["feedback"]} ({result["user_text"]})')
            os.remove(audio_path)
            self.current_sentence_index += 2
        except Exception as e:  # Catch any exception during evaluation
            QMessageBox.warning(self, 'Lỗi', f'Không thể đánh giá: {type(e).__name__} - {e}')

    def summarize_results(self):
        total_score = sum(self.score_list)
        average_score = total_score / len(self.score_list) if self.score_list else 0
        QMessageBox.information(
            self, "Kết quả",
            f"Bạn đã hoàn thành chủ đề này!\nĐiểm trung bình: {average_score:.2f}"
        )
        self.on_topic_selected()  # Reset UI for new topic
