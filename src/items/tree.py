"""This module contains the Tree class."""

from math import cos, pi
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.polygon import Polygon
from src.maths.utils import lerp, lerp_2d


class Tree:
    """Tree class represents a tree."""

    def __init__(self, center: Point, size: float, height: float = 200) -> None:
        self.center = center
        self.size = size
        self.height = height
        self.level_count = 15
        self.base = self._generate_level(self.center, self.size)

    def _generate_level(self, point: Point, size: float) -> Polygon:
        """Generate a polygon based on its location and size.

        Args:
            point (Point): The point to generate a polygon that is considered as the center of the
            polygon.
            size (float): The size is considered as the diameter of an imaginary circle that the
            polygon fits into it.

        Returns:
            Polygon: The generated polygon.
        """
        points = []
        radius = size / 2
        a = 0
        while a < pi * 2:
            kind_of_random = cos(((a + self.center.x) * size) % 17) ** 2
            noisy_radius = radius * lerp(0.5, 1, kind_of_random)
            points.append(point.translate(a, noisy_radius))
            a += pi / 16
        return Polygon(points)

    def draw(self, painter: QPainter, view_point: Point) -> None:
        """Draw the tree using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            view_point (Point): The center of the viewport.
        """
        top = self.center.get_3d_point(view_point, self.height)
        for level in range(self.level_count):
            level_height = level / (self.level_count - 1)
            point = lerp_2d(self.center, top, level_height)
            color = QColor(30, round(lerp(50, 200, level_height)), 70)
            size = lerp(self.size, 40, level_height)
            level_polygon = self._generate_level(point, size)
            level_polygon.draw(painter, color, outline_color=QColor(0, 0, 0))
