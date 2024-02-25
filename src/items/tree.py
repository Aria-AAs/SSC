from math import cos, pi
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.polygon import Polygon
from src.maths.utils import lerp, lerp_2d


class Tree:
    def __init__(self, center: Point, size: float, height: float = 200) -> None:
        self.center = center
        self.size = size
        self.height = height
        self.level_count = 15
        self.base = self.generate_level(self.center, self.size)

    def generate_level(self, point: Point, size: float) -> Polygon:
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
        top = self.center.get_3d_point(view_point, self.height)
        for level in range(self.level_count):
            level_height = level / (self.level_count - 1)
            point = lerp_2d(self.center, top, level_height)
            color = QColor(30, round(lerp(50, 200, level_height)), 70)
            size = lerp(self.size, 40, level_height)
            level_polygon = self.generate_level(point, size)
            level_polygon.draw(painter, color, outline_color=QColor(0, 0, 0))
