from focus_backdrop.core import logger

from pathlib import Path

from PySide6.QtCore import (Qt, QPoint, QSettings)

# from PySide6.QtCore import (Qt, QRect, QSize, QEvent, QPoint, Signal, QSettings,
#                             QCoreApplication, qInstallMessageHandler)
# from PySide6.QtGui import (QIcon, QFont, QColor, QAction, QPixmap, QMoveEvent,
#                             QCloseEvent, QShortcut, QPalette, QKeySequence)
# from PySide6.QtWidgets import (QMenu, QSlider, QLabel, QWidget, QDialog, QCheckBox,
#                                 QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog,
#                                 QMainWindow, QGridLayout, QRadioButton, QButtonGroup,
#                                 QColorDialog, QApplication)

logger.VERBOSE = True

def debug(*args, **kwargs):
    return logger.debug(*args, **kwargs)


def get_default_image_directory():
    """Get the default directory for image file dialogs."""
    if (Path.home() / 'Pictures' / 'Backdrops').exists():
        return str(Path.home() / 'Pictures' / 'Backdrops')
    elif (Path.home() / 'Pictures').exists():
        return str(Path.home() / 'Pictures')
    else:
        return str(Path.home())


class Settings:
    def __init__(self) -> None:
        
        # Constants for scale options
        self.SCALE_NO_SCALE     = 'original_no_scaling'
        self.SCALE_CUSTOM       = 'custom_scaling'
        self.SCALE_FILL_DISTORT = 'fill_distort'
        self.SCALE_FILL_CROP    = 'fill_crop'
        self.SCALE_FIT_NOCROP   = 'fit_nocrop'
        self.SCALE_FIT_WIDTH    = 'fit_width'
        self.SCALE_FIT_HEIGHT   = 'fit_height'
        
        # Constants for anchor points
        self.ANCHOR_TOP_LEFT    = int(Qt.AlignTop       | Qt.AlignLeft)     # 'top-left'
        self.ANCHOR_TOP_CENTER  = int(Qt.AlignTop       | Qt.AlignHCenter)  # 'top-center'
        self.ANCHOR_TOP_RIGHT   = int(Qt.AlignTop       | Qt.AlignRight)    # 'top-right'
        self.ANCHOR_MID_LEFT    = int(Qt.AlignVCenter   | Qt.AlignLeft)     # 'middle-left'
        self.ANCHOR_MID_CENTER  = int(Qt.AlignVCenter   | Qt.AlignHCenter)  # 'middle-center'
        self.ANCHOR_MID_RIGHT   = int(Qt.AlignVCenter   | Qt.AlignRight)    # 'middle-right'
        self.ANCHOR_BOT_LEFT    = int(Qt.AlignBottom    | Qt.AlignLeft)     # 'bottom-left'
        self.ANCHOR_BOT_CENTER  = int(Qt.AlignBottom    | Qt.AlignHCenter)  # 'bottom-center'
        self.ANCHOR_BOT_RIGHT   = int(Qt.AlignBottom    | Qt.AlignRight)    # 'bottom-right'
        
        # settings file: ~/.config/focus_backdrop/focus_backdrop.conf
        self.qsettings = QSettings("focus_backdrop", "focus_backdrop")
        
        # Load settings or set defaults
        self.dark_theme         = self.qsettings.value("dark_theme", True, type=bool)
        self.bg_color           = self.qsettings.value("bg_color", "#80333333", type=str)
        self.alpha_level        = self.qsettings.value("alpha_level", "80", type=str)
        self.scaling_option     = self.qsettings.value("scaling_option", self.SCALE_FIT_NOCROP, type=str)
        self.custom_scaling     = self.qsettings.value("custom_scaling", 0, type=int)
        self.anchor_point       = self.qsettings.value("anchor_point", self.ANCHOR_MID_CENTER, type=int)
        self.pixmap_path        = self.qsettings.value("pixmap_path", "", type=str)
        self.recent_image_path  = self.qsettings.value("recent_image_path", "", type=str)
        self.dialog_position    = self.qsettings.value("dialog_position", QPoint(100, 100), type=QPoint)

    def save_dialog_position(self, position: QPoint):
        self.dialog_position = position
        self.qsettings.setValue("dialog_position", position)
        self.qsettings.sync()

    def save_settings(self):
        self.qsettings.setValue("dark_theme", self.dark_theme)
        self.qsettings.setValue("bg_color", self.bg_color)
        self.qsettings.setValue("alpha_level", self.alpha_level)
        self.qsettings.setValue("scaling_option", self.scaling_option)
        self.qsettings.setValue("custom_scaling", self.custom_scaling)
        self.qsettings.setValue("anchor_point", self.anchor_point)
        self.qsettings.setValue("pixmap_path", self.pixmap_path)
        self.qsettings.setValue("recent_image_path", self.recent_image_path)
        self.qsettings.setValue("dialog_position", self.dialog_position)
        self.qsettings.sync()
