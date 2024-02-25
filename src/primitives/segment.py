from typing import Self
from PyQt6.QtCore import QLineF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from src.primitives.point import Point


class Segment:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def __eq__(self, __value: Self) -> bool:
        return self.contains_point(__value.start) and self.contains_point(__value.end)

    def contains_point(self, point: Point) -> bool:
        return point in (self.start, self.end)

    def length(self) -> None:
        return self.start.distance_to_point(self.end)

    def direction_vector(self):
        return (self.end - self.start).normalize()

    def midpoint(self) -> Point:
        return self.start.midpoint(self.end)

    def distance_to_point(self, point: Point) -> float:
        projected_point = self.project_point(point)
        if 0 < projected_point["offset"] < 1:
            return point.distance_to_point(projected_point["point"])
        distance_to_start = self.start.distance_to_point(point)
        distance_to_end = self.end.distance_to_point(point)
        return min(distance_to_start, distance_to_end)

    def project_point(self, point: Point) -> dict:
        a = point - self.start
        b = self.end - point
        normalize_b = b.normalize()
        scaler = a.dot_product(normalize_b)
        return {
            "point": self.start + normalize_b.scale(scaler),
            "offset": scaler / b.magnitude(),
        }

    def draw(
        self,
        painter: QPainter,
        width: float = 0,
        cap_style: Qt.PenCapStyle = Qt.PenCapStyle.RoundCap,
        dash_style: list | None = None,
        color: QColor = QColor(0, 0, 0),
        style: Qt.PenStyle = Qt.PenStyle.SolidLine,
    ) -> None:
        line = QLineF(self.start.x, self.start.y, self.end.x, self.end.y)
        pen = QPen(color, width, style)
        pen.setCapStyle(cap_style)
        if dash_style:
            pen.setDashPattern(dash_style)
        painter.setPen(pen)
        painter.drawLine(line)
