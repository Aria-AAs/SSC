from typing import Self
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF
from src.primitives.segment import Segment
from src.primitives.point import Point
from src.maths.utils import find_intersection


class Polygon:
    def __init__(self, points: list) -> None:
        self.points = points
        self.segments = []
        for i, _ in enumerate(self.points):
            self.segments.append(
                Segment(self.points[i], self.points[(i + 1) % len(self.points)])
            )

    def __str__(self) -> str:
        string = "A Polygon with\npoints{\n"
        for point in self.points:
            string += f"\t{point.__str__()}\n"
        string += "}\nsegments{"
        for segment in self.segments:
            string += f"\t{segment.__str__()}\n"
        string += "}"
        return string

    def load(self, data) -> Self:
        return Polygon(data.points)

    def union(self, polygons: list) -> list:
        i = 0
        while i < len(polygons):
            j = i + 1
            while j < len(polygons):
                polygons[i].break_segments(polygons[j])
                j += 1
            i += 1
        kept_segments = []
        i = 0
        while i < len(polygons):
            for segment in polygons[i].segments:
                keep = True
                j = 0
                while j < len(polygons):
                    if i != j:
                        if polygons[j].contains_segment(segment):
                            keep = False
                            break
                    j += 1
                if keep:
                    kept_segments.append(segment)
            i += 1
        return kept_segments

    def break_segments(self, other: Self) -> None:
        segments_1 = self.segments
        segments_2 = other.segments
        for i, _ in enumerate(segments_1):
            for j, _ in enumerate(segments_2):
                intersection = find_intersection(
                    segments_1[i].start,
                    segments_1[i].end,
                    segments_2[j].start,
                    segments_2[j].end,
                )
                if (
                    intersection
                    and intersection["offset"] != 0
                    and intersection["offset"] != 1
                ):
                    point = Point(intersection["x"], intersection["y"])
                    temporary = segments_1[i].end
                    segments_1[i].end = point
                    segments_1.insert(i + 1, Segment(point, temporary))
                    temporary = segments_2[j].end
                    segments_2[j].end = point
                    segments_2.insert(j + 1, Segment(point, temporary))

    def contains_segment(self, segment: Segment) -> bool:
        return self.contains_point(segment.midpoint())

    def contains_point(self, point: Point) -> bool:
        outer_point = Point(-1000, -1000)
        intersection_counter = 0
        for segment in self.segments:
            if find_intersection(outer_point, point, segment.start, segment.end):
                intersection_counter += 1
        return intersection_counter % 2 == 1

    def distance_to_point(self, point: Point) -> float:
        distances = []
        for segment in self.segments:
            distances.append(segment.distance_to_point(point))
        return min(distances)

    def distance_to_polygon(self, other: Self) -> float:
        distances = []
        for point in self.points:
            distances.append(other.distance_to_point(point))
        return min(distances)

    def intersect_with_polygon(self, other: Self) -> bool:
        for segment_1 in self.segments:
            for segment_2 in other.segments:
                if find_intersection(
                    segment_1.start, segment_1.end, segment_2.start, segment_2.end
                ):
                    return True
        return False

    def draw(
        self,
        painter: QPainter,
        color: QColor = QColor(0, 0, 0),
        width: float = -1,
        style: Qt.BrushStyle = Qt.BrushStyle.SolidPattern,
        join_style: Qt.PenJoinStyle = Qt.PenJoinStyle.MiterJoin,
        cap_style: Qt.PenCapStyle = Qt.PenCapStyle.RoundCap,
        dash_style: list | None = None,
        outline_color: QColor = QColor(0, 0, 0),
        outline_style: Qt.PenStyle = Qt.PenStyle.SolidLine,
    ) -> None:
        points = []
        for point in self.points:
            points.append(QPointF(point.x, point.y))
        polygon = QPolygonF(points)
        pen = QPen(outline_color, width, outline_style)
        pen.setCapStyle(cap_style)
        pen.setJoinStyle(join_style)
        if dash_style:
            pen.setDashPattern(dash_style)
        painter.setPen(pen)
        painter.setBrush(QBrush(color, style))
        painter.drawPolygon(polygon)
