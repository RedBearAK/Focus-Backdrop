import re

from focus_backdrop.core.config import Settings
from focus_backdrop.core.themes import apply_theme
from focus_backdrop.gui.dialogs import PreferencesDialog

from pathlib import Path

from PySide6.QtCore import Qt, QRect, QSize, QEvent

from PySide6.QtGui import QFont, QAction, QPixmap, QMoveEvent, QShortcut, QKeySequence

from PySide6.QtWidgets import QMenu, QLabel, QWidget, QMainWindow, QGridLayout



class MainWindow(QMainWindow):
    def __init__(self, cnfg: Settings, parent=None):
        super().__init__(parent)
        self._cnfg = cnfg
        self.setup_ui()
        self.update_theme()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        # self.setAttribute(Qt.WA_TransparentForMouseEvents) # doesn't work?

    def setup_ui(self):
        # Bind Ctrl+comma to open the Preferences dialog
        preferences_shortcut = QShortcut(QKeySequence("Ctrl+,"), self)
        preferences_shortcut.activated.connect(self.show_preferences_dialog)

        self.setWindowTitle("Focus Backdrop")
        self.setWindowFlags(
            Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.FramelessWindowHint)

        self.widget = QWidget(self)
        self.widget.setStyleSheet(f"background-color: {self._cnfg.bg_color};")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)
        self.label = QLabel(self.widget)

        original_pixmap = QPixmap(str(self._cnfg.pixmap_path)) or ""
        self.update_image_and_scaling(
            original_pixmap, 
            scaling_option=self._cnfg.scaling_option, 
            anchor_point=self._cnfg.anchor_point
        )
        self.update_theme()

        self.label.setGeometry(0, 0, self.widget.width(), self.widget.height())

        # Bind Ctrl+W to close the main window
        ctrlWShortcut = QShortcut(QKeySequence("Ctrl+W"), self.widget)
        ctrlWShortcut.activated.connect(self.close)

        layout.addWidget(self.label, 0, 0)
        # label.setStyleSheet("border: 1px solid red;") # debugging border
        self.setCentralWidget(self.widget)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def adjust_app_window(self, available_geometry: QRect):
        # available_size = available_geometry.size()
        # self.setFixedSize(available_size.width(), available_size.height())
        # self.move(available_geometry.topLeft())
        self.update_image_and_scaling(
            self._cnfg.pixmap_path, 
            scaling_option=self._cnfg.scaling_option, 
            anchor_point=self._cnfg.anchor_point
        )

    def update_current_screen(self, new_screen):
        self.windowHandle().screen().availableGeometryChanged.disconnect(self.adjust_app_window)
        new_screen.availableGeometryChanged.connect(self.adjust_app_window)
        self.adjust_app_window(new_screen.availableGeometry())

    def moveEvent(self, event: QMoveEvent):
        new_screen = self.screen()
        if new_screen != self.windowHandle().screen():
            self.update_current_screen(new_screen)
        super().moveEvent(event)

    def showEvent(self, event: QEvent):
        current_screen = self.screen()
        available_size = current_screen.availableGeometry()
        self.setFixedSize(available_size.width(), available_size.height())
        current_screen.availableGeometryChanged.connect(self.adjust_app_window)
        self.windowHandle().screenChanged.connect(self.update_current_screen)
        # QCoreApplication.instance().installEventFilter(self)

    def show_context_menu(self, point):
        context_menu_stylesheet = """
        QMenu {
            padding: 2px;
            spacing: 4px;
        }
        QMenu::item:disabled {
            color: gray;
        }
        QMenu::separator {
            height: 2px;
            background: gray;
            margin-left: 4px;
            margin-right: 4px;
        }
        QMenu::item:selected {
            background-color: #d7d7d7;
        }
        """

        context_menu = QMenu(self)
        context_menu.setStyleSheet(context_menu_stylesheet)
        context_menu.setFont(QFont('Arial', 12, weight=QFont.Bold))

        inactive_label = QAction("~ Focus Backdrop ~", context_menu)
        inactive_label.setEnabled(False)
        context_menu.addAction(inactive_label)

        context_menu.addSeparator()

        open_preferences_action = context_menu.addAction("      Preferences      ")

        # context_menu.addSeparator()

        # clear_image_action = context_menu.addAction("Clear Image")

        # connect all context_menu items to their methods here
        open_preferences_action.triggered.connect(self.show_preferences_dialog)
        # clear_image_action.triggered.connect(self.clear_image)

        context_menu.exec(self.mapToGlobal(point))

    def update_image_and_scaling(self, pixmap_path=None, scaling_option=None, anchor_point=None):
        if not pixmap_path or QPixmap(pixmap_path).isNull():
            self.label.clear()
            return

        if not scaling_option:
            scaling_option = self._cnfg.SCALE_FIT_NOCROP

        pixmap = QPixmap(pixmap_path)
        scaled_pixmap = pixmap

        if scaling_option:
            self.scaling_option = scaling_option

        # available_size = QGuiApplication.primaryScreen().availableGeometry()
        current_screen = self.screen()
        available_geometry = current_screen.availableGeometry()
        available_size = available_geometry.size()
        self.setFixedSize(available_size.width(), available_size.height())
        self.move(available_geometry.topLeft())

        desired_size = QSize(available_size.width(), available_size.height())
        original_size = QSize(pixmap.width(), pixmap.height())

        ###############################################################################
        ##### Show the image at the original size, no scaling
        if self.scaling_option == self._cnfg.SCALE_NO_SCALE:
            scaled_pixmap = pixmap.scaled(original_size, Qt.KeepAspectRatio)
        ###############################################################################
        ##### Scale to the size specified by custom scale slider, keep aspect ratio 
        if self.scaling_option == self._cnfg.SCALE_CUSTOM:
            if self._cnfg.custom_scaling < 0:
                # Scaling down from 100% to 1%
                scale_factor = 1 + (self._cnfg.custom_scaling / 999)
            else:
                # Scaling up from 100% to 200% (2 times the original size)
                scale_factor = 1 + (2 * self._cnfg.custom_scaling / 999)

            if scale_factor < 0.02:     # stop downscaling at 2% of original size
                scale_factor = 0.02
            scaled_pixmap = pixmap.scaled(
                QSize(
                    pixmap.width() * scale_factor,
                    pixmap.height() * scale_factor
                ), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ###############################################################################
        ##### Scale to the size of the window/widget/screen, ignoring aspect ratio 
        ##### (fill screen by modifying both dimensions separately as needed)
        if self.scaling_option == self._cnfg.SCALE_FILL_DISTORT:
            scaled_pixmap = pixmap.scaled(
                desired_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        ###############################################################################
        ##### Scale smaller dimension to the size of the window/widget/screen, 
        ##### with cropping of spillover (fill screen by cropping, keep aspect)
        if self.scaling_option == self._cnfg.SCALE_FILL_CROP:
            scaled_pixmap = pixmap.scaled(
                desired_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        ###############################################################################
        ##### Fit within the window/widget/screen dimensions
        ##### (no cropping, allow leaving blank bars in smaller dimension)
        if self.scaling_option == self._cnfg.SCALE_FIT_NOCROP:
            scaled_pixmap = pixmap.scaled(
                desired_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ###############################################################################
        ##### Fit the width of the image to the size of the window/widget/screen, 
        ##### ignoring whether the height would crop or leave blank bars
        if self.scaling_option == self._cnfg.SCALE_FIT_WIDTH:
            scaled_pixmap = pixmap.scaledToWidth(
                desired_size.width(), Qt.SmoothTransformation)
        ###############################################################################
        ##### Fit the height of the image to the size of the window/widget/screen, 
        ##### ignoring whether the width would crop or leave blank bars
        if self.scaling_option == self._cnfg.SCALE_FIT_HEIGHT:
            scaled_pixmap = pixmap.scaledToHeight(
                desired_size.height(), Qt.SmoothTransformation)

        if not anchor_point:
            self.label.setAlignment(Qt.Alignment(self._cnfg.ANCHOR_MID_CENTER))
        else:
            self.label.setAlignment(Qt.Alignment(anchor_point))
            
        self.label.setPixmap(scaled_pixmap)

    def on_emit_anchor_point_changed(self, pixmap_path, scaling_option, anchor_point):
        self.update_image_and_scaling(pixmap_path, scaling_option, anchor_point)

    def clear_image(self):
        self._cnfg.pixmap_path = ""
        self.update_image_and_scaling()
        self._cnfg.save_settings()

    def update_image(self, image_path, scaling_option, anchor_point):
        self._cnfg.pixmap_path = str(Path(image_path))
        pixmap = QPixmap(str(self._cnfg.pixmap_path)) or ""
        self.update_image_and_scaling(pixmap, scaling_option, anchor_point)
        self._cnfg.save_settings()

    def update_bg_color(self, color: str):
        self._cnfg.bg_color = color
        self.widget.setStyleSheet(f"background-color: {self._cnfg.bg_color};")
        self._cnfg.save_settings()
        
    def update_alpha_level(self, new_alpha_level: str):
        self._cnfg.alpha_level = new_alpha_level
        self._cnfg.bg_color = re.sub(r'#[0-9A-F][0-9A-F]', '#' + new_alpha_level, self._cnfg.bg_color, re.I)
        self.widget.setStyleSheet(f"background-color: {self._cnfg.bg_color};")
        self._cnfg.save_settings()

    def update_theme(self):
        # from focus_backdrop.core.themes import apply_theme
        apply_theme(self._cnfg)

    def show_preferences_dialog(self):
        prefs_dialog = PreferencesDialog(self, cnfg=self._cnfg)
        
        prefs_dialog.sig_dark_theme_toggled.connect(self.update_theme)
        prefs_dialog.sig_anchor_point_changed.connect(self.on_emit_anchor_point_changed)
        prefs_dialog.sig_scaling_opt_changed.connect(self.update_image_and_scaling)
        prefs_dialog.sig_custom_scaling_changed.connect(self.update_image_and_scaling)
        prefs_dialog.sig_new_color_selected.connect(self.update_bg_color)
        prefs_dialog.sig_clear_image_display.connect(self.clear_image)
        prefs_dialog.sig_new_image_selected.connect(self.update_image)
        prefs_dialog.sig_alpha_value_changed.connect(self.update_alpha_level)
        
        prefs_dialog.exec()
