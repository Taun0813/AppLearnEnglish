# from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedLayout, QVBoxLayout, QPushButton, QTabWidget
# from PyQt5.QtGui import QFont
# from PyQt5.QtCore import Qt
# from PyQt5.QtMultimedia import QMediaPlayer
# from gui.welcome_screen import WelcomeScreen
# from gui.menu_screen import MenuScreen
# from gui.tabs.ai_chat_tab import AIChatTab
# from gui.tabs.listening_tab import ListeningTab
# from gui.tabs.speaking_tab import SpeakingTab
# from gui.tabs.vocabulary_tab import VocabularyTab
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("English Learning App")
#         self.showMaximized()
#
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #EAE7D6;
#                 font-family: 'Segoe UI';
#             }
#
#             QPushButton {
#                 background-color: #5D7B6F;
#                 color: white;
#                 font-size: 18px;
#                 padding: 12px 24px;
#                 border-radius: 12px;
#             }
#
#             QPushButton:hover {
#                 background-color: #B0D4B8;
#                 color: #333;
#             }
#
#             QTabWidget::pane {
#                 border: 2px solid #B0D4B8;
#                 margin: 10px;
#             }
#
#             QTabBar::tab {
#                 background: #5D7B6F;
#                 color: white;
#                 padding: 12px 24px;
#                 font-size: 18px;
#                 border-top-left-radius: 10px;
#                 border-top-right-radius: 10px;
#                 margin-right: 8px;
#                 min-width: 120px;
#             }
#
#             QTabBar::tab:selected {
#                 background: #B0D4B8;
#                 color: black;
#             }
#
#             QLabel {
#                 font-size: 20px;
#                 font-weight: 600;
#             }
#
#             QLineEdit, QTextBrowser, QComboBox, QListWidget {
#                 font-size: 18px;
#                 padding: 10px;
#                 border-radius: 8px;
#             }
#         """)
#
#         self.main_font = QFont("Segoe UI", 12)
#         self.set_app_font(self.main_font)
#         self.player = QMediaPlayer()
#
#         self.central_widget = QWidget()
#         self.stacked_layout = QStackedLayout()
#
#         self.welcome_screen = WelcomeScreen(self.show_menu_screen)
#         self.menu_screen = MenuScreen(self.open_tab_screen)
#         self.main_app_screen = self.create_tab_screen()
#
#         self.stacked_layout.addWidget(self.welcome_screen)
#         self.stacked_layout.addWidget(self.menu_screen)
#         self.stacked_layout.addWidget(self.main_app_screen)
#
#         self.central_widget.setLayout(self.stacked_layout)
#         self.setCentralWidget(self.central_widget)
#
#     def set_app_font(self, font):
#         self.setFont(font)
#
#     def create_tab_screen(self):
#         self.tabs = QTabWidget()
#         self.tabs.addTab(AIChatTab(), "Chat AI")
#         self.tabs.addTab(ListeningTab(), "Listening")
#         self.tabs.addTab(SpeakingTab(), "Speaking")
#         self.tabs.addTab(VocabularyTab(), "Vocabulary")
#
#         back_btn = QPushButton("← Back to Menu")
#         back_btn.clicked.connect(self.show_menu_screen)
#
#         wrapper_layout = QVBoxLayout()
#         wrapper_layout.addWidget(back_btn, alignment=Qt.AlignLeft)
#         wrapper_layout.addWidget(self.tabs)
#
#         container = QWidget()
#         container.setLayout(wrapper_layout)
#         return container
#
#     def show_menu_screen(self):
#         self.stacked_layout.setCurrentIndex(1)
#
#     def open_tab_screen(self, tab_index):
#         self.tabs.setCurrentIndex(tab_index)
#         self.stacked_layout.setCurrentIndex(2)
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedLayout, QVBoxLayout, QPushButton, QTabWidget, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer
from gui.welcome_screen import WelcomeScreen
from gui.menu_screen import MenuScreen
from gui.tabs.ai_chat_tab import AIChatTab
from gui.tabs.listening_tab import ListeningTab
from gui.tabs.speaking_tab import SpeakingTab
from gui.tabs.vocabulary_tab import VocabularyTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("English Learning App")

        # Calculate window size and position to center it
        screen_geometry = QApplication.desktop().availableGeometry()
        window_width = int(screen_geometry.width() * 0.8)  # 80% of screen width
        window_height = int(screen_geometry.height() * 0.8)  # 80% of screen height
        self.setGeometry((screen_geometry.width() - window_width) // 2, (screen_geometry.height() - window_height) // 2, window_width, window_height)
        self.setMinimumSize(600, 400)  # Set minimum size

        self.setStyleSheet("""
            QMainWindow {
                background-color: #EAE7D6;
                font-family: 'Segoe UI';
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

            QTabWidget::pane { 
                border: 2px solid #B0D4B8;
                margin: 10px;
            }

            QTabBar::tab {
                background: #5D7B6F;
                color: white;
                padding: 12px 24px;
                font-size: 18px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 8px;
                min-width: 120px;
            }

            QTabBar::tab:selected {
                background: #B0D4B8;
                color: black;
            }

            QLabel {
                font-size: 20px;
                font-weight: 600;
            }

            QLineEdit, QTextBrowser, QComboBox, QListWidget {
                font-size: 18px;
                padding: 10px;
                border-radius: 8px;
            }
        """)

        self.main_font = QFont("Segoe UI", 12)
        self.set_app_font(self.main_font)
        self.player = QMediaPlayer()

        self.central_widget = QWidget()
        self.stacked_layout = QStackedLayout()

        self.welcome_screen = WelcomeScreen(self.show_menu_screen)
        self.menu_screen = MenuScreen(self.open_tab_screen)
        self.main_app_screen = self.create_tab_screen()

        self.stacked_layout.addWidget(self.welcome_screen)
        self.stacked_layout.addWidget(self.menu_screen)
        self.stacked_layout.addWidget(self.main_app_screen)

        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

    def set_app_font(self, font):
        self.setFont(font)

    def create_tab_screen(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(AIChatTab(), "Chat AI")
        self.tabs.addTab(ListeningTab(), "Listening")
        self.tabs.addTab(SpeakingTab(), "Speaking")
        self.tabs.addTab(VocabularyTab(), "Vocabulary")

        self.back_btn = QPushButton("← Back to Menu")
        self.back_btn.clicked.connect(self.show_menu_screen)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        wrapper_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(wrapper_layout)

        # Apply same style as other buttons to back_btn
        self.back_btn.setStyleSheet(self.styleSheet().split("QPushButton {")[1].split("}")[0])


        return container

    def show_menu_screen(self):
        self.stacked_layout.setCurrentIndex(1)

    def open_tab_screen(self, tab_index):
        self.tabs.setCurrentIndex(tab_index)
        self.stacked_layout.setCurrentIndex(2)

    def update_window_title(self, title):
        self.setWindowTitle(f"English Learning App - {title}")
