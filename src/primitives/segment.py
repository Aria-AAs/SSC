"""This module contains the Segment class."""

from math import degrees, atan, sqrt, inf
from typing import Self
from PyQt6.QtCore import QLineF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from src.primitives.point import Point


class Segment:
    """Segment class represents a segment."""

    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def __eq__(self, other: Self) -> bool:
        return self.start == other.start and self.end == other.end

    def contains_point(self, point: Point) -> bool:
        """Check if the given point is a point of the segment.

        Args:
            point (Point): The point to check.

        Returns:
            bool: True if the point is a point of the segment otherwise False.
        """
        return point in (self.start, self.end)

    def length(self) -> float:
        """Calculate and return the length of the segment.

        Returns:
            float: The length of the segment.
        """
        return self.start.distance_to_point(self.end)

    def direction(self) -> Point:
        """Calculate and return a point with length one from the zero position of the logical
        coordinate system that represents the direction of the segment.

        Returns:
            Point: The point that represents the direction of the segment.
        """
        return (self.end - self.start).normalize()

    def midpoint(self) -> Point:
        """Find the midpoint of the segment.

        Returns:
            Point: The midpoint of the segment.
        """
        return self.start.midpoint(self.end)

    def distance_to_point(self, point: Point) -> float:
        """Calculate the minimum distance from this segment to the given point.

        Args:
            point (Point): The point to calculate the distance.

        Returns:
            float: The distance from the given point to the segment.
        """
        projected_point = self.project_point(point)
        if 0 < projected_point["offset"] < 1:
            return point.distance_to_point(projected_point["point"])
        distance_to_start = self.start.distance_to_point(point)
        distance_to_end = self.end.distance_to_point(point)
        return min(distance_to_start, distance_to_end)

    def project_point(self, point: Point) -> dict:
        """Project the given point on the segment.

        Args:
            point (Point): The point to project on the segment.

        Returns:
            dict: A dict contains the projected point and the offset of it from the segment.
        """
        a = point - self.start
        b = self.end - self.start
        if b.magnitude() == 0:
            return {"point": Point(), "offset": 0}
        normalize_b = b.normalize()
        scaler = a.dot_product(normalize_b)
        return {
            "point": self.start + normalize_b.scale(scaler),
            "offset": scaler / b.magnitude(),
        }

    def slope(self, axis: str = "x") -> float:
        """Find the slope of this segment.

        Returns:
            float: The slope of the segment.
        """
        if axis == "x":
            if self.end.x == self.start.x:
                return inf
            return (self.end.y - self.start.y) / (self.end.x - self.start.x)
        if axis == "y":
            if self.end.y == self.start.y:
                return inf
            return (self.end.x - self.start.x) / (self.end.y - self.start.y)

    def angle(self) -> float:
        """Calculate and return the angle of this segment from the x-axis (measured in degrees).

        Returns:
            float: The angle of the segment in radians.
        """
        if self.start.x < self.end.x:
            if self.start.y < self.end.y:
                angle = -degrees(atan(self.slope()))
            elif self.start.y > self.end.y:
                angle = -degrees(atan(self.slope()))
            else:
                angle = 0.0
        elif self.start.x > self.end.x:
            if self.start.y < self.end.y:
                angle = degrees(atan(self.slope("y"))) - 90
            elif self.start.y > self.end.y:
                angle = degrees(atan(self.slope("y"))) + 90
            else:
                angle = 180.0
        else:
            if self.start.y < self.end.y:
                angle = 270.0
            elif self.start.y > self.end.y:
                angle = 90.0
            else:
                print("Error: angle = None")
        if angle < 0:
            angle += 360
        return angle

    def make_parallel_with_offset(self, offset: float) -> Self:
        m = self.slope()
        if self.start.x > self.end.x:
            new_start = Point(
                self.start.x - offset * m / sqrt(1 + m**2),
                self.start.y + offset / sqrt(1 + m**2),
            )
            new_end = Point(
                self.end.x - offset * m / sqrt(1 + m**2),
                self.end.y + offset / sqrt(1 + m**2),
            )
            return Segment(new_start, new_end)
        if self.start.x < self.end.x:
            new_start = Point(
                self.start.x + offset * m / sqrt(1 + m**2),
                self.start.y - offset / sqrt(1 + m**2),
            )
            new_end = Point(
                self.end.x + offset * m / sqrt(1 + m**2),
                self.end.y - offset / sqrt(1 + m**2),
            )
            return Segment(new_start, new_end)
        if self.start.y > self.end.y:
            new_start = Point(
                self.start.x - offset,
                self.start.y,
            )
            new_end = Point(
                self.end.x - offset,
                self.end.y,
            )
        elif self.start.y < self.end.y:
            new_start = Point(
                self.start.x + offset,
                self.start.y,
            )
            new_end = Point(
                self.end.x + offset,
                self.end.y,
            )
        return Segment(new_start, new_end)

    def is_parallel(self, other: Self) -> bool:
        """Check if this segment is parallel with the other given segment.

        Args:
            other (Self): Another segment to check is parallel with this segment or not.

        Returns:
            bool: True if two segments are parallel and false otherwise.
        """
        return self.slope() == other.slope()

    def middle_segment(self, other: Self) -> Self:
        """Find a middle segment between two existing parallel segments.

        Args:
            other (Self): The other segment is given to find a middle segment between it and
            this segment.

        Returns:
            Self: The middle segment. None if these two segments are not parallel.
        """
        if self.is_parallel(other):
            if self.start.midpoint(other.start) != self.end.midpoint(other.end):
                return Segment(
                    self.start.midpoint(other.start), self.end.midpoint(other.end)
                )
            return Segment(
                self.start.midpoint(other.end), self.end.midpoint(other.start)
            )

    def draw(
        self,
        painter: QPainter,
        width: float = 0,
        cap_style: Qt.PenCapStyle = Qt.PenCapStyle.RoundCap,
        dash_style: list | None = None,
        color: QColor = QColor(0, 0, 0),
        style: Qt.PenStyle = Qt.PenStyle.SolidLine,
    ) -> None:
        """Draw the segment using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            width (float, optional): The width of the line to paint. Defaults to 0.
            cap_style (Qt.PenCapStyle, optional): The style of caps of the segment to paint.
            Defaults to Qt.PenCapStyle.RoundCap.
            dash_style (list | None, optional): The style of the dash pattern.
            None or empty list to draw a solid segment. Defaults to None.
            color (QColor, optional): The color to paint the point. Defaults to QColor(0, 0, 0).
            style (Qt.PenStyle, optional): The style of the segment itself to paint.
            Defaults to Qt.PenStyle.SolidLine.
        """
        line = QLineF(self.start.x, self.start.y, self.end.x, self.end.y)
        pen = QPen(color, width, style)
        pen.setCapStyle(cap_style)
        if dash_style:
            pen.setDashPattern(dash_style)
        painter.setPen(pen)
        painter.drawLine(line)
