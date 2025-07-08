from focus_backdrop.core.config import Settings, get_default_image_directory

from pathlib import Path

from PySide6.QtCore import Qt, Signal

from PySide6.QtGui import QCloseEvent, QColor, QFont, QKeySequence, QMoveEvent, QShortcut

from PySide6.QtWidgets import ( QButtonGroup, QCheckBox, QColorDialog, QDialog, QFileDialog,
                                QGridLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton,
                                QSlider, QVBoxLayout, QWidget)


default_image_dir_path = get_default_image_directory()


class ColorDialog(QColorDialog):
    def __init__(self, parent=None, cnfg=None):
        super().__init__(parent)
        self._cnfg = cnfg


class FileDialog(QFileDialog):
    def __init__(self, parent=None, cnfg=None):
        super().__init__(parent)
        self._cnfg = cnfg


class PreferencesDialog(QDialog):
    sig_dark_theme_toggled = Signal()

    sig_new_image_selected = Signal(str, str, int)
    sig_scaling_opt_changed = Signal(str, str, int)
    sig_anchor_point_changed = Signal(str, str, int)
    sig_custom_scaling_changed = Signal(str, str, int)

    sig_new_color_selected = Signal(str)
    sig_alpha_value_changed = Signal(str)
    sig_clear_image_display = Signal()

    def __init__(self, parent=None, cnfg: Settings = None):
        super().__init__(parent)
        self._cnfg = cnfg
        self.move(self._cnfg.dialog_position)
        self.setup_ui()

    def closeEvent(self, event: QCloseEvent):
        self._cnfg.save_dialog_position(self.pos())
        super().closeEvent(event)

    def moveEvent(self, event: QMoveEvent):
        self._cnfg.save_dialog_position(self.pos())
        super().moveEvent(event)

    def setup_ui(self):
        self.setWindowTitle("Focus Backdrop Preferences")
        # self.setFixedSize(600, 600)
        self.setFixedWidth(660)

        # Bind Ctrl+w to close Preferences dialog
        close_prefs_shortcut = QShortcut(QKeySequence("Ctrl+w"), self)
        close_prefs_shortcut.activated.connect(self.close)

        main_prefs_dialog_layout = QVBoxLayout(self)
        main_prefs_dialog_layout.setContentsMargins(10, 10, 10, 10)
        # main_prefs_dialog_layout.setSpacing(10)

        # Dark theme switch
        dark_theme_switch = QCheckBox("Dark Theme")
        dark_theme_switch.setChecked(self._cnfg.dark_theme)
        dark_theme_switch.stateChanged.connect(self.toggle_dark_theme)
        dark_theme_switch.setFont(QFont('Arial', 10, weight=QFont.Bold))

        top_layout = QHBoxLayout()
        top_layout.addWidget(dark_theme_switch, 0, Qt.AlignRight)
        main_prefs_dialog_layout.addLayout(top_layout)

        label_font = QFont('Arial', 13, weight=QFont.Bold)
        label_contents_margins = (0, 20, 0, 0)

        middle_items_hbox_layout = QHBoxLayout()
        middle_items_hbox_layout.setContentsMargins(0, 20, 0, 0)
        
        middle_items_vbox_left_layout = QVBoxLayout()
        middle_items_vbox_right_layout = QVBoxLayout()
        
        middle_items_hbox_layout.addLayout(middle_items_vbox_left_layout)
        middle_items_hbox_layout.addLayout(middle_items_vbox_right_layout)

        anchor_point_btns_grp = QButtonGroup()

        anchor_point_grid_widget = QWidget()
        # anchor_point_grid_widget.setStyleSheet("border: 1px solid red;") # debugging border
        
        anchor_point_grid_layout = QGridLayout(anchor_point_grid_widget)
        anchor_point_grid_layout.setAlignment(Qt.AlignCenter)
        anchor_point_grid_layout.setContentsMargins(30, 0, 0, 0)

        anchor_point_group_label = QLabel("Anchor Point")
        # anchor_point_group_label.setStyleSheet("border: 1px solid red;") # debugging border
        anchor_point_group_label.setFont(label_font)
        anchor_point_group_label.setAlignment(Qt.AlignCenter)

        # main_prefs_dialog_layout.addWidget(anchor_point_group_label)
        middle_items_vbox_left_layout.addWidget(anchor_point_group_label)

        # Create radio buttons for anchor points
        self.anchor_point_btn_top_left    = QRadioButton(f"\nT-L")
        self.anchor_point_btn_top_center  = QRadioButton(f"\nT-C")
        self.anchor_point_btn_top_right   = QRadioButton(f"\nT-R")
        self.anchor_point_btn_mid_left    = QRadioButton(f"\nM-L")
        self.anchor_point_btn_mid_center  = QRadioButton(f"\nM-C")
        self.anchor_point_btn_mid_right   = QRadioButton(f"\nM-R")
        self.anchor_point_btn_bot_left    = QRadioButton(f"\nB-L")
        self.anchor_point_btn_bot_center  = QRadioButton(f"\nB-C")
        self.anchor_point_btn_bot_right   = QRadioButton(f"\nB-R")

        anchor_point_grid_widget.setFocusProxy(self.anchor_point_btn_top_left)

        anchor_point_btns_lst = [
            self.anchor_point_btn_top_left,
            self.anchor_point_btn_top_center,
            self.anchor_point_btn_top_right,
            self.anchor_point_btn_mid_left,
            self.anchor_point_btn_mid_center,
            self.anchor_point_btn_mid_right,
            self.anchor_point_btn_bot_left,
            self.anchor_point_btn_bot_center,
            self.anchor_point_btn_bot_right
        ]
        anchor_point_btn_font = QFont('monospace', 10, weight=QFont.Bold)
        for _btn in anchor_point_btns_lst:
            _btn.setFont(anchor_point_btn_font)
            _btn.setFixedSize(60, 30)

        # Add radio buttons to the grid layout
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_top_left, 0, 0, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_top_center, 0, 1, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_top_right, 0, 2, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_mid_left, 1, 0, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_mid_center, 1, 1, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_mid_right, 1, 2, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_bot_left, 2, 0, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_bot_center, 2, 1, Qt.AlignCenter)
        anchor_point_grid_layout.addWidget(self.anchor_point_btn_bot_right, 2, 2, Qt.AlignCenter)

        # Add anchor point radio buttons to the anchor_point_group
        anchor_point_btns_grp.addButton(self.anchor_point_btn_top_left)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_top_center)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_top_right)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_mid_left)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_mid_center)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_mid_right)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_bot_left)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_bot_center)
        anchor_point_btns_grp.addButton(self.anchor_point_btn_bot_right)

        anchor_point_btns_mapping = {
            self._cnfg.ANCHOR_TOP_LEFT: self.anchor_point_btn_top_left,
            self._cnfg.ANCHOR_TOP_CENTER: self.anchor_point_btn_top_center,
            self._cnfg.ANCHOR_TOP_RIGHT: self.anchor_point_btn_top_right,
            self._cnfg.ANCHOR_MID_LEFT: self.anchor_point_btn_mid_left,
            self._cnfg.ANCHOR_MID_CENTER: self.anchor_point_btn_mid_center,
            self._cnfg.ANCHOR_MID_RIGHT: self.anchor_point_btn_mid_right,
            self._cnfg.ANCHOR_BOT_LEFT: self.anchor_point_btn_bot_left,
            self._cnfg.ANCHOR_BOT_CENTER: self.anchor_point_btn_bot_center,
            self._cnfg.ANCHOR_BOT_RIGHT: self.anchor_point_btn_bot_right
        }
        anchor_point_btns_mapping[int(self._cnfg.anchor_point)].setChecked(True)

        # main_prefs_dialog_layout.addWidget(anchor_point_grid_widget)
        middle_items_vbox_left_layout.addWidget(anchor_point_grid_widget)

        scaling_opts_btns_grp = QButtonGroup()

        scaling_opts_widget = QWidget()
        # scaling_opts_widget.setStyleSheet("border: 1px solid red;") # debugging border
        
        scaling_opts_layout = QVBoxLayout(scaling_opts_widget)
        scaling_opts_layout.setAlignment(Qt.AlignCenter)

        scaling_opts_label = QLabel("Scaling Option")
        # scaling_opts_label.setStyleSheet("border: 1px solid red;") # debugging border
        scaling_opts_label.setContentsMargins(*label_contents_margins)
        scaling_opts_label.setFont(label_font)
        scaling_opts_label.setAlignment(Qt.AlignCenter)
        
        # main_prefs_dialog_layout.addWidget(scaling_opts_label)
        middle_items_vbox_left_layout.addWidget(scaling_opts_label)

        orig_size_group_label           = QLabel("No Scaling:")
        self.original_no_scaling_btn    = QRadioButton("Original (no scaling, keep aspect)")

        self.custom_scaling_btn         = QRadioButton("Custom Scaling (keep aspect, use slider > )")

        fill_opts_group_label           = QLabel("Fill:")
        self.fill_ignore_aspect_btn     = QRadioButton("Fill screen (allow distortion)")
        self.fill_keep_aspect_crop_btn  = QRadioButton("Fill screen (keep aspect, crop any excess)")

        fit_opts_group_label            = QLabel("Fit:")
        self.fit_within_screen_btn      = QRadioButton("Fit within screen (keep aspect, no cropping)")
        self.fit_width_to_screen_btn    = QRadioButton("Fit width to screen (crop any excess height)")
        self.fit_height_to_screen_btn   = QRadioButton("Fit height to screen (crop any excess width)")

        # main_prefs_dialog_layout.addWidget(orig_size_group_label)
        scaling_opts_layout.addWidget(self.original_no_scaling_btn)
        scaling_opts_layout.addWidget(self.custom_scaling_btn)
        # main_prefs_dialog_layout.addWidget(fill_opts_group_label)
        scaling_opts_layout.addWidget(self.fill_ignore_aspect_btn)
        scaling_opts_layout.addWidget(self.fill_keep_aspect_crop_btn)
        # main_prefs_dialog_layout.addWidget(fit_opts_group_label)
        scaling_opts_layout.addWidget(self.fit_within_screen_btn)
        scaling_opts_layout.addWidget(self.fit_width_to_screen_btn)
        scaling_opts_layout.addWidget(self.fit_height_to_screen_btn)
        
        scaling_opt_radio_btns = [
            orig_size_group_label, self.original_no_scaling_btn, self.custom_scaling_btn,
            fill_opts_group_label, self.fill_ignore_aspect_btn, self.fill_keep_aspect_crop_btn, 
            fit_opts_group_label, self.fit_within_screen_btn, self.fit_width_to_screen_btn, self.fit_height_to_screen_btn
        ]
        radio_font = QFont('Arial', 10, weight=QFont.Bold)
        for _button in scaling_opt_radio_btns:
            _button.setFont(radio_font)

        scaling_opts_btns_grp.addButton(self.original_no_scaling_btn)
        scaling_opts_btns_grp.addButton(self.custom_scaling_btn)
        scaling_opts_btns_grp.addButton(self.fill_ignore_aspect_btn)
        scaling_opts_btns_grp.addButton(self.fill_keep_aspect_crop_btn)
        scaling_opts_btns_grp.addButton(self.fit_within_screen_btn)
        scaling_opts_btns_grp.addButton(self.fit_width_to_screen_btn)
        scaling_opts_btns_grp.addButton(self.fit_height_to_screen_btn)

        # main_prefs_dialog_layout.addWidget(scaling_opts_widget)
        middle_items_vbox_left_layout.addWidget(scaling_opts_widget)

        self.custom_scaling_slider = QSlider()
        self.custom_scaling_slider.setOrientation(Qt.Vertical)
        self.custom_scaling_slider.setRange(-999, 999)
        self.custom_scaling_slider.setValue(self._cnfg.custom_scaling)
        self.custom_scaling_slider.setFixedWidth(60)

        # Customize the groove and handle
        self.custom_scaling_slider.setStyleSheet("""
            QSlider::groove:vertical {
                background: #aaa;
                width: 8px; /* Adjust the groove width */
                border-radius: 4px;
            }
            QSlider::handle:vertical {
                background-color: #555;
                border: 1px solid #333;
                width: 20px; /* Adjust the handle width */
                height: 20px; /* Adjust the handle height */
                margin: 0 -8px; /* Expand the draggable area */
            }
            QSlider::handle:vertical:focus {
                background-color: #0C90EE;
                border: 1px solid #7B0;
            }
        """)

        middle_items_vbox_right_layout.addWidget(self.custom_scaling_slider)

        main_prefs_dialog_layout.addLayout(middle_items_hbox_layout)

        if self._cnfg.scaling_option == self._cnfg.SCALE_NO_SCALE:
            self.original_no_scaling_btn.setChecked(True)
        elif self._cnfg.scaling_option == self._cnfg.SCALE_CUSTOM:
            self.custom_scaling_btn.setChecked(True)
        elif self._cnfg.scaling_option == self._cnfg.SCALE_FILL_DISTORT:
            self.fill_ignore_aspect_btn.setChecked(True)
        elif self._cnfg.scaling_option == self._cnfg.SCALE_FILL_CROP:
            self.fill_keep_aspect_crop_btn.setChecked(True)
        elif self._cnfg.scaling_option == self._cnfg.SCALE_FIT_NOCROP:
            self.fit_within_screen_btn.setChecked(True)
        elif self._cnfg.scaling_option == self._cnfg.SCALE_FIT_WIDTH:
            self.fit_width_to_screen_btn.setChecked(True)
        elif self._cnfg.scaling_option == self._cnfg.SCALE_FIT_HEIGHT:
            self.fit_height_to_screen_btn.setChecked(True)

        image_path_desc_label = QLabel("Image to Display")
        image_path_desc_label.setFont(QFont('Arial', 12, weight=QFont.Bold))
        image_path_desc_label.setAlignment(Qt.AlignCenter)
        image_path_desc_label.setContentsMargins(*label_contents_margins)
        main_prefs_dialog_layout.addWidget(image_path_desc_label)

        self.image_path_label = QLabel(str(self._cnfg.pixmap_path))
        self.image_path_label.setFont(QFont('Arial', 12))
        main_prefs_dialog_layout.addWidget(self.image_path_label)

        image_path_layout = QHBoxLayout()

        color_picker_button = QPushButton("Background Color")
        color_picker_button.setFont(QFont('Arial', 12, weight=QFont.Bold))
        color_picker_button.setFixedSize(160, 50)
        image_path_layout.addWidget(color_picker_button, 0, Qt.AlignLeft)

        clear_image_button = QPushButton("Clear Image")
        clear_image_button.setFont(QFont('Arial', 12, weight=QFont.Bold))
        clear_image_button.setFixedSize(160, 50)

        image_path_layout.addWidget(clear_image_button, 0, Qt.AlignCenter)

        image_path_button = QPushButton("Change Image")
        image_path_button.setFont(QFont('Arial', 12, weight=QFont.Bold))
        image_path_button.setFixedSize(160, 50)
        image_path_layout.addWidget(image_path_button, 0, Qt.AlignRight)
        
        main_prefs_dialog_layout.addLayout(image_path_layout)
        
        alpha_slider_layout = QVBoxLayout()
        
        alpha_slider_label = QLabel("<< Clear            Background Color Transparency         Opaque >>")
        alpha_slider_label.setAlignment(Qt.AlignCenter)
        alpha_slider_label.setContentsMargins(*label_contents_margins)
        alpha_slider_label.setFont(label_font)
        
        alpha_slider = QSlider()
        alpha_slider.setOrientation(Qt.Horizontal)
        alpha_slider.setFixedHeight(50)
        alpha_slider.setRange(0, 255)
        alpha_slider.setValue(int(self._cnfg.alpha_level, 16))

        # Customize the groove and handle
        alpha_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #aaa;
                height: 8px; /* Adjust the groove height */
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #555;
                border: 1px solid #333;
                width: 20px; /* Adjust the handle width */
                height: 20px; /* Adjust the handle height */
                margin: -8px 0; /* Expand the draggable area */
            }
            QSlider::handle:horizontal:focus {
                background-color: #0C90EE;
                border: 1px solid #7B0;
            }
        """)

        alpha_slider_layout.addWidget(alpha_slider_label)
        alpha_slider_layout.addWidget(alpha_slider)

        main_prefs_dialog_layout.addLayout(alpha_slider_layout)

        self.anchor_point_btn_top_left.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_top_center.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_top_right.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_mid_left.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_mid_center.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_mid_right.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_bot_left.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_bot_center.toggled.connect(self.on_anchor_point_changed)
        self.anchor_point_btn_bot_right.toggled.connect(self.on_anchor_point_changed)

        self.original_no_scaling_btn.toggled.connect(self.on_scaling_option_changed)
        self.custom_scaling_btn.toggled.connect(self.on_scaling_option_changed)
        self.fill_ignore_aspect_btn.toggled.connect(self.on_scaling_option_changed)
        self.fill_keep_aspect_crop_btn.toggled.connect(self.on_scaling_option_changed)
        self.fit_within_screen_btn.toggled.connect(self.on_scaling_option_changed)
        self.fit_width_to_screen_btn.toggled.connect(self.on_scaling_option_changed)
        self.fit_height_to_screen_btn.toggled.connect(self.on_scaling_option_changed)

        self.custom_scaling_slider.valueChanged.connect(self.on_custom_scaling_value_changed)

        color_picker_button.clicked.connect(self.choose_color)

        clear_image_button.clicked.connect(self.emit_clear_image_signal)

        image_path_button.clicked.connect(self.choose_image)

        alpha_slider.valueChanged.connect(self.on_alpha_value_changed)

    def toggle_dark_theme(self):
        if self._cnfg.dark_theme:
            self._cnfg.dark_theme = False
            self.sig_dark_theme_toggled.emit()
        elif not self._cnfg.dark_theme:
            self._cnfg.dark_theme = True
            self.sig_dark_theme_toggled.emit()
        self._cnfg.save_settings()

    def choose_color(self):
        initial_color = QColor(self._cnfg.bg_color)
        color_dialog = ColorDialog(parent=self, cnfg=self._cnfg)
        new_bg_color_rgb = color_dialog.getColor(initial_color)
        new_bg_color_rgba = new_bg_color_rgb.name().replace('#', f'#{self._cnfg.alpha_level}')
        if new_bg_color_rgb.isValid():
            self.sig_new_color_selected.emit(new_bg_color_rgba)
            self._cnfg.save_settings()

    def on_alpha_value_changed(self, value):
        # Convert the decimal value to a two-digit hexadecimal string
        alpha_hex = f"{value:02X}"
        self.sig_alpha_value_changed.emit(alpha_hex)

    def on_custom_scaling_value_changed(self, value):
        self._cnfg.custom_scaling = value
        self._cnfg.scaling_option = self._cnfg.SCALE_CUSTOM
        self.custom_scaling_btn.setChecked(True)
        self.sig_custom_scaling_changed.emit(
            self._cnfg.pixmap_path, 
            self._cnfg.scaling_option, 
            self._cnfg.anchor_point
        )
        self._cnfg.save_settings()

    def emit_clear_image_signal(self):
        self._cnfg.pixmap_path = ""
        self.image_path_label.setText(None)
        self.sig_clear_image_display.emit()

    def choose_image(self):
        if self._cnfg.pixmap_path == "" or self._cnfg.pixmap_path == ".":
            if self._cnfg.recent_image_path == "" or not Path(self._cnfg.recent_image_path).exists():
                browse_path = str(default_image_dir_path)
            else:
                browse_path = str(self._cnfg.recent_image_path)
        else:
            try:
                browse_path = str(Path(self._cnfg.pixmap_path).parent)
            except AttributeError:
                browse_path = str(default_image_dir_path)
        new_image_file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", f"{browse_path}",
            "Image Files (*.png *.jpg *.gif *.bmp)"
        )
        if new_image_file_path:
            current_scaling = self._cnfg.scaling_option
            current_anchor_point = self._cnfg.anchor_point
            self.image_path_label.setText(new_image_file_path)
            self.sig_new_image_selected.emit(new_image_file_path, current_scaling, current_anchor_point)
            self._cnfg.recent_image_path = str(Path(new_image_file_path).parent)
            self._cnfg.save_settings()

    def on_anchor_point_changed(self):
        if self.anchor_point_btn_top_left.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_TOP_LEFT
        elif self.anchor_point_btn_top_center.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_TOP_CENTER
        elif self.anchor_point_btn_top_right.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_TOP_RIGHT
        elif self.anchor_point_btn_mid_left.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_MID_LEFT
        elif self.anchor_point_btn_mid_center.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_MID_CENTER
        elif self.anchor_point_btn_mid_right.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_MID_RIGHT
        elif self.anchor_point_btn_bot_left.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_BOT_LEFT
        elif self.anchor_point_btn_bot_center.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_BOT_CENTER
        elif self.anchor_point_btn_bot_right.isChecked():
            self._cnfg.anchor_point = self._cnfg.ANCHOR_BOT_RIGHT
        self.sig_anchor_point_changed.emit(
            str(self._cnfg.pixmap_path),
            self._cnfg.scaling_option,
            self._cnfg.anchor_point)
        self._cnfg.save_settings()

    def on_scaling_option_changed(self):
        if self.original_no_scaling_btn.isChecked():
            self._cnfg.scaling_option = self._cnfg.SCALE_NO_SCALE
            self.custom_scaling_slider.setValue(0)
            self.original_no_scaling_btn.setChecked(True)
        elif self.custom_scaling_btn.isChecked():
            self._cnfg.scaling_option = self._cnfg.SCALE_CUSTOM
            self.custom_scaling_btn.setChecked(True)
        elif self.fill_ignore_aspect_btn.isChecked():
            self._cnfg.scaling_option = self._cnfg.SCALE_FILL_DISTORT
            self.custom_scaling_slider.setValue(0)
            self.fill_ignore_aspect_btn.setChecked(True)
        elif self.fill_keep_aspect_crop_btn.isChecked():
            self._cnfg.scaling_option = self._cnfg.SCALE_FILL_CROP
            self.custom_scaling_slider.setValue(0)
            self.fill_keep_aspect_crop_btn.setChecked(True)
        elif self.fit_within_screen_btn.isChecked():
            self._cnfg.scaling_option = self._cnfg.SCALE_FIT_NOCROP
            self.custom_scaling_slider.setValue(0)
            self.fit_within_screen_btn.setChecked(True)
        elif self.fit_width_to_screen_btn.isChecked():
            self._cnfg.scaling_option = self._cnfg.SCALE_FIT_WIDTH
            self.custom_scaling_slider.setValue(0)
            self.fit_width_to_screen_btn.setChecked(True)
        elif self.fit_height_to_screen_btn.isChecked():
            self._cnfg.scaling_option = self._cnfg.SCALE_FIT_HEIGHT
            self.custom_scaling_slider.setValue(0)
            self.fit_height_to_screen_btn.setChecked(True)
        self.sig_scaling_opt_changed.emit(
            str(self._cnfg.pixmap_path),
            self._cnfg.scaling_option,
            self._cnfg.anchor_point)
        self._cnfg.save_settings()