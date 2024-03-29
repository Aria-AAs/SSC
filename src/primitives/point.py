"""This module contains the Point class."""

from math import sqrt, sin, cos, atan, atan2, pi
from typing import Self
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QPen, QColor


class Point:
    """Point class represents a point."""

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Point(self.x - other.x, self.y - other.y)

    def distance_to_point(self, other: Self) -> float:
        """Calculate the distance from itself to the other point.

        Args:
            other (Self): The point to calculate the distance to.

        Returns:
            float: The distance from this point to the given point.
        """
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def midpoint(self, other: Self) -> Self:
        """Return a point that is in the middle of this point and the other given point.

        Args:
            other (Self): The point to return the middle point of it and this point.

        Returns:
            Self: The point that is in the middle of this point and the given point.
        """
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)

    def dot_product(self, other: Self) -> float:
        """Calculate the dot product of the given point and this point.
        The points are considered vectors from the zero position of
        the logical coordinate system (top-left corner).

        Args:
            other (Self): The point to calculate the dot product of it and this point.

        Returns:
            float: The dot product result of the given point and this point.
        """
        return self.x * other.x + self.y * other.y

    def scale(self, scaler: float) -> Self:
        """Scale this point with the amount of the given scaler.

        Args:
            scaler (float): The amount of scaler to scale this point.

        Returns:
            Self: A point that scaled from this point with the given scaler.
        """
        return Point(self.x * scaler, self.y * scaler)

    def magnitude(self) -> float:
        """Calculate the magnitude of the point.
        The point is considered vector from the zero position of
        the logical coordinate system (top-left corner).

        Returns:
            float: The magnitude of the point.
        """
        return sqrt(self.x**2 + self.y**2)

    def normalize(self) -> Self:
        """Calculate and return a normalized point from this point.
        The point is considered vector from the zero position of
        the logical coordinate system (top-left corner).

        Returns:
            Self: A point that maintains the direction of this point but its Length is one.
        """
        return self.scale(1 / self.magnitude())

    def mirror_about_x_axis(self) -> Self:
        """Mirror this point about the x-axis and return it as a new point.

        Returns:
            Self: The mirrored point.
        """
        return Point(self.y, -self.x)

    def mirror_about_y_axis(self) -> Self:
        """Mirror this point about the y-axis and return it as a new point.

        Returns:
            Self: The mirrored point.
        """
        return Point(-self.y, self.x)

    def angle(self) -> float:
        """Calculate and return the angle of this point from the x-axis (measured in radians).
        The point is considered vector from the zero position of
        the logical coordinate system (top-left corner).

        Returns:
            float: The angle of the point in radians.
        """
        return atan2(self.y, self.x)

    def translate(self, angle: float, offset: float) -> Self:
        """Create a new point in a new location based on this point and the given angle and
        offset.

        Args:
            angle (float): The angle from the x-axis (measured in radians) to translate.
            offset (float): The offset to translate.

        Returns:
            Self: A point that translated with this point and the given angle and offset.
        """
        return Point(
            self.x + cos(angle) * offset,
            self.y + sin(angle) * offset,
        )

    def get_3d_point(self, view_point: Self, height: float) -> Self:
        """Generate a fake 3D point based on where we are looking at and a given height.

        Args:
            view_point (Self): The point that we are looking at.
            height (float): The height of the 3D point.

        Returns:
            Self: The 3D point
        """
        direction = (self - view_point).normalize()
        distance = self.distance_to_point(view_point)
        scaler = atan(distance / 300) / (pi / 2)
        return self + direction.scale(height * scaler)

    def draw(
        self,
        painter: QPainter,
        thickness: int = 1,
        color: QColor = QColor(0, 0, 0),
    ) -> None:
        """Draw the point using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            thickness (int, optional): the size of the point. Defaults to 1.
            color (QColor, optional): the color to paint the point. Defaults to QColor(0, 0, 0).
        """
        point = QPointF(self.x, self.y)
        pen = QPen(color)
        pen.setWidth(thickness)
        painter.setPen(pen)
        painter.drawPoint(point)
