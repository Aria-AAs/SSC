from math import sqrt, sin, cos, atan, atan2, pi
from typing import Self
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor


class Point:
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
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def midpoint(self, other: Self) -> Self:
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)

    def dot_product(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y

    def scale(self, scaler: float) -> Self:
        return Point(self.x * scaler, self.y * scaler)

    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def normalize(self) -> Self:
        return self.scale(1 / self.magnitude())

    def perpendicular(self) -> Self:
        return Point(-self.y, self.x)

    def angle(self) -> float:
        return atan2(self.y, self.x)

    def translate(self, angle, offset) -> Self:
        return Point(
            self.x + cos(angle) * offset,
            self.y + sin(angle) * offset,
        )

    def get_3d_point(self, view_point: Self, height: float) -> Self:
        direction = (self - view_point).normalize()
        distance = self.distance_to_point(view_point)
        scaler = atan(distance / 300) / (pi / 2)
        return self + direction.scale(height * scaler)

    def draw(
        self,
        painter: QPainter,
        thickness: int = 1,
        color: QColor = QColor(0, 0, 0),
        style: Qt.PenStyle = Qt.PenStyle.SolidLine,
    ) -> None:
        point = QPointF(self.x, self.y)
        painter.setPen(QPen(color, thickness, style))
        painter.drawPoint(point)
