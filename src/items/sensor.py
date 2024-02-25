from math import sin, cos, radians
from PyQt6.QtCore import Qt, QLineF
from PyQt6.QtGui import QPainter, QPen, QColor
from src.primitives.point import Point
from src.maths.utils import find_intersection


class Sensor:
    def __init__(self, length: float) -> None:
        self.length = length
        self.angle = 0
        self.start = None
        self.end = None
        self.intersect = None
        self.offset = None

    def read(self) -> float | None:
        return self.offset

    def update(self, road_borders, angle, start_position):
        self.angle = angle
        self.start = start_position
        self.end = Point(
            self.start.x + sin(radians(angle)) * self.length,
            self.start.y - cos(radians(angle)) * self.length,
        )
        touches = []
        for border in road_borders:
            touch = find_intersection(
                self.start, self.end, border.points[0], border.points[1]
            )
            if touch:
                touches.append(touch)
        if touches:
            offsets = []
            for touch in touches:
                offsets.append(touch["offset"])
            self.offset = min(offsets)
            for touch in touches:
                if touch["offset"] == self.offset:
                    self.intersect = Point(touch["x"], touch["y"])
        else:
            self.intersect = self.end
            self.offset = None

    def draw(self, painter: QPainter):
        if self.start:
            painter.setPen(QPen(QColor(0, 0, 0), 2, Qt.PenStyle.SolidLine))
            line = QLineF(self.intersect.x, self.intersect.y, self.end.x, self.end.y)
            painter.drawLine(line)
            painter.setPen(QPen(QColor(255, 255, 0), 2, Qt.PenStyle.SolidLine))
            line = QLineF(
                self.start.x, self.start.y, self.intersect.x, self.intersect.y
            )
            painter.drawLine(line)
