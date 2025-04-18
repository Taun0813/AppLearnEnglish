from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QComboBox, QLineEdit, QTextEdit, \
    QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
import re
import json


class ListeningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 16px;")
        self.exercises = self.load_exercises()
        self.current_exercise = ""
        self.current_challenge_data = None
        self.challenge_queue = []
        self.current_challenge_index = 0

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 30, 50, 30)

        title = QLabel("🎧 Luyện Nghe")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        # Conversation Dropdown
        self.exercise_dropdown = QComboBox()
        self.exercise_dropdown.currentIndexChanged.connect(self.exercise_selected)
        main_layout.addWidget(self.exercise_dropdown)

        # Speed Slider
        speed_layout = QHBoxLayout()
        self.speed_label = QLabel("Audio Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(150)
        self.speed_slider.setValue(100)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.valueChanged.connect(self.update_audio_speed)
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_slider)
        main_layout.addLayout(speed_layout)

        # Start Button
        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self.play_audio)
        main_layout.addWidget(self.start_button)

        # Input and Result Layout
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type what you hear here")
        main_layout.addWidget(self.user_input)

        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.check_answer)
        main_layout.addWidget(self.submit_button)

        self.listening_result = QTextEdit()
        self.listening_result.setReadOnly(True)
        self.listening_result.setStyleSheet("background-color: #f0f0f0;")
        main_layout.addWidget(self.listening_result)

        self.translation_label = QLabel("")
        self.translation_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.translation_label)

        self.setLayout(main_layout)

        # Audio Player
        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.player.stateChanged.connect(self.audio_state_changed)

        # Populate dropdown
        for link in self.exercises.keys():
            self.exercise_dropdown.addItem(link)

        if self.exercise_dropdown.count() > 0:
            self.exercise_selected()

    def update_audio_speed(self, value):
        speed = value / 100.0  # convert từ phần trăm (ví dụ: 100 → 1.0)
        self.player.setPlaybackRate(speed)
        self.speed_label.setText(f"Audio Speed: {value}%")

    def load_exercises(self):
        exercises_data = {}
        file_path = "data/listen.json"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for conversation_url, content in data.items():
                        if 'Challenges' in content:
                            exercises_data[conversation_url] = content['Challenges']
            except json.JSONDecodeError:
                print("Error decoding JSON data")
        else:
            print("File not found:", file_path)
        return exercises_data

    def exercise_selected(self):
        self.current_exercise = self.exercise_dropdown.currentText()
        self.challenge_queue = []
        self.current_challenge_index = 0

        if self.current_exercise in self.exercises:
            for challenge_id, challenge_data in self.exercises[self.current_exercise].items():
                self.challenge_queue.append((challenge_id, challenge_data))

    def audio_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.start_button.setEnabled(True)

    def play_audio(self):
        if self.current_challenge_index >= len(self.challenge_queue):
            self.listening_result.setText("🎉 All challenges completed!")
            return

        challenge_id, challenge_data = self.challenge_queue[self.current_challenge_index]
        self.current_challenge_data = challenge_data
        self.user_input.clear()
        self.listening_result.clear()
        self.translation_label.clear()

        audio_path = challenge_data.get("audio_path")
        if not audio_path or not os.path.exists(audio_path):
            self.listening_result.setText(f"Audio file not found: {audio_path}")
            return

        self.start_button.setEnabled(False)
        self.player.stop()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(audio_path))))
        self.player.setVolume(100)
        self.player.play()

    def normalize_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = ' '.join(text.split())
        return text

    def check_answer(self):
        user_answer = self.user_input.text().strip()
        if not self.current_challenge_data:
            self.listening_result.setText("Please select a challenge first.")
            return

        correct_answer = self.current_challenge_data['spoken_text']

        if self.normalize_text(user_answer) == self.normalize_text(correct_answer):
            self.listening_result.setText(f"✅ Correct! The sentence is:\n{correct_answer}")
            # Next challenge
            self.current_challenge_index += 1
            QTimer.singleShot(1500, self.play_audio)
        else:
            self.listening_result.setText("❌ Incorrect. Checking words...\n")
            user_words = self.normalize_text(user_answer).split()
            correct_words = self.normalize_text(correct_answer).split()
            for i in range(min(len(user_words), len(correct_words))):
                if user_words[i] == correct_words[i]:
                    self.listening_result.append(f"✅ {user_words[i]}")
                else:
                    self.listening_result.append(f"❌ '{user_words[i]}' → ✅ '{correct_words[i]}'")


