from math import degrees
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPaintEvent, QPainter, QColor, QShowEvent
from src.items.car import Car
from src.primitives.point import Point


class MainApplication(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.car = None
        self.w_is_pressed = False
        self.a_is_pressed = False
        self.s_is_pressed = False
        self.d_is_pressed = False
        self.frames_show_per_second = 30
        self.graphic_timer = QTimer(self)
        self.graphic_timer.timeout.connect(self.update)
        self.graphic_timer.start(round((1 / self.frames_show_per_second) * 1000))
        self.base_timer = QTimer(self)
        self.base_timer.timeout.connect(self.run)
        self.base_timer.start(10)

    def run(self) -> None:
        if self.car.control_type == "user":
            if self.w_is_pressed:
                self.car.accelerate_forward()
            if self.a_is_pressed:
                self.car.turn_steering_wheel(degrees(-0.03))
            if self.s_is_pressed:
                self.car.accelerate_backward()
            if self.d_is_pressed:
                self.car.turn_steering_wheel(degrees(0.03))

    def paintEvent(self, event: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(50, 50, 50))

        self.car.update([])
        for sensor in self.car.sensors:
            sensor.draw(painter)
        self.car.draw(painter)
        return super().paintEvent(event)

    def showEvent(self, event: QShowEvent | None) -> None:
        self.car = Car(Point(self.width() / 2, self.height() / 2))
        return super().showEvent(event)
