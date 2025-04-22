from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextBrowser, QHBoxLayout
from PyQt5.QtCore import Qt
from googletrans import Translator
import pyttsx3


class DictionaryTab(QWidget):
    def __init__(self):
        super().__init__()

        self.translator = Translator()
        self.tts_engine = pyttsx3.init()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Search Input
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter a word...")
        search_layout.addWidget(self.search_input)

        # Search Button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_word)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        # Definition Display
        self.definition_display = QTextBrowser()
        layout.addWidget(self.definition_display)

        # Text-to-Speech Button
        tts_button = QPushButton("Pronounce")
        tts_button.clicked.connect(self.pronounce_word)
        layout.addWidget(tts_button, alignment=Qt.AlignRight)  # Align to the right

        self.setLayout(layout)

    def search_word(self):
        word = self.search_input.text()
        if word:
            try:
                translation = self.translator.translate(word, dest='vi')
                definition = f"<h2>{word}</h2>\n" \
                             f"<p><b>Vietnamese Translation:</b> {translation.text}</p>"
                self.definition_display.setHtml(definition)
            except Exception as e:
                self.definition_display.setHtml(f"<p style='color:red;'>Error: {str(e)}</p>")
        else:
            self.definition_display.setHtml("<p>Please enter a word to search.</p>")

    def pronounce_word(self):
        word = self.search_input.text()
        if word:
            try:
                self.tts_engine.say(word)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {str(e)}")