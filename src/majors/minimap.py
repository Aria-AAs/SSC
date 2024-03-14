"""This module contains the Minimap class."""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath
from src.items.car import Car
from src.primitives.point import Point
from src.primitives.circle import Circle


class Minimap:
    """Minimap class represents a minimap."""

    scaler = 0.05
    size = 1 / 4
    margin = 30

    def __init__(self, graph, car: Car, app_width, app_height) -> None:
        self.graph = graph
        self.app_width = app_width
        self.app_height = app_height
        self.car_position = car.position

    def update(self, car: Car):
        """Update the position of the car.

        Args:
            car (Car): Car to update the position.
        """
        self.car_position = car.position

    def draw(self, painter: QPainter, view_point: Point) -> None:
        """Draw the minimap using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            view_point (Point): The center of the viewport.
        """
        radius = self.app_height * self.size / 2
        position = Point(
            self.app_width - radius - self.margin,
            radius + self.margin,
        )
        background = Circle(0, 0, radius)
        red_dot = Circle(
            (self.car_position.x - view_point.x) * self.scaler,
            (self.car_position.y - view_point.y) * self.scaler,
            0.15 / self.scaler,
        )
        scaled_view_point = view_point.scale(-self.scaler)
        base_path = painter.clipPath()
        minimap_path = QPainterPath()
        minimap_path.addEllipse(0, 0, radius * 2, radius * 2)
        painter.save()
        painter.translate(position.x, position.y)
        background.draw(
            painter,
            QColor(5, 113, 5),
            outline_thickness=-1,
            outline_color=QColor(5, 113, 5),
            transparency=0.7,
        )
        painter.translate(
            -radius,
            -radius,
        )
        painter.setClipPath(minimap_path)
        painter.translate(
            scaled_view_point.x + radius,
            scaled_view_point.y + radius,
        )
        painter.scale(self.scaler, self.scaler)
        for segment in self.graph.segments:
            segment.draw(
                painter,
                3 / self.scaler,
                Qt.PenCapStyle.RoundCap,
                [],
                QColor(255, 255, 255),
            )
        painter.scale(1 / self.scaler, 1 / self.scaler)
        painter.translate(
            -scaled_view_point.x,
            -scaled_view_point.y,
        )
        red_dot.draw(
            painter,
            QColor(255, 0, 0),
        )
        painter.setClipPath(base_path)
        painter.restore()
        rect = QRectF(position.x - radius, position.y - radius, radius * 2, radius * 2)
        painter.setPen(QPen(QColor(0, 80, 0), 0.2 / self.scaler, Qt.PenStyle.SolidLine))
        painter.drawArc(rect, 0, 360 * 16)
