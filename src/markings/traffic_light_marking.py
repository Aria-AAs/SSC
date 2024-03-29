"""This module contains the TrafficLightMarking class."""

from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.circle import Circle
from src.primitives.segment import Segment
from src.markings.marking import Marking
from src.maths.utils import lerp_2d


class TrafficLightMarking(Marking):
    """TrafficLightMarking class represents a traffic light marking. Inherited from Marking."""

    def __init__(
        self,
        center_of_segment: Point,
        direction_of_segment: Point,
        width: float,
        height: float,
    ) -> None:
        super().__init__(center_of_segment, direction_of_segment, width, height)
        self.borders = [self.polygon.segments[0]]
        self.type = "traffic_light"
        self.state = "off"

    def draw(self, painter: QPainter) -> None:
        """Draw the traffic light using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        for border in self.borders:
            border.draw(painter, 4, color=QColor(255, 255, 255))
        perpendicular = self.direction_of_segment.mirror_about_y_axis()
        line = Segment(
            self.center_of_segment + perpendicular.scale(self.width / 2),
            self.center_of_segment + perpendicular.scale(-self.width / 2),
        )
        green = lerp_2d(line.start, line.end, 0.2)
        yellow = lerp_2d(line.start, line.end, 0.5)
        red = lerp_2d(line.start, line.end, 0.8)
        Segment(red, green).draw(painter, self.height)
        Circle(green.x, green.y, self.height * 0.4).draw(painter, QColor(0, 100, 0))
        Circle(yellow.x, yellow.y, self.height * 0.4).draw(painter, QColor(100, 100, 0))
        Circle(red.x, red.y, self.height * 0.4).draw(painter, QColor(100, 0, 0))
        if self.state == "green":
            Circle(green.x, green.y, self.height * 0.4).draw(painter, QColor(0, 255, 0))
        elif self.state == "yellow":
            Circle(yellow.x, yellow.y, self.height * 0.4).draw(
                painter, QColor(255, 255, 0)
            )
        elif self.state == "red":
            Circle(red.x, red.y, self.height * 0.4).draw(painter, QColor(255, 0, 0))
