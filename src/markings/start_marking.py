"""This module contains the StartMarking class."""

from math import degrees
from pathlib2 import Path
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPixmap
from src.primitives.point import Point
from src.markings.marking import Marking


class StartMarking(Marking):
    """StartMarking class represents a start marking. Inherited from Marking."""

    def __init__(
        self,
        center_of_segment: Point,
        direction_of_segment: Point,
        width: float,
        height: float,
    ) -> None:
        super().__init__(center_of_segment, direction_of_segment, width, height)
        image = QPixmap(
            str(Path(Path(__file__).parent.parent.parent, "asset/images/car.png"))
        )
        self.image = image.scaledToWidth(
            round(self.width), Qt.TransformationMode.SmoothTransformation
        )
        self.type = "start"

    def draw(self, painter: QPainter) -> None:
        """Draw the start marking using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        rect = QRect(-15, -25, 30, 50)
        painter.save()
        painter.translate(self.center_of_segment.x, self.center_of_segment.y)
        painter.rotate(degrees(self.direction_of_segment.angle()) - 90)
        painter.drawPixmap(rect, self.image)
        painter.restore()
