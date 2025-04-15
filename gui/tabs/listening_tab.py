from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QComboBox, QLineEdit, QTextEdit, \
    QHBoxLayout, QSlider, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import json
import os


class ListeningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.exercises = self.load_exercises()
        self.current_exercise = None
        self.current_challenge_data = None

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 30, 50, 30)

        title = QLabel("🎧 Luyện Nghe")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        # Exercise Selection
        self.exercise_dropdown = QComboBox()
        self.exercise_dropdown.currentIndexChanged.connect(self.update_challenge_list)
        main_layout.addWidget(self.exercise_dropdown)

        self.challenge_list = QListWidget()
        self.challenge_list.itemClicked.connect(self.challenge_selected)
        main_layout.addWidget(self.challenge_list)

        for link in self.exercises.keys():
            self.exercise_dropdown.addItem(link)
        if self.exercise_dropdown.count() > 0:
            self.update_challenge_list()

        # Speed Slider
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Audio Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(50)  # 50%
        self.speed_slider.setMaximum(150)  # 150%
        self.speed_slider.setValue(100)  # Default 100%
        self.speed_slider.setTickInterval(10)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        main_layout.addLayout(speed_layout)

        # Start Button
        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self.play_audio)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        main_layout.addLayout(button_layout)

        # Input and Result Layout
        input_result_layout = QVBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type what you hear here")
        input_result_layout.addWidget(self.user_input)

        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.check_answer)
        input_result_layout.addWidget(self.submit_button)

        self.listening_result = QTextEdit()
        self.listening_result.setReadOnly(True)
        self.listening_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_result_layout.addWidget(self.listening_result)

        self.translation_label = QLabel("")
        self.translation_label.setAlignment(Qt.AlignCenter)
        input_result_layout.addWidget(self.translation_label)

        main_layout.addLayout(input_result_layout)

        self.setLayout(main_layout)

        # Audio Player
        self.player = QMediaPlayer()
        self.player.setVolume(50)  # Default volume
        self.player.stateChanged.connect(self.audio_state_changed)

    def load_exercises(self):
        """Loads exercises from the 'data/listen.json' file."""
        exercises_data = {}
        file_path = "data/listen.json"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for conversation_url, challenges in data.items():
                        exercises_data[conversation_url] = challenges
                        for challenge_id, challenge_data in challenges.items():
                            if 'audio_path' in challenge_data:
                                # Cập nhật đường dẫn âm thanh từ 'audio_path' trong JSON
                                audio_path = challenge_data['audio_path']
                                # Kiểm tra nếu file âm thanh tồn tại
                                full_audio_path = os.path.join('data', 'tts', audio_path)  # Đảm bảo đường dẫn chính xác
                                if not os.path.exists(full_audio_path):
                                    print(f"Warning: audio file not found: {full_audio_path}")
                            else:
                                print(
                                    f"Warning: audio_path not found in challenge {challenge_id} of {conversation_url}")
            except json.JSONDecodeError:
                print("Error decoding JSON data from file")
        else:
            print("File not found")
        return exercises_data

    def update_challenge_list(self):
        """Updates the challenge list based on the selected exercise."""
        self.challenge_list.clear()
        selected_exercise = self.exercise_dropdown.currentText()
        if selected_exercise in self.exercises:
            challenges = self.exercises[selected_exercise]
            for challenge_id in challenges.keys():
                item = QListWidgetItem(challenge_id)
                self.challenge_list.addItem(item)

    def challenge_selected(self, item):
        """Handles the selection of a challenge from the list."""
        selected_exercise = self.exercise_dropdown.currentText()
        selected_challenge = item.text()
        if selected_exercise in self.exercises:
            challenges = self.exercises[selected_exercise]
            if selected_challenge in challenges:
                self.current_challenge_data = challenges[selected_challenge]
                self.user_input.clear()
                self.listening_result.clear()
                self.translation_label.clear()

    def audio_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.start_button.setEnabled(True)

    def play_audio(self):
        self.start_button.setEnabled(False)
        self.listening_result.setText("")
        self.translation_label.setText("")

        # Kiểm tra xem đã chọn challenge chưa
        if not self.current_challenge_data:
            self.listening_result.setText("Please select a challenge first.")
            return

        # Lấy audio_path từ dữ liệu challenge hiện tại
        audio_path = self.current_challenge_data.get('audio_path')

        if audio_path is None:
            self.listening_result.setText("Audio file not found for this challenge.")
            return

        # Chuyển đổi đường dẫn từ file JSON thành đường dẫn tuyệt đối
        audio_path = QDir.current().absoluteFilePath(os.path.join('data', 'tts', audio_path))  # Chỉnh sửa đường dẫn

        try:
            # Kiểm tra và khởi tạo QMediaContent
            media = QMediaContent(QUrl.fromLocalFile(audio_path))

            # Set media và bắt đầu phát âm thanh
            self.player.setMedia(media)
            self.player.play()
        except Exception as e:
            print(f"Error playing audio: {e}")
            self.listening_result.setText("Error playing audio.")
            self.start_button.setEnabled(True)

    def check_answer(self):
        user_answer = self.user_input.text().strip()
        if not self.current_challenge_data:
            self.listening_result.setText("Please select a challenge first.")
            return

        correct_answer = self.current_challenge_data['spoken_text']

        if user_answer.lower() == correct_answer.lower():
            self.listening_result.setText(f"Correct! The sentence is:\n{correct_answer}")

        else:
            self.listening_result.setText("Incorrect. Checking words...")
            words_correct = []
            user_words = user_answer.lower().split()
            correct_words = correct_answer.lower().split()
            for i in range(min(len(user_words), len(correct_words))):
                if user_words[i] == correct_words[i]:
                    words_correct.append(correct_words[i])
                else:
                    self.listening_result.append(
                        f"Word '{user_words[i]}' is incorrect. Correct word: '{correct_words[i]}'")
