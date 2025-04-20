# from PyQt5.QtGui import QFont
#
# app_stylesheet = """
#     QMainWindow {
#         background-color: #EAE7D6;
#         font-family: 'Segoe UI';
#     }
#
#     QPushButton {
#         background-color: #5D7B6F;
#         color: white;
#         font-size: 18px;
#         padding: 12px 24px;
#         border-radius: 12px;
#     }
#
#     QPushButton:hover {
#         background-color: #B0D4B8;
#         color: #333;
#     }
#
#     QTabWidget::pane {
#         border: 2px solid #B0D4B8;
#         margin: 10px;
#     }
#
#     QTabBar::tab {
#         background: #5D7B6F;
#         color: white;
#         padding: 12px 24px;
#         font-size: 18px;
#         border-top-left-radius: 10px;
#         border-top-right-radius: 10px;
#         margin-right: 8px;
#         min-width: 120px;
#     }
#
#     QTabBar::tab:selected {
#         background: #B0D4B8;
#         color: black;
#     }
#
#     QLabel {
#         font-size: 20px;
#         font-weight: 600;
#     }
#
#     QLineEdit, QTextBrowser, QComboBox, QListWidget {
#         font-size: 18px;
#         padding: 10px;
#         border-radius: 8px;
#     }
# """
#
# main_font = QFont("Segoe UI", 12)
#
# menu_title_font = QFont("Segoe UI", 28, QFont.Bold)
#
# title_style = "font-size: 24px; font-weight: bold;"
from PyQt5.QtGui import QFont

app_stylesheet = """
    QMainWindow {
        background-color: #EAE7D6;       
        font-family: 'Consolas';
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
        border: 3px solid #B0D4B8;
        border-radius: 10px;
        margin: 10px;
    }

    QTabBar::tab {        
        background: #5D7B6F;
        color: white;
        padding: 16px 24px;
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
        font-size: 20px;
        padding: 10px;
        border-radius: 8px;
    }
"""

main_font = QFont("Consolas", 12)

menu_title_font = QFont("Segoe UI", 28, QFont.Bold)

title_style = "font-size: 24px; font-weight: bold;"