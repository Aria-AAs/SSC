"""This module contains the intersection class."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from src.primitives.circle import Circle
from src.primitives.point import Point


class Intersection:
    """Intersection class represents an intersection."""

    def __init__(self, location: Point, connected_roads: list) -> None:
        self.location = location
        self.connected_roads = connected_roads
        self.has_traffic_light = False

    def draw(self, painter: QPainter) -> None:
        """Draw the intersection area using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        Circle(self.location.x, self.location.y, 120).draw(
            painter,
            style=Qt.BrushStyle.NoBrush,
            outline_thickness=5,
            outline_color=QColor(0, 255, 0),
        )
