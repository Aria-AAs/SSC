"""This module contains the MainApplication class."""

from math import degrees, inf
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import (
    QPaintEvent,
    QShowEvent,
    QMouseEvent,
    QWheelEvent,
    QPainter,
    QCursor,
    QPen,
    QColor,
)
from src.items.car import Car
from src.primitives.point import Point
from src.primitives.polygon import Polygon
from src.majors.world import World
from src.majors.viewport import Viewport
from src.majors.minimap import Minimap
from src.editors.graph_editor import GraphEditor
from data.backups.world_backup import WORLD_BACKUP
from data.backups.viewport_backup import VIEWPORT_BACKUP


class MainApplication(QWidget):
    """The main application that is Inherited from QWidget."""

    number_of_ai_cars = 50
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
        self.setStyleSheet("QWidget{font-size:20px;}")
        self.application_mode = "run"
        self.clock_counter_variable = 0
        if WORLD_BACKUP:
            self.world = World().load(WORLD_BACKUP)
        else:
            self.world = World()
        self.graph_editor = GraphEditor(self.world.graph)
        self.road_borders = []
        for segment in self.world.road_borders:
            self.road_borders.append(Polygon([segment.start, segment.end]))
        self.viewport = None
        self.minimap = None
        self.cars = []
        self.best_car = None
        self.base_timer = QTimer(self)
        self.base_timer.timeout.connect(self.run)
        self.graphic_timer = QTimer(self)
        self.graphic_timer.timeout.connect(self.update)
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clock_counter)
        self._cursor = None

    def start_timers(self) -> None:
        """Start timers of the application."""
        self.clock.start(1000)
        self.base_timer.start(10)
        self.graphic_timer.start(round((1 / self.frames_show_per_second) * 1000))

    def clock_counter(self) -> None:
        """Count every second."""
        self.clock_counter_variable += 1

    def run(self) -> None:
        """A method that runs on base timer timeout and runs the base logic of the application."""
        if self.application_mode == "run":
            if self.best_car.control_type == "user":
                if self.w_is_pressed:
                    self.best_car.accelerate_forward()
                if self.a_is_pressed:
                    self.best_car.turn_steering_wheel(degrees(-0.03))
                if self.s_is_pressed:
                    self.best_car.accelerate_backward()
                if self.d_is_pressed:
                    self.best_car.turn_steering_wheel(degrees(0.03))
            best_fitness = -inf
            for car in self.cars:
                car.update(self.road_borders)
                if car.fitness > best_fitness:
                    best_fitness = car.fitness
                    self.best_car = car
            self.minimap.update(self.best_car)
        elif self.application_mode == "edit":
            pos = QCursor.pos()
            pos = self.mapFromGlobal(pos)
            if pos != self._cursor:
                self._cursor = pos
                self.graph_editor.mouse_move(Point(pos.x(), pos.y()), self.viewport)

    def signals(self, signals: dict) -> None:
        """Get signals from main_window for changing the state of the program.

        Args:
            signals (dict): The given signal to change the state of the program.
        """
        for signal, value in signals.items():
            if signal == "application_mode":
                self.application_mode = value
                if value == "run":
                    self.graph_editor.selected = None
                    self.graph_editor.hovered = None
                    self.set_to_start()
                    self.world.graph = self.graph_editor.graph
                    self.world.generate()
                elif value == "edit":
                    self.graph_editor.graph = self.world.graph

    def set_to_start(self) -> None:
        """Setup the application parameter to start running."""
        self.cars = self.generate_cars(self.number_of_ai_cars)
        for car in self.cars:
            car.update([])
        self.best_car = self.cars[0]

    def generate_cars(self, count: int) -> list:
        """Generate a list of cars as many as the given count.

        Args:
            count (int): Number of cars to generate.

        Returns:
            list: List of cars.
        """
        cars = []
        for _ in range(count):
            start_point = Point(self.width() / 2 - 120, self.height() / 2)
            start_angle = 0
            cars.append(Car(start_point, start_angle, "ai"))
        return cars

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
        if self.application_mode == "edit":
            if event.button() == Qt.MouseButton.LeftButton:
                self.graph_editor.mouse_left_button_down(
                    Point(event.position().x(), event.position().y())
                )
            elif event.button() == Qt.MouseButton.RightButton:
                self.graph_editor.mouse_right_button_down()

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
        if self.application_mode == "edit":
            if event.button() == Qt.MouseButton.LeftButton:
                self.graph_editor.mouse_left_button_up()
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

    def resizeEvent(self, event: QShowEvent | None) -> None:
        """The resizeEvent method is an event handler.
        It activates when the QWidget is resized.

        Args:
            event (QShowEvent | None): An instance contains event information.
        """
        if VIEWPORT_BACKUP:
            self.viewport = Viewport(
                self.width() / 2,
                self.height() / 2,
                VIEWPORT_BACKUP["zoom"],
                VIEWPORT_BACKUP["offset"],
            )
        else:
            self.viewport = Viewport(self.width() / 2, self.height() / 2)
        self.set_to_start()
        self.minimap = Minimap(
            self.world.graph, self.best_car, self.width(), self.height()
        )
        super().resizeEvent(event)
        self.start_timers()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """The paintEvent method is an event handler.
        It activates when the QWidget is updated.

        Args:
            event (QPaintEvent | None): An instance contains event information.
        """
        minutes, seconds = divmod(self.clock_counter_variable, 60)
        hours, minutes = divmod(minutes, 60)
        painter_1 = QPainter(self)
        view_point = self.viewport.get_offset().scale(-1)
        self.viewport.reset(painter_1, self.rect())
        if self.application_mode == "run":
            self.world.draw(painter_1, view_point)
            for sensor in self.best_car.sensors:
                sensor.draw(painter_1)
            for car in self.cars:
                car.draw(painter_1, 0.15)
            self.best_car.draw(painter_1)
        elif self.application_mode == "edit":
            self.graph_editor.draw(painter_1, self.viewport.zoom)
        painter_2 = QPainter(self)
        self.minimap.draw(painter_2, view_point)
        painter_2.setPen(QPen(QColor(255, 128, 20), 1, Qt.PenStyle.SolidLine))
        painter_2.drawText(
            QRect(40, 30, 400, 30),
            Qt.AlignmentFlag.AlignLeft,
            f"{hours:02d} : {minutes:02d} : {seconds:02d}",
        )
        super().paintEvent(event)
