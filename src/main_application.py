"""This module contains the MainApplication class."""

from math import degrees, inf
from random import choice
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
from src.editors.cross_editor import CrossEditor
from src.editors.park_editor import ParkEditor
from src.editors.start_editor import StartEditor
from src.editors.stop_editor import StopEditor
from src.editors.target_editor import TargetEditor
from src.editors.traffic_light_editor import TrafficLightEditor
from src.editors.yield_editor import YieldEditor
from src.maths.graph import Graph
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
        self.editors = {
            "graph": GraphEditor(self.world),
        }
        self.editors["cross_editor"] = CrossEditor(self.editors["graph"])
        self.editors["park_editor"] = ParkEditor(self.editors["graph"])
        self.editors["start_editor"] = StartEditor(self.editors["graph"])
        self.editors["stop_editor"] = StopEditor(self.editors["graph"])
        self.editors["target_editor"] = TargetEditor(self.editors["graph"])
        self.editors["traffic_light_editor"] = TrafficLightEditor(self.editors["graph"])
        self.editors["yield_editor"] = YieldEditor(self.editors["graph"])
        self.active_editor = None
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
            if self.editors["graph"].graph != self.world.graph:
                self.editors["graph"].world.generate_roads()
                self.world.graph = Graph(
                    self.editors["graph"].world.graph.points,
                    self.editors["graph"].world.graph.segments,
                )
                self.minimap = Minimap(
                    self.world.graph, self.best_car, self.width(), self.height()
                )
            elif self.editors["graph"].world.markings != self.world.markings:
                self.world = self.editors["graph"].world
            pos = QCursor.pos()
            pos = self.mapFromGlobal(pos)
            if pos != self._cursor:
                self._cursor = pos
                self.editors[self.active_editor].mouse_move(
                    Point(pos.x(), pos.y()), self.viewport
                )

    def signals(self, signals: dict) -> None:
        """Get signals from main_window for changing the state of the program.

        Args:
            signals (dict): The given signal to change the state of the program.
        """
        for signal, value in signals.items():
            self.disable_editors()
            if signal == "application_mode":
                self.application_mode = value
                if value == "run":
                    self.set_to_start()
                    self.world.generate()
                    self.road_borders.clear()
                    for segment in self.world.road_borders:
                        self.road_borders.append(Polygon([segment.start, segment.end]))
                elif value == "edit":
                    self.signals({"editor_mode": "graph"})
            elif signal == "editor_mode":
                if value == "graph":
                    self.editors["graph"] = GraphEditor(self.world)
                    self.editors["graph"].world.generate_roads()
                    if self.active_editor:
                        self.editors["graph"].world.markings = self.editors[
                            self.active_editor
                        ].graph_editor.world.markings
                    self.active_editor = "graph"
                elif value == "cross_editor":
                    self.editors["cross_editor"] = CrossEditor(self.editors["graph"])
                    self.active_editor = "cross_editor"
                elif value == "park_editor":
                    self.editors["park_editor"] = ParkEditor(self.editors["graph"])
                    self.active_editor = "park_editor"
                elif value == "start_editor":
                    self.editors["start_editor"] = StartEditor(self.editors["graph"])
                    self.active_editor = "start_editor"
                elif value == "stop_editor":
                    self.editors["stop_editor"] = StopEditor(self.editors["graph"])
                    self.active_editor = "stop_editor"
                elif value == "target_editor":
                    self.editors["target_editor"] = TargetEditor(self.editors["graph"])
                    self.active_editor = "target_editor"
                elif value == "traffic_light_editor":
                    self.editors["traffic_light_editor"] = TrafficLightEditor(
                        self.editors["graph"]
                    )
                    self.active_editor = "traffic_light_editor"
                elif value == "yield_editor":
                    self.editors["yield_editor"] = YieldEditor(self.editors["graph"])
                    self.active_editor = "yield_editor"

    def disable_editors(self) -> None:
        """Disable the functionality of all editors."""
        for value in self.editors.values():
            value.disable()

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
        start_markings = []
        for marking in self.world.markings:
            if marking.type == "start":
                start_markings.append(marking)
        cars = []
        for _ in range(count):
            start_point = Point(self.width() / 2 - 120, self.height() / 2)
            start_angle = 0
            if start_markings:
                start_marking = choice(start_markings)
                start_point = Point(
                    start_marking.center_of_segment.x, start_marking.center_of_segment.y
                )
                start_angle = degrees(start_marking.direction_of_segment.angle()) - 90
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
                self.editors[self.active_editor].mouse_left_button_down()
            elif event.button() == Qt.MouseButton.RightButton:
                if self.active_editor == "graph":
                    self.editors["graph"].mouse_right_button_down()
                else:
                    self.editors[self.active_editor].mouse_right_button_down(
                        Point(event.position().x(), event.position().y()), self.viewport
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
        if self.application_mode == "edit":
            if event.button() == Qt.MouseButton.LeftButton:
                if self.active_editor == "graph":
                    self.editors["graph"].mouse_left_button_up()
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
            for road in self.editors["graph"].world.roads:
                road.draw(
                    painter_1,
                    color=QColor(51, 51, 51),
                    outline_width=15,
                    outline_color=QColor(51, 51, 51),
                )
            for segment in self.editors["graph"].graph.segments:
                segment.draw(
                    painter_1,
                    color=QColor(255, 255, 255),
                    width=4,
                    dash_style=[5, 5],
                )
            for segment in self.editors["graph"].world.road_borders:
                segment.draw(painter_1, color=QColor(255, 255, 255), width=4)
            for marking in self.editors["graph"].world.markings:
                marking.draw(painter_1)
            self.editors[self.active_editor].draw(painter_1, self.viewport.zoom)
        painter_2 = QPainter(self)
        self.minimap.draw(painter_2, view_point)
        painter_2.setPen(QPen(QColor(255, 128, 20), 1, Qt.PenStyle.SolidLine))
        painter_2.drawText(
            QRect(40, 30, 400, 30),
            Qt.AlignmentFlag.AlignLeft,
            f"{hours:02d} : {minutes:02d} : {seconds:02d}",
        )
        super().paintEvent(event)
