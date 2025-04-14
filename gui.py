# # mmm.py
# import time
# import re
# from datetime import date, datetime
# from openai import OpenAI
# import speech_recognition as sr
# import pyttsx3
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
#
# # OpenAI client config
# client = OpenAI(
#     base_url="http://172.20.128.1:3000/v1",
#     api_key="lm-studio",
# )
#
# BOT_PROMPT = """
# Bạn là một người bạn đồng hành giúp luyện nghe và luyện nói tiếng Anh.
# Hãy giao tiếp đơn giản, dễ hiểu, và phản hồi bằng ngôn ngữ mà người dùng đã sử dụng trong câu hỏi.
# """
#
# def summarize_text(text, max_sentences=3):
#     sentences = re.split(r'(?<=[.!?]) +', text)
#     summary = ' '.join(sentences[:max_sentences])
#     return summary.strip()
#
# class VoiceAssistantApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Voice Assistant - Luyện nói tiếng Anh")
#         self.setGeometry(100, 100, 500, 400)
#
#         self.layout = QVBoxLayout()
#         self.listen_button = QPushButton("🎤 Bắt đầu nghe")
#         self.listen_button.clicked.connect(self.handle_listen)
#
#         self.user_input_label = QLabel("Bạn nói:")
#         self.user_input_text = QTextEdit()
#         self.user_input_text.setReadOnly(True)
#
#         self.bot_reply_label = QLabel("Phản hồi từ trợ lý:")
#         self.bot_reply_text = QTextEdit()
#         self.bot_reply_text.setReadOnly(True)
#
#         self.layout.addWidget(self.listen_button)
#         self.layout.addWidget(self.user_input_label)
#         self.layout.addWidget(self.user_input_text)
#         self.layout.addWidget(self.bot_reply_label)
#         self.layout.addWidget(self.bot_reply_text)
#
#         self.setLayout(self.layout)
#
#         # Voice setup
#         self.robot_ear = sr.Recognizer()
#         self.robot_mouth = pyttsx3.init()
#         self.messages = [{"role": "system", "content": BOT_PROMPT}]
#
#     def type_print_to_textbox(self, text, textbox, delay=0.01):
#         textbox.clear()
#         for char in text:
#             textbox.insertPlainText(char)
#             time.sleep(delay)
#
#     def handle_listen(self):
#         with sr.Microphone() as mic:
#             self.robot_ear.adjust_for_ambient_noise(mic, duration=0.5)
#             try:
#                 audio = self.robot_ear.listen(mic, timeout=5, phrase_time_limit=7)
#                 user_input = self.robot_ear.recognize_google(audio, language='vi-VN')
#                 self.user_input_text.setPlainText(user_input)
#             except sr.UnknownValueError:
#                 self.user_input_text.setPlainText("Không nhận diện được giọng nói.")
#                 return
#             except sr.WaitTimeoutError:
#                 self.user_input_text.setPlainText("Không nghe thấy gì.")
#                 return
#
#         # Phản hồi đặc biệt
#         if "thoát" in user_input.lower():
#             self.bot_reply_text.setPlainText("Tạm biệt nhé!")
#             self.robot_mouth.say("Tạm biệt nhé!")
#             self.robot_mouth.runAndWait()
#             return
#
#         self.messages.append({"role": "user", "content": user_input})
#         response = client.chat.completions.create(
#             model="meta-llama-3.1-8b-instruct",
#             stream=True,
#             messages=self.messages
#         )
#
#         full_reply = ""
#         for chunk in response:
#             content = chunk.choices[0].delta.content or ""
#             full_reply += content
#
#         self.messages.append({"role": "assistant", "content": full_reply})
#         self.type_print_to_textbox(full_reply, self.bot_reply_text)
#
#         summary = summarize_text(full_reply)
#         self.robot_mouth.say(summary)
#         self.robot_mouth.runAndWait()
