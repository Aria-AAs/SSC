"""This module contains the MainWindow class."""

from pathlib2 import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
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
        self.application_mode_button = QPushButton("🖊")
        self.application_mode_button.clicked.connect(self.change_application_mode)
        self.main_application_buttons_layout.addWidget(self.application_mode_button)
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

    def change_application_mode(self) -> None:
        """Change the application mode when application_mode_button is clicked."""
        if self.application_mode_button.text() == "🖊":
            self.application_mode_button.setText("🚗")
            self.main_application.signals({"application_mode": "edit"})
        else:
            self.application_mode_button.setText("🖊")
            self.main_application.signals({"application_mode": "run"})

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
