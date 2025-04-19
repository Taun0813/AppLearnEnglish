# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextBrowser
# from PyQt5.QtCore import QTimer, Qt
# from core.ai_conversation import AIConversation
#
#
# class AIChatTab(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setStyleSheet("QLabel#title { font-size: 24px; font-weight: bold; }")
#
#         layout = QVBoxLayout()
#         layout.setSpacing(15)
#         layout.setContentsMargins(50, 30, 50, 30)
#
#         self.title = QLabel("🗨️ Giao tiếp với AI")
#         self.title.setObjectName("title")
#         self.title.setAlignment(Qt.AlignCenter)
#
#         self.chat_display = QTextBrowser()
#         self.input_field = QLineEdit()
#         self.input_field.setPlaceholderText("Nhập tin nhắn...")
#         self.send_button = QPushButton("Gửi")
#
#         self.send_button.clicked.connect(self.send_message_to_ai)
#         self.input_field.returnPressed.connect(self.send_message_to_ai)
#
#         layout.addWidget(self.title)
#         layout.addWidget(self.chat_display)
#         layout.addWidget(self.input_field)
#         layout.addWidget(self.send_button)
#
#         self.setLayout(layout)
#
#         self.ai_conversation = AIConversation()
#         self.response_generator = None
#         self.typing_timer = QTimer()
#         self.typing_timer.timeout.connect(self.display_next_character)
#         self.pending_text = ""
#
#     def send_message_to_ai(self):
#         message = self.input_field.text()
#         if message:
#             self.chat_display.append(f"You: {message}")
#             self.input_field.clear()
#
#             self.response_generator = self.ai_conversation.chat_with_ai(message)
#             self.chat_display.append("AI: ")
#             self.pending_text = ""
#             self.typing_timer.start(30)
#
#     def display_next_character(self):
#         try:
#             if self.pending_text:
#                 next_char = self.pending_text[0]
#                 self.pending_text = self.pending_text[1:]
#                 self.chat_display.textCursor().insertText(next_char)
#                 self.chat_display.ensureCursorVisible()
#             else:
#                 next_chunk = next(self.response_generator)
#                 self.pending_text = next_chunk
#         except StopIteration:
#             self.typing_timer.stop()
#             self.chat_display.append("")
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextBrowser,
)
from PyQt5.QtCore import QTimer, Qt, pyqtSlot
from core.ai_conversation import AIConversation


class AIChatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #5D7B6F;
                color: white;
                font-size: 18px;
                padding: 12px 24px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #B0D4B8;
                color: #333;
            }
            QLineEdit, QTextBrowser {
                font-size: 18px;
                padding: 10px;
                border-radius: 8px;
            }
        """
        )
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel("🗨️ Giao tiếp với AI")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.chat_display = QTextBrowser(self)
        self.layout.addWidget(self.chat_display)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Nhập tin nhắn...")
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Gửi", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.ai_conversation = AIConversation()
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.update_chat)
        self.partial_response = ""

    @pyqtSlot()
    def send_message(self):
        user_message = self.input_field.text()
        if user_message:
            self.chat_display.append(f"<p style='color: blue;'>Bạn: {user_message}</p>")
            self.input_field.clear()
            self.send_button.setEnabled(False)
            self.partial_response = ""
            self.response_generator = self.ai_conversation.chat_with_ai(user_message)
            self.typing_timer.start(50)

    @pyqtSlot()
    def update_chat(self):
        try:
            chunk = next(self.response_generator)
            self.partial_response += chunk
            formatted_response = self.partial_response.replace("\n", "<br>")
            self.chat_display.setHtml(
                self.chat_display.toHtml()
                + f"<p style='color: green;'>AI: {formatted_response}</p>"
            )
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )
        except StopIteration:
            self.typing_timer.stop()
            self.send_button.setEnabled(True)
