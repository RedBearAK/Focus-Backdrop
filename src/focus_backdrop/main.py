import os
import sys
import signal
import argparse
import platform

from focus_backdrop._version import __version__
from focus_backdrop.core import logger
from focus_backdrop.core.config import Settings
from focus_backdrop.gui.main_window import MainWindow

from pathlib import Path

from PySide6.QtCore import qInstallMessageHandler

from PySide6.QtGui import QIcon

from PySide6.QtWidgets import QApplication


logger.VERBOSE = True

def debug(*args, **kwargs):
    return logger.debug(*args, **kwargs)

if os.name == 'posix' and os.geteuid() == 0:
    print("This app should not be run as root/superuser.")
    sys.exit(1)

def signal_handler(sig, frame):
    if sig in (signal.SIGINT, signal.SIGQUIT):
        # Perform any cleanup code here before exiting
        # traceback.print_stack(frame)
        print(f'\nSIGINT or SIGQUIT received. Exiting.\n')
        sys.exit(0)

if platform.system() != 'Windows':
    signal.signal(signal.SIGINT,    signal_handler)
    signal.signal(signal.SIGQUIT,   signal_handler)
    signal.signal(signal.SIGHUP,    signal_handler)
    signal.signal(signal.SIGUSR1,   signal_handler)
    signal.signal(signal.SIGUSR2,   signal_handler)
else:
    signal.signal(signal.SIGINT,    signal_handler)

# catch some Qt specific errors from other libraries
def message_handler(msg_type, context, msg):
    if "libpng warning: iCCP: known incorrect sRGB profile" not in msg:
        print(f"{msg_type}: {msg}")

qInstallMessageHandler(message_handler)

app_file_dir_path       = Path(__file__).resolve().parent

# set icon path for app compiled with Nuitka
if getattr(sys, 'frozen', False):
    # Running in a compiled application
    app_assets_dir_path = os.path.join(sys._MEIPASS, 'resources')
    app_icon_file_path = os.path.join(app_assets_dir_path, 'icons', 'focus_backdrop_icon.svg')
else:
    # Running in a normal Python environment
    app_assets_dir_path     = app_file_dir_path / 'resources'
    app_icon_file_path      = app_assets_dir_path / 'icons' / 'focus_backdrop_icon.svg'

icon_file_path_str      = str(app_icon_file_path)


def main(args: argparse.Namespace):
    cnfg = Settings()
    app = QApplication(sys.argv)

    app.setApplicationVersion('2023.0314')
    app.setApplicationName('Focus Backdrop')
    app.setDesktopFileName('Focus_Backdrop')
    app_icon = QIcon(icon_file_path_str)
    app.setWindowIcon(app_icon)

    main_window = MainWindow(cnfg)
    
    # main_window.update_theme()
    # main_window.setAttribute(Qt.WA_TranslucentBackground)
    # main_window.setAttribute(Qt.WA_NoSystemBackground)

    main_window.show()

    if args.preferences:
        main_window.show_preferences_dialog()
    sys.exit(app.exec())
