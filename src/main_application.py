"""This module contains the MainApplication class."""

from math import degrees
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QPaintEvent,
    QPainter,
    QShowEvent,
    QMouseEvent,
    QWheelEvent,
)
from src.items.car import Car
from src.primitives.point import Point
from src.majors.world import World
from src.majors.viewport import Viewport
from data.backups.world_backup import WORLD_BACKUP
from data.backups.viewport_backup import VIEWPORT_BACKUP


class MainApplication(QWidget):
    """The main application that is Inherited from QWidget."""

    w_is_pressed = False
    a_is_pressed = False
    s_is_pressed = False
    d_is_pressed = False
    frames_show_per_second = 30

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        if WORLD_BACKUP:
            self.world = World().load(WORLD_BACKUP)
        else:
            self.world = World()
        self.viewport = None
        self.car = None
        self.base_timer = QTimer(self)
        self.base_timer.timeout.connect(self.run)
        self.graphic_timer = QTimer(self)
        self.graphic_timer.timeout.connect(self.update)

    def start_timers(self) -> None:
        """Start timers of the application."""
        self.base_timer.start(10)
        self.graphic_timer.start(round((1 / self.frames_show_per_second) * 1000))

    def run(self) -> None:
        """A method that runs on base timer timeout and runs the base logic of the application."""
        if self.car.control_type == "user":
            if self.w_is_pressed:
                self.car.accelerate_forward()
            if self.a_is_pressed:
                self.car.turn_steering_wheel(degrees(-0.03))
            if self.s_is_pressed:
                self.car.accelerate_backward()
            if self.d_is_pressed:
                self.car.turn_steering_wheel(degrees(0.03))

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """The mousePressEvent method is an event handler.
        It activates when keys on the mouse are pressed.

        Args:
            event (QMouseEvent | None): An instance contains event information.
        """
        if event.button() == Qt.MouseButton.MiddleButton:
            self.viewport.mouse_middle_button_down(
                Point(event.position().x(), event.position().y())
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        """The mouseMoveEvent method is an event handler.
        It activates when the mouse is moved.

        Args:
            event (QMouseEvent | None): An instance contains event information.
        """
        if self.viewport.drag["active"]:
            self.viewport.mouse_move(Point(event.position().x(), event.position().y()))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        """The mouseReleaseEvent method is an event handler.
        It activates when keys on the keyboard are released.

        Args:
            event (QMouseEvent | None): An instance contains event information.
        """
        if self.viewport.drag["active"]:
            self.viewport.mouse_middle_button_up()
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent | None) -> None:
        """The wheelEvent method is an event handler.
        It activates when the mouse wheel is turned.

        Args:
            event (QWheelEvent | None): An instance contains event information.
        """
        steps = round(event.angleDelta().y() / 120)
        self.viewport.mouse_wheel_scroll(steps)
        super().wheelEvent(event)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """The paintEvent method is an event handler.
        It activates when the QWidget is updated.

        Args:
            event (QPaintEvent | None): An instance contains event information.
        """
        painter = QPainter(self)
        view_point = self.viewport.get_offset().scale(-1)
        self.viewport.reset(painter, self.rect())
        self.world.draw(painter, view_point)
        self.car.update([])
        for sensor in self.car.sensors:
            sensor.draw(painter)
        self.car.draw(painter)
        super().paintEvent(event)

    def resizeEvent(self, event: QShowEvent | None) -> None:
        """The resizeEvent method is an event handler.
        It activates when the QWidget is resized.

        Args:
            event (QShowEvent | None): An instance contains event information.
        """
        self.car = Car(Point(self.width() / 2 - 120, self.height() / 2))
        if VIEWPORT_BACKUP:
            self.viewport = Viewport(
                self.width() / 2,
                self.height() / 2,
                VIEWPORT_BACKUP["zoom"],
                VIEWPORT_BACKUP["offset"],
            )
        else:
            self.viewport = Viewport(self.width() / 2, self.height() / 2)
        super().resizeEvent(event)
        self.start_timers()
