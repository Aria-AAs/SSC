"""This module contains the MainWindow class."""

from pathlib2 import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QDoubleSpinBox,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QKeyEvent
from src.main_application import MainApplication


class MainWindow(QWidget):
    """The main window of the application is Inherited from QWidget."""

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window,
    ) -> None:
        super().__init__(parent, flags)
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the UI of the main window."""
        self.setStyleSheet("QWidget{background-color:#777777;color:#000000;}")
        self.setWindowTitle("Self-driving Smart Cars")
        self.setGeometry(-1920, 0, 1920, 1080)
        self.showFullScreen()
        self.setWindowIcon(
            QIcon(str(Path(Path(__file__).parent.parent, "asset/images/f1_car.png")))
        )
        self.main_window_layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.app_name_and_icon_layout = QHBoxLayout()
        self.app_icon_label = QLabel("")
        self.app_icon_label.setPixmap(
            QIcon(
                str(Path(Path(__file__).parent.parent, "asset/images/f1_car.png"))
            ).pixmap(QSize(16, 16))
        )
        self.app_name_and_icon_layout.addWidget(self.app_icon_label)
        self.app_nama_label = QLabel("Self-driving Smart Cars")
        self.app_name_and_icon_layout.addWidget(self.app_nama_label)
        self.app_name_and_icon_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.header_layout.addLayout(self.app_name_and_icon_layout)
        self.main_application_buttons_layout = QHBoxLayout()
        self.application_mode_layout = QHBoxLayout()
        self.application_save_button = QPushButton("💾")
        self.application_save_button.clicked.connect(self.save)
        self.application_save_button.setMaximumWidth(30)
        self.application_mode_layout.addWidget(self.application_save_button)
        self.application_load_button = QPushButton("📂")
        self.application_load_button.clicked.connect(self.load)
        self.application_load_button.setMaximumWidth(30)
        self.application_mode_layout.addWidget(self.application_load_button)
        self.application_mode_button = QPushButton("🖊")
        self.application_mode_button.clicked.connect(self.change_application_mode)
        self.application_mode_button.setMaximumWidth(30)
        self.application_mode_layout.addWidget(self.application_mode_button)
        self.application_mode_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.main_application_buttons_layout.addLayout(self.application_mode_layout)
        self.graph_editor_option_layout = QHBoxLayout()
        self.edit_mode_button = QPushButton("⬆")
        self.edit_mode_button.clicked.connect(self.toggle_edit_mode)
        self.edit_mode_button.setMaximumWidth(30)
        self.edit_mode_button.hide()
        self.graph_editor_option_layout.addWidget(self.edit_mode_button)
        self.set_road_to_oneway_checkbox = QCheckBox()
        self.set_road_to_oneway_checkbox.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft
        )
        self.set_road_to_oneway_checkbox.setToolTip("One way road")
        self.set_road_to_oneway_checkbox.toggled.connect(self.toggle_oneway)
        self.set_road_to_oneway_checkbox.hide()
        self.graph_editor_option_layout.addWidget(self.set_road_to_oneway_checkbox)
        self.number_of_left_lanes = QDoubleSpinBox()
        self.number_of_left_lanes.setDecimals(0)
        self.number_of_left_lanes.setRange(1, 4)
        self.number_of_left_lanes.setValue(2)
        self.number_of_left_lanes.setToolTip("Number of lanes in left side of the road")
        self.number_of_left_lanes.valueChanged.connect(self.change_number_of_left_lanes)
        self.number_of_left_lanes.hide()
        self.graph_editor_option_layout.addWidget(self.number_of_left_lanes)
        self.number_of_right_lanes = QDoubleSpinBox()
        self.number_of_right_lanes.setDecimals(0)
        self.number_of_right_lanes.setRange(1, 4)
        self.number_of_right_lanes.setValue(2)
        self.number_of_right_lanes.setToolTip(
            "Number of lanes in right side of the road"
        )
        self.number_of_right_lanes.valueChanged.connect(
            self.change_number_of_right_lanes
        )
        self.number_of_right_lanes.hide()
        self.graph_editor_option_layout.addWidget(self.number_of_right_lanes)
        self.main_application_buttons_layout.addLayout(self.graph_editor_option_layout)
        self.editor_buttons_layout = QHBoxLayout()
        self.graph_editor_button = QPushButton("🌐")
        self.graph_editor_button.clicked.connect(self.graph_editor_activator)
        self.editor_buttons_layout.addWidget(self.graph_editor_button)
        self.graph_editor_button.hide()
        self.graph_editor_button.setMaximumWidth(30)
        self.start_marking_editor_button = QPushButton("🚙")
        self.start_marking_editor_button.clicked.connect(
            self.start_marking_editor_activator
        )
        self.editor_buttons_layout.addWidget(self.start_marking_editor_button)
        self.start_marking_editor_button.hide()
        self.start_marking_editor_button.setMaximumWidth(30)
        self.target_marking_editor_button = QPushButton("🎯")
        self.target_marking_editor_button.clicked.connect(
            self.target_marking_editor_activator
        )
        self.editor_buttons_layout.addWidget(self.target_marking_editor_button)
        self.target_marking_editor_button.hide()
        self.target_marking_editor_button.setMaximumWidth(30)
        self.yield_marking_editor_button = QPushButton("⚠")
        self.yield_marking_editor_button.clicked.connect(
            self.yield_marking_editor_activator
        )
        self.editor_buttons_layout.addWidget(self.yield_marking_editor_button)
        self.yield_marking_editor_button.hide()
        self.yield_marking_editor_button.setMaximumWidth(30)
        self.stop_marking_editor_button = QPushButton("🛑")
        self.stop_marking_editor_button.clicked.connect(
            self.stop_marking_editor_activator
        )
        self.editor_buttons_layout.addWidget(self.stop_marking_editor_button)
        self.stop_marking_editor_button.hide()
        self.stop_marking_editor_button.setMaximumWidth(30)
        self.traffic_light_marking_editor_button = QPushButton("🚦")
        self.traffic_light_marking_editor_button.clicked.connect(
            self.traffic_light_marking_editor_activator
        )
        self.editor_buttons_layout.addWidget(self.traffic_light_marking_editor_button)
        self.traffic_light_marking_editor_button.hide()
        self.traffic_light_marking_editor_button.setMaximumWidth(30)
        self.cross_marking_editor_button = QPushButton("🚶🏻‍♂️")
        self.cross_marking_editor_button.clicked.connect(
            self.cross_marking_editor_activator
        )
        self.editor_buttons_layout.addWidget(self.cross_marking_editor_button)
        self.cross_marking_editor_button.hide()
        self.cross_marking_editor_button.setMaximumWidth(30)
        self.park_marking_editor_button = QPushButton("🅿")
        self.park_marking_editor_button.clicked.connect(
            self.park_marking_editor_activator
        )
        self.editor_buttons_layout.addWidget(self.park_marking_editor_button)
        self.park_marking_editor_button.hide()
        self.park_marking_editor_button.setMaximumWidth(30)
        self.main_application_buttons_layout.addLayout(self.editor_buttons_layout)
        self.header_layout.addLayout(self.main_application_buttons_layout)
        self.application_buttons_layout = QHBoxLayout()
        self.minimize_pushbutton = QPushButton(
            QIcon(str(Path(Path(__file__).parent.parent, "asset/icons/minimize.png"))),
            "",
        )
        self.minimize_pushbutton.clicked.connect(self.showMinimized)
        self.application_buttons_layout.addWidget(self.minimize_pushbutton)
        self.close_pushbutton = QPushButton(
            QIcon(str(Path(Path(__file__).parent.parent, "asset/icons/close.png"))), ""
        )
        self.close_pushbutton.clicked.connect(self.close)
        self.application_buttons_layout.addWidget(self.close_pushbutton)
        self.application_buttons_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.header_layout.addLayout(self.application_buttons_layout)
        self.main_window_layout.addLayout(self.header_layout)
        self.main_application_layout = QVBoxLayout()
        self.main_application = MainApplication()
        self.main_application_layout.addWidget(self.main_application)
        self.main_window_layout.addLayout(self.main_application_layout)
        self.setLayout(self.main_window_layout)

    def save(self) -> None:
        """Save the state of main_application"""
        self.main_application.save()

    def load(self) -> None:
        """Load a state of main_application"""
        self.main_application.load()

    def toggle_oneway(self) -> None:
        """_summary_"""
        if self.set_road_to_oneway_checkbox.isChecked():
            self.number_of_left_lanes.setRange(0, 0)
            self.number_of_left_lanes.setValue(0)
            self.number_of_left_lanes.setDisabled(True)
            self.number_of_right_lanes.setRange(1, 8)
            self.main_application.signals({"graph_editor_set_oneway_road": True})
        else:
            self.number_of_left_lanes.setRange(1, 4)
            self.number_of_left_lanes.setValue(2)
            self.number_of_left_lanes.setDisabled(False)
            self.number_of_right_lanes.setRange(1, 4)
            if self.number_of_right_lanes.value() > 4:
                self.number_of_right_lanes.setValue(4)
            self.main_application.signals({"graph_editor_set_oneway_road": False})

    def change_number_of_left_lanes(self) -> None:
        """_summary_"""
        self.main_application.signals(
            {
                "graph_editor_set_number_of_left_lanes": int(
                    self.number_of_left_lanes.value()
                )
            }
        )

    def change_number_of_right_lanes(self) -> None:
        """_summary_"""
        self.main_application.signals(
            {
                "graph_editor_set_number_of_right_lanes": int(
                    self.number_of_right_lanes.value()
                )
            }
        )

    def toggle_edit_mode(self) -> None:
        """toggle the graph editor mode when the edit_mode_button is clicked."""
        if self.edit_mode_button.text() == "⬆":
            self.edit_mode_button.setText("🔃")
        else:
            self.edit_mode_button.setText("⬆")

    def enable_editors_buttons(self) -> None:
        """Reset and enable buttons of all editors."""
        self.set_road_to_oneway_checkbox.hide()
        self.number_of_left_lanes.hide()
        self.number_of_right_lanes.hide()
        self.edit_mode_button.hide()
        self.graph_editor_button.setDisabled(False)
        self.graph_editor_button.setStyleSheet("QPushButton{background-color:#777777;}")
        self.start_marking_editor_button.setDisabled(False)
        self.start_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#777777;}"
        )
        self.target_marking_editor_button.setDisabled(False)
        self.target_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#777777;}"
        )
        self.yield_marking_editor_button.setDisabled(False)
        self.yield_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#777777;}"
        )
        self.stop_marking_editor_button.setDisabled(False)
        self.stop_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#777777;}"
        )
        self.traffic_light_marking_editor_button.setDisabled(False)
        self.traffic_light_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#777777;}"
        )
        self.cross_marking_editor_button.setDisabled(False)
        self.cross_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#777777;}"
        )
        self.park_marking_editor_button.setDisabled(False)
        self.park_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#777777;}"
        )

    def change_application_mode(self) -> None:
        """Change the application mode when the application_mode_button is clicked."""
        self.enable_editors_buttons()
        if self.application_mode_button.text() == "🖊":
            self.application_mode_button.setText("🚗")
            self.graph_editor_button.show()
            self.graph_editor_button.setDisabled(True)
            self.graph_editor_button.setStyleSheet(
                "QPushButton{background-color:#555555;}"
            )
            self.start_marking_editor_button.show()
            self.target_marking_editor_button.show()
            self.yield_marking_editor_button.show()
            self.stop_marking_editor_button.show()
            self.traffic_light_marking_editor_button.show()
            self.cross_marking_editor_button.show()
            self.park_marking_editor_button.show()
            self.set_road_to_oneway_checkbox.show()
            self.number_of_left_lanes.show()
            self.number_of_right_lanes.show()
            self.edit_mode_button.show()
            self.main_application.signals({"application_mode": "edit"})
        else:
            self.application_mode_button.setText("🖊")
            self.graph_editor_button.hide()
            self.start_marking_editor_button.hide()
            self.target_marking_editor_button.hide()
            self.yield_marking_editor_button.hide()
            self.stop_marking_editor_button.hide()
            self.traffic_light_marking_editor_button.hide()
            self.cross_marking_editor_button.hide()
            self.park_marking_editor_button.hide()
            self.main_application.signals({"application_mode": "run"})

    def graph_editor_activator(self) -> None:
        """Activate the graph editor when the graph_editor_button button is clicked."""
        self.enable_editors_buttons()
        self.graph_editor_button.setDisabled(True)
        self.graph_editor_button.setStyleSheet("QPushButton{background-color:#555555;}")
        self.main_application.signals({"editor_mode": "graph"})
        self.set_road_to_oneway_checkbox.show()
        self.number_of_left_lanes.show()
        self.number_of_right_lanes.show()
        self.edit_mode_button.show()

    def start_marking_editor_activator(self) -> None:
        """Activate the start marking editor when the start_marking_editor_button
        button is clicked.
        """
        self.enable_editors_buttons()
        self.start_marking_editor_button.setDisabled(True)
        self.start_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#555555;}"
        )
        self.main_application.signals({"editor_mode": "start_editor"})

    def target_marking_editor_activator(self) -> None:
        """Activate the target marking editor when the target_marking_editor_button
        button is clicked.
        """
        self.enable_editors_buttons()
        self.target_marking_editor_button.setDisabled(True)
        self.target_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#555555;}"
        )
        self.main_application.signals({"editor_mode": "target_editor"})

    def yield_marking_editor_activator(self) -> None:
        """Activate the yield marking editor when the yield_marking_editor_button
        button is clicked.
        """
        self.enable_editors_buttons()
        self.yield_marking_editor_button.setDisabled(True)
        self.yield_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#555555;}"
        )
        self.main_application.signals({"editor_mode": "yield_editor"})

    def stop_marking_editor_activator(self) -> None:
        """Activate the stop marking editor when the stop_marking_editor_button
        button is clicked.
        """
        self.enable_editors_buttons()
        self.stop_marking_editor_button.setDisabled(True)
        self.stop_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#555555;}"
        )
        self.main_application.signals({"editor_mode": "stop_editor"})

    def traffic_light_marking_editor_activator(self) -> None:
        """Activate the traffic light marking editor when the traffic_light_marking_editor_button
        button is clicked.
        """
        self.enable_editors_buttons()
        self.traffic_light_marking_editor_button.setDisabled(True)
        self.traffic_light_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#555555;}"
        )
        self.main_application.signals({"editor_mode": "traffic_light_editor"})

    def cross_marking_editor_activator(self) -> None:
        """Activate the cross marking editor when the cross_marking_editor_button
        button is clicked.
        """
        self.enable_editors_buttons()
        self.cross_marking_editor_button.setDisabled(True)
        self.cross_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#555555;}"
        )
        self.main_application.signals({"editor_mode": "cross_editor"})

    def park_marking_editor_activator(self) -> None:
        """Activate the park marking editor when the park_marking_editor_button
        button is clicked.
        """
        self.enable_editors_buttons()
        self.park_marking_editor_button.setDisabled(True)
        self.park_marking_editor_button.setStyleSheet(
            "QPushButton{background-color:#555555;}"
        )
        self.main_application.signals({"editor_mode": "park_editor"})

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        """The keyPressEvent method is an event handler.
        It activates when keys on the keyboard are pressed.

        Args:
            event (QKeyEvent | None): An instance contains event information.
        """
        key = event.key()
        if key == Qt.Key.Key_W:
            self.main_application.w_is_pressed = True
        elif key == Qt.Key.Key_A:
            self.main_application.a_is_pressed = True
        elif key == Qt.Key.Key_S:
            self.main_application.s_is_pressed = True
        elif key == Qt.Key.Key_D:
            self.main_application.d_is_pressed = True
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent | None) -> None:
        """The keyReleaseEvent method is an event handler.
        It activates when keys on the keyboard are released.

        Args:
            event (QKeyEvent | None): An instance contains event information.
        """
        key = event.key()
        if key == Qt.Key.Key_W:
            self.main_application.w_is_pressed = False
        elif key == Qt.Key.Key_A:
            self.main_application.a_is_pressed = False
        elif key == Qt.Key.Key_S:
            self.main_application.s_is_pressed = False
        elif key == Qt.Key.Key_D:
            self.main_application.d_is_pressed = False
        super().keyReleaseEvent(event)
