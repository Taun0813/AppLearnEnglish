# import os
# import json
# import tempfile
# from PyQt5.QtWidgets import (
#     QWidget,
#     QVBoxLayout, QLabel, QComboBox,
#     QPushButton, QHBoxLayout, QMessageBox, QApplication
# )
# from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
#
# import sounddevice as sd
# import soundfile as sf
#
#
# class RecorderThread(QThread):
#     recording_done = pyqtSignal(str)
#
#     def __init__(self, duration):
#         super().__init__()
#         self.duration = duration
#
#     def run(self):
#         print('RecorderThread: run() - Starting')
#         try:
#             print('RecorderThread: run() - Recording...')
#             audio = sd.rec(int(self.duration * 44100), samplerate=44100, channels=1, dtype='float32')
#             print('RecorderThread: run() - Recording in progress, waiting...')
#             sd.wait() #remove timeout
#             print('RecorderThread: run() - Recording finished.')
#             audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
#             print(f'RecorderThread: run() - Saving to: {audio_path}')
#             sf.write(audio_path, audio, 44100)
#             print(f'RecorderThread: run() - audio save complete')
#             self.recording_done.emit(audio_path)
#             print('RecorderThread: run() - recording done emit')
#         except sd.PortAudioError as e:
#             print(f'RecorderThread: run() - PortAudioError: {e}')
#             self.recording_done.emit(None)
#         except Exception as e:
#             print(f'RecorderThread: run() - An unexpected error occurred: {type(e).__name__} - {e}')
#             self.recording_done.emit(None)
#         print('RecorderThread: run() - Exiting')
#
#
# class SpeakingTab(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.load_topics()
#         self.current_topic_data = None
#         self.current_sentence_index = 0
#         self.score_list = []  # Initialize score list
#         self.recorder_thread = None  # Initialize recorder_thread
#         self.sentence_count = 0
#         self.current_sentence_progress = 0
#
#     # UI initialization (no changes needed in this section, but kept for completeness)
#     # ...
#     def initUI(self):
#         main_layout = QVBoxLayout()
#         main_layout.setContentsMargins(50, 30, 50, 30)
#         main_layout.setSpacing(20)
#
#         title_label = QLabel("🗣️ Luyện Nói Theo Chủ Đề")
#         title_label.setAlignment(Qt.AlignCenter)
#         title_label.setStyleSheet('font-size: 24px; font-weight: bold;')
#         main_layout.addWidget(title_label)
#
#         topic_layout = QHBoxLayout()
#         topic_label = QLabel("Chọn chủ đề:")
#         self.topic_combobox = QComboBox()
#         self.topic_combobox.currentIndexChanged.connect(self.on_topic_selected)
#         topic_layout.addWidget(topic_label)
#         topic_layout.addWidget(self.topic_combobox)
#         main_layout.addLayout(topic_layout)
#
#         self.dialogue_label = QLabel('Câu hội thoại sẽ hiển thị ở đây.')
#         self.dialogue_label.setAlignment(Qt.AlignCenter)
#         self.dialogue_label.setWordWrap(True)
#         self.dialogue_label.setStyleSheet('font-size: 18px;')
#         main_layout.addWidget(self.dialogue_label)
#
#         button_layout = QHBoxLayout()
#         self.next_button = QPushButton("Bắt đầu")
#         self.next_button.clicked.connect(self.next_pair)
#         button_layout.addWidget(self.next_button)
#         main_layout.addLayout(button_layout)
#
#         self.score_label = QLabel('Điểm số: ')
#         main_layout.addWidget(self.score_label)
#
#         self.feedback_label = QLabel('Nhận xét: ')
#         main_layout.addWidget(self.feedback_label)
#
#         self.progress_label = QLabel('')  # Label to display progress
#         main_layout.addWidget(self.progress_label)
#         self.setLayout(main_layout)
#
#     def load_topics(self):
#         print('load_topics - Starting')
#         try:
#             with open("data/speaking.json", "r", encoding="utf-8") as f:
#                 self.speaking_data = json.load(f)
#             for url, data in self.speaking_data.items():
#                 self.topic_combobox.addItem(data["topic"], url)
#             print('load_topics - Finished')
#         except Exception as e:
#             print(f'load_topics - error: {e}')
#
#     @pyqtSlot()
#     def on_topic_selected(self):
#         print('on_topic_selected - Starting')
#         selected_url = self.topic_combobox.currentData()
#         if selected_url:
#             try:
#                 self.current_topic_data = self.speaking_data[selected_url]
#                 self.sentence_count = len(self.current_topic_data['dialogue'])
#                 self.current_sentence_index = 0
#                 self.score_list = []
#                 self.dialogue_label.setText('Câu hội thoại sẽ hiển thị ở đây.')
#                 self.score_label.setText('Điểm số: ')
#                 self.feedback_label.setText('Nhận xét: ')
#                 self.update_progress_label()  # Initial progress display
#                 self.next_button.setText('Tiếp Tục')
#                 print('on_topic_selected - Finished')
#             except KeyError as e:
#                 QMessageBox.critical(self, 'Lỗi', f'Không tìm thấy dữ liệu cho chủ đề: {e}')
#             except Exception as e:
#                 QMessageBox.critical(self, 'Lỗi', f'Lỗi khi tải chủ đề: {e}')
#         else:
#             print('on_topic_selected - nothing selected')
#
#     def update_progress_label(self):
#         if self.current_topic_data:
#             progress = min(self.current_sentence_index, self.sentence_count)  # Cap progress
#             self.progress_label.setText(f'Câu {progress // 2 + 1}/{self.sentence_count // 2}')
#         else:
#             self.progress_label.setText('')
#
#     def next_pair(self):
#         print('next_pair - Starting')
#         if not self.current_topic_data:
#             print('next_pair - No topic data')
#             return
#
#         while True:
#             if self.current_sentence_index >= len(self.current_topic_data['dialogue']) - 1:
#                 print('next_pair - summarize_results')
#                 self.summarize_results()
#                 return
#
#             try:
#                 # Check index before accessing list
#                 if (self.current_sentence_index < 0 or self.current_sentence_index >= len(
#                         self.current_topic_data['dialogue']) or
#                         self.current_sentence_index + 1 < 0 or self.current_sentence_index + 1 >= len(
#                             self.current_topic_data['dialogue'])):
#                     raise IndexError('Index out of range')
#
#                 sentence_a = self.current_topic_data['dialogue'][self.current_sentence_index]
#                 sentence_b = self.current_topic_data['dialogue'][self.current_sentence_index + 1]
#
#                 if sentence_a['speaker'] == 'A' and sentence_b['speaker'] == 'B':
#                     self.current_sentence_progress += 1
#                     self.update_progress_label()
#
#                     # Hiển thị đoạn hội thoại
#                     self.dialogue_label.setText(f'👤 A: {sentence_a["text"]}\n🧑 Bạn hãy nói: "{sentence_b["text"]}"')
#                     # Ghi âm người dùng nói theo câu B trong thread riêng
#                     self.score_label.setText('🎙️ Đang ghi âm...')
#                     QApplication.processEvents()  # Process events once before recording
#
#                     self.recorder_thread = RecorderThread(duration=5)  # Keep duration as 5 seconds for now
#                     self.recorder_thread.recording_done.connect(self.on_recording_done)
#                     self.recorder_thread.start()
#                     print('next_pair - Recording started')
#                     return  # Break out of the loop after starting recording
#                 else:
#                     self.current_sentence_index += 1
#                     print('next_pair - Wrong speakers, try next')
#
#             except (IndexError, KeyError) as e:
#                 QMessageBox.critical(self, 'Lỗi', f'Lỗi khi xử lý cặp câu: {type(e).__name__} - {e}')
#                 return
#             except Exception as e:
#                 QMessageBox.critical(self, 'Lỗi', f'Lỗi không xác định khi xử lý cặp câu: {type(e).__name__} - {e}')
#                 return
#         print('next_pair - Exiting')
#
#     def on_recording_done(self, audio_path):
#         print(f'on_recording_done - Starting with audio_path: {audio_path}')
#         if self.recorder_thread:
#             print('on_recording_done - Cleaning up recorder_thread')
#             self.recorder_thread.quit()
#             self.recorder_thread.wait()
#             self.recorder_thread = None
#
#         if not audio_path:
#             print('on_recording_done - Recording failed.')
#             self.feedback_label.setText('Ghi âm không thành công.')
#             return
#
#         try:
#             print('on_recording_done - Importing core.speech_assessment')
#             import core.speech_assessment as speech_assessment # Import here
#             sentence_b = self.current_topic_data['dialogue'][self.current_sentence_index + 1]
#             reference_text = sentence_b['text']
#             print('on_recording_done - Evaluating speech...')
#             result = speech_assessment.evaluate(audio_path, reference_text)
#             self.score_list.append(result['score'])
#             self.score_label.setText(f'Điểm số: {result["score"]}')
#             self.feedback_label.setText(f'Nhận xét: {result["feedback"]} ({result["user_text"]})')
#             try:
#               print(f'on_recording_done - try removing: {audio_path}')
#               os.remove(audio_path)
#               print(f'on_recording_done - remove success')
#             except Exception as e:
#               print(f'on_recording_done - cannot delete the audio path : {e}')
#             self.current_sentence_index += 2
#             print('on_recording_done - evaluation success')
#         except Exception as e:  # Catch any exception during evaluation
#             print(f'on_recording_done - cannot evaluate: {type(e).__name__} - {e}')
#             QMessageBox.warning(self, 'Lỗi', f'Không thể đánh giá: {type(e).__name__} - {e}')
#         print('on_recording_done - Exiting')
#         self.next_pair()
#
#
#     def summarize_results(self):
#         print('summarize_results - Starting')
#         total_score = sum(self.score_list)
#         average_score = total_score / len(self.score_list) if self.score_list else 0
#         QMessageBox.information(
#             self, "Kết quả",
#             f"Bạn đã hoàn thành chủ đề này!\nĐiểm trung bình: {average_score:.2f}"
#         )
#         self.on_topic_selected()  # Reset UI for new topic
#         print('summarize_results - Finished')
import os
import json
import tempfile
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout, QLabel, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal

import sounddevice as sd
import soundfile as sf


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
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
            sf.write(audio_path, audio, 44100)  # No subtype needed for float32
            self.recording_done.emit(audio_path)
        except sd.PortAudioError as e:
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

    # UI initialization (no changes needed in this section, but kept for completeness)
    # ...
    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        title_label = QLabel("🗣️ Luyện Nói Theo Chủ Đề")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        main_layout.addWidget(title_label)

        topic_layout = QHBoxLayout()
        topic_label = QLabel("Chủ đề:")
        topic_label.setStyleSheet("font-weight: bold; margin-right: 10px;")  # Add margin
        topic_layout.addWidget(topic_label)

        self.topic_combobox = QComboBox()
        self.topic_combobox.currentIndexChanged.connect(self.on_topic_selected)
        self.topic_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        topic_layout.addWidget(self.topic_combobox)
        topic_layout.addStretch()  # Add stretch to push widgets to the left

        main_layout.addLayout(topic_layout)

        self.dialogue_label = QLabel('Câu hội thoại sẽ hiển thị ở đây.')
        self.dialogue_label.setAlignment(Qt.AlignCenter)
        self.dialogue_label.setStyleSheet('font-size: 18px; margin-bottom: 20px;')  # Add margin
        self.dialogue_label.setWordWrap(True)
        self.dialogue_label.setStyleSheet('font-size: 18px;')
        main_layout.addWidget(self.dialogue_label)

        button_layout = QHBoxLayout()
        self.next_button = QPushButton("Bắt đầu")
        self.next_button.clicked.connect(self.next_pair)
        button_layout.addWidget(self.next_button)
        main_layout.addLayout(button_layout)

        # Score and Feedback labels in a grid layout
        score_feedback_layout = QVBoxLayout()

        score_label = QLabel("Điểm số:")
        self.score_label = QLabel('')  # Label to display the score value
        score_label.setStyleSheet("font-weight: bold;")
        score_feedback_layout.addWidget(score_label)
        score_feedback_layout.addWidget(self.score_label, alignment=Qt.AlignLeft)

        feedback_label = QLabel("Nhận xét:")
        self.feedback_label = QLabel('')  # Label to display feedback
        feedback_label.setStyleSheet("font-weight: bold;")
        score_feedback_layout.addWidget(feedback_label)
        score_feedback_layout.addWidget(self.feedback_label, alignment=Qt.AlignLeft)

        score_feedback_layout.setAlignment(Qt.AlignLeft)  # Align the content to the left
        main_layout.addLayout(score_feedback_layout)

        self.progress_label = QLabel('')  # Label to display progress
        main_layout.addWidget(self.progress_label)
        self.setLayout(main_layout)  # Set the main layout for the widget

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
                self.score_label.setText('Điểm số: ')
                self.feedback_label.setText('Nhận xét: ')
                self.update_progress_label()  # Initial progress display
                self.next_button.setText('Tiếp Tục')
            except KeyError as e:
                QMessageBox.critical(self, 'Lỗi', f'Không tìm thấy dữ liệu cho chủ đề: {e}')
            except Exception as e:
                QMessageBox.critical(self, 'Lỗi', f'Lỗi khi tải chủ đề: {e}')

    def update_progress_label(self):
        if self.current_topic_data:
            progress = min(self.current_sentence_index, self.sentence_count)  # Cap progress
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
            self.score_label.setText(f'Điểm số: {result["score"]}')
            self.feedback_label.setText(f'Nhận xét: {result["feedback"]} ({result["user_text"]})')
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
