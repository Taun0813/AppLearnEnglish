# from gui.ui import ui_config
# from PyQt5.QtWidgets import (
#     QWidget,
#     QVBoxLayout,
#     QLabel,
#     QLineEdit,
#     QPushButton,
#     QTextBrowser,
# )
# from PyQt5.QtCore import QTimer, Qt, pyqtSlot
# from core.ai_conversation import AIConversation
#
#
# class AIChatTab(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setStyleSheet(ui_config.app_stylesheet)
#         self.initUI()
#
#     def initUI(self):
#         self.layout = QVBoxLayout(self)
#         self.layout.setSpacing(20)
#         self.layout.setAlignment(Qt.AlignTop)
#
#         self.title_label = QLabel("🗨️ Giao tiếp với AI")
#         self.title_label.setObjectName("title")
#         self.title_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.title_label)
#
#         self.chat_display = QTextBrowser(self)
#         self.layout.addWidget(self.chat_display)
#
#         self.input_field = QLineEdit(self)
#         self.input_field.setPlaceholderText("Nhập tin nhắn...")
#         self.layout.addWidget(self.input_field)
#
#         self.send_button = QPushButton("Gửi", self)
#         self.send_button.clicked.connect(self.send_message)
#         self.layout.addWidget(self.send_button)
#
#         self.ai_conversation = AIConversation()
#         self.typing_timer = QTimer(self)
#         self.typing_timer.timeout.connect(self.update_chat)
#         self.partial_response = ""
#
#     @pyqtSlot()
#     def send_message(self):
#         user_message = self.input_field.text()
#         if user_message:
#             self.chat_display.append(f"<p style='color: blue;'>Bạn: {user_message}</p>")
#             self.input_field.clear()
#             self.send_button.setEnabled(False)
#             self.partial_response = ""
#             self.response_generator = self.ai_conversation.chat_with_ai(user_message)
#             self.typing_timer.start(50)
#
#     @pyqtSlot()
#     def update_chat(self):
#         try:
#             chunk = next(self.response_generator)
#             self.partial_response += chunk
#             formatted_response = self.partial_response.replace("\n", "<br>")
#             self.chat_display.setHtml(
#                 self.chat_display.toHtml()
#                 + f"<p style='color: green;'>AI: {formatted_response}</p>"
#             )
#             self.chat_display.verticalScrollBar().setValue(
#                 self.chat_display.verticalScrollBar().maximum()
#             )
#         except StopIteration:
#             self.typing_timer.stop()
#             self.send_button.setEnabled(True)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextBrowser, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
from core.ai_conversation import AIConversation


class AIChatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.ai_conversation = AIConversation()
        self.response_generator = None
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.display_next_character)
        self.pending_text = ""
        self.setStyleSheet("""
            QLabel#title { font-size: 24px; font-weight: bold; padding: 10px; }
            QPushButton#sendButton {
                background-color: #4CAF50; /* Green */
                border-radius: 10px;
                color: white;
                padding: 10px 20px;
                text-align: center;
            }
            QPushButton#sendButton:hover {
                background-color: #367C39; /* Darker Green */
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        self.title = QLabel("🗨️ Chat with AI")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)

        self.chat_display = QTextBrowser()

        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter a message ...")
        self.input_field.setFixedHeight(40)
        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("sendButton")
        self.send_button.clicked.connect(self.send_message_to_ai)
        self.input_field.returnPressed.connect(self.send_message_to_ai)
        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_button)
        self.send_button.setFixedWidth(100)

        layout.addWidget(self.title)
        layout.addWidget(self.chat_display)
        layout.addLayout(self.input_layout)
        self.setLayout(layout)
    def send_message_to_ai(self):
        message = self.input_field.text()
        if message:
            self.chat_display.append(f"You: {message}")
            self.input_field.clear()
            self.response_generator = self.ai_conversation.chat_with_ai(message)
            self.chat_display.append("AI: ")
            self.pending_text = ""
            self.typing_timer.start(30)
    def display_next_character(self):
        try:
            if self.pending_text:
                next_char = self.pending_text[0]
                self.pending_text = self.pending_text[1:]
                self.chat_display.textCursor().insertText(next_char)
                self.chat_display.ensureCursorVisible()
            else:
                next_chunk = next(self.response_generator)
                self.pending_text = next_chunk
        except StopIteration:
            self.typing_timer.stop()
            self.chat_display.append("")
