"""This module contains the Marking class."""

from PyQt6.QtGui import QPainter
from src.primitives.point import Point
from src.primitives.segment import Segment
from src.primitives.envelope import Envelope


class Marking:
    """Marking is an abstract class for different markings."""

    def __init__(
        self,
        center_of_segment: Point,
        direction_of_segment: Point,
        width: float,
        height: float,
    ) -> None:
        self.center_of_segment = center_of_segment
        self.direction_of_segment = direction_of_segment
        self.width = width
        self.height = height
        self.support = Segment(
            Point(self.center_of_segment.x, self.center_of_segment.y).translate(
                self.direction_of_segment.angle(), height / 2
            ),
            Point(self.center_of_segment.x, self.center_of_segment.y).translate(
                self.direction_of_segment.angle(), -height / 2
            ),
        )
        self.polygon = Envelope(self.support, width, 0).polygon
        if len(self.polygon.segments) != 4:
            self.polygon.segments = [
                Segment(Point(), Point()),
                Segment(Point(), Point()),
                Segment(Point(), Point()),
                Segment(Point(), Point()),
            ]

    def draw(self, painter: QPainter) -> None:
        """Draw the graph editor using the given painter. This is an abstract method.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
