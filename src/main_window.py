"""This module contains the MainWindow class."""

from pathlib2 import Path
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon


class MainWindow(QWidget):
    """The main window of the application is Inherited from QWidget."""

    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the UI of the main window."""
        self.setStyleSheet("QWidget{background-color:#777777;color:#000000;}")
        self.setWindowTitle("Self-driving Smart Cars")
        self.showFullScreen()
        self.setWindowIcon(
            QIcon(str(Path(Path(__file__).parent.parent, "asset/images/f1_car.png")))
        )
