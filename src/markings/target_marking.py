"""This module contains the TargetMarking class."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.markings.marking import Marking


class TargetMarking(Marking):
    """TargetMarking class represents a target marking. Inherited from Marking."""

    def __init__(
        self,
        center_of_segment: Point,
        direction_of_segment: Point,
        width: float,
        height: float,
    ) -> None:
        super().__init__(center_of_segment, direction_of_segment, width, height)
        self.borders = [self.polygon.segments[0]]
        self.type = "target"

    def draw(self, painter: QPainter) -> None:
        """Draw the target marking using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        if len(self.polygon.segments) == 4:
            self.polygon.segments[0].draw(
                painter,
                5,
                color=QColor(255, 0, 0),
                cap_style=Qt.PenCapStyle.FlatCap,
            )
            self.polygon.segments[2].draw(
                painter,
                5,
                color=QColor(255, 0, 0),
                cap_style=Qt.PenCapStyle.FlatCap,
            )
            self.polygon.segments[0].draw(
                painter,
                5,
                color=QColor(255, 255, 0),
                dash_style=[1, 1],
                cap_style=Qt.PenCapStyle.FlatCap,
            )
            self.polygon.segments[2].draw(
                painter,
                5,
                color=QColor(255, 255, 0),
                dash_style=[1, 1],
                cap_style=Qt.PenCapStyle.FlatCap,
            )
