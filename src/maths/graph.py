from PyQt6.QtGui import QPainter
from src.primitives.segment import Segment
from src.primitives.circle import Circle
from src.primitives.point import Point


class Graph:
    def __init__(
        self, points: list | None = None, segments: list | None = None
    ) -> None:
        self.points = points
        self.segments = segments

    def load(self, data) -> None:
        self.points = []
        for point in data["points"]:
            self.points.append(Point(point["x"], point["y"]))
        self.segments = []
        for segment in data["segments"]:
            self.segments.append(
                Segment(
                    Point(segment["start"]["x"], segment["start"]["y"]),
                    Point(segment["end"]["x"], segment["end"]["y"]),
                )
            )

    def get_hash(self) -> None:
        return hash(self)

    def add_point(self, point: Point) -> None:
        if not self.contains_point(point):
            self.points.append(point)

    def contains_point(self, point: Point) -> bool:
        return point in self.points

    def add_segment(self, segment: Segment) -> None:
        if not self.contains_segment(segment):
            self.segments.append(segment)

    def contains_segment(self, segment: Segment) -> bool:
        return segment in self.segments

    def remove_point(self, point: Point) -> None:
        segments = self.segments_contains_point(point)
        for segment in segments:
            self.remove_segment(segment)
        self.points.remove(point)

    def remove_segment(self, segment: Segment) -> None:
        self.segments.remove(segment)

    def segments_contains_point(self, point: Point) -> list:
        segments = []
        for segment in self.segments:
            if segment.contains_point(point):
                segments.append(segment)
        return segments

    def dispose(self) -> None:
        self.points.clear()
        self.segments.clear()

    def draw(self, painter: QPainter, zoom: float) -> None:
        for segment in self.segments:
            segment.draw(painter, zoom * 3)
        for point in self.points:
            Circle(point.x, point.y, zoom * 15).draw(painter)
