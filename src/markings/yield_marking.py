"""This module contains the YieldMarking class."""

from math import degrees
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.markings.marking import Marking


class YieldMarking(Marking):
    """YieldMarking class represents a yield marking. Inherited from Marking."""

    def __init__(
        self,
        center_of_segment: Point,
        direction_of_segment: Point,
        width: float,
        height: float,
    ) -> None:
        super().__init__(center_of_segment, direction_of_segment, width, height)
        self.borders = [self.polygon.segments[2]]
        self.type = "yield"

    def draw(self, painter: QPainter) -> None:
        """Draw the yield marking using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        for border in self.borders:
            border.draw(painter, 4, color=QColor(255, 255, 255))
        painter.save()
        painter.translate(
            self.center_of_segment.x,
            self.center_of_segment.y,
        )
        painter.rotate(degrees(self.direction_of_segment.angle()) - 90)
        painter.scale(1, 3)
        font = painter.font()
        font.setPixelSize(20)
        painter.setFont(font)
        painter.drawText(
            -round(self.width / 2),
            -round(self.height / 2),
            round(self.width),
            round(self.height),
            Qt.AlignmentFlag.AlignCenter,
            "YIELD",
        )
        painter.restore()
