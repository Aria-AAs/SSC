"""This module contains the CrossMarking class."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.segment import Segment
from src.markings.marking import Marking


class CrossMarking(Marking):
    """CrossMarking class represents a cross marking. Inherited from Marking."""

    def __init__(
        self,
        center_of_segment: Point,
        direction_of_segment: Point,
        width: float,
        height: float,
    ) -> None:
        super().__init__(center_of_segment, direction_of_segment, width, height)
        self.borders = [self.polygon.segments[0], self.polygon.segments[2]]
        self.type = "cross"

    def draw(self, painter: QPainter) -> None:
        """Draw the cross marking using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        perpendicular = self.direction_of_segment.mirror_about_y_axis()
        line = Segment(
            self.center_of_segment + perpendicular.scale(self.width / 2),
            self.center_of_segment + perpendicular.scale(-self.width / 2),
        )
        line.draw(
            painter,
            self.height,
            color=QColor(255, 255, 255),
            dash_style=[2 / 11, 2 / 11],
            cap_style=Qt.PenCapStyle.FlatCap,
        )
