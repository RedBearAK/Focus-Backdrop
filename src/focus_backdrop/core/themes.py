from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


def apply_theme(config_object):
    app: QApplication = QCoreApplication.instance()
    if not config_object.dark_theme:
        light_theme_palette = QPalette()
        light_theme_palette.setColor(QPalette.Window, QColor(240, 240, 240))
        light_theme_palette.setColor(QPalette.WindowText, Qt.black)
        light_theme_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        light_theme_palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        light_theme_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 225))
        light_theme_palette.setColor(QPalette.ToolTipText, Qt.black)
        light_theme_palette.setColor(QPalette.Text, Qt.black)
        light_theme_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_theme_palette.setColor(QPalette.ButtonText, Qt.black)
        light_theme_palette.setColor(QPalette.Active, QPalette.Button, QColor(240, 240, 240))
        light_theme_palette.setColor(QPalette.Active, QPalette.ButtonText, Qt.black)
        light_theme_palette.setColor(QPalette.ButtonText, Qt.black)
        light_theme_palette.setColor(QPalette.BrightText, Qt.red)
        light_theme_palette.setColor(QPalette.Link, QColor(0, 0, 255))
        light_theme_palette.setColor(QPalette.Highlight, QColor(51, 153, 255))
        light_theme_palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(light_theme_palette)
        light_style = """
            QToolTip {
                color: #000000;
                background-color: #ffffe1;
                border: 1px solid gray;
            }
            QPushButton {
                border: 2px solid #dddddd;
                background-color: #fefefe;
                border-radius: 10px;
            }
            QPushButton:focus {
                border: 2px solid #2a82da;
                background-color: #2a82da;
            }
        """
        app.setStyleSheet(light_style)
    else:
        dark_theme_palette = QPalette()
        dark_theme_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_theme_palette.setColor(QPalette.WindowText, Qt.white)
        dark_theme_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_theme_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_theme_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_theme_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_theme_palette.setColor(QPalette.Text, Qt.white)
        dark_theme_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_theme_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_theme_palette.setColor(QPalette.Active, QPalette.Button, QColor(64, 64, 64))
        dark_theme_palette.setColor(QPalette.Active, QPalette.ButtonText, Qt.white)
        dark_theme_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_theme_palette.setColor(QPalette.BrightText, Qt.red)
        dark_theme_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_theme_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_theme_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_theme_palette)
        dark_style = """
            QToolTip {
                color: #ffffff;
                background-color: gray;
                border: 1px solid gray;
            }
            QPushButton {
                border: 2px solid #666666;
                background-color: #555555;
                border-radius: 10px;
            }
            QPushButton:focus {
                border: 2px solid #2a82da;
                background-color: #2a82da;
            }
        """
        app.setStyleSheet(dark_style)