"""This is the main module of the application. Run it to run the program."""

from sys import argv
from sys import exit as ex
from PyQt6.QtWidgets import QApplication
from src.main_window import MainWindow


if __name__ == "__main__":
    application = QApplication(argv)
    application.setStyle("Fusion")
    main_window = MainWindow()
    ex(application.exec())
