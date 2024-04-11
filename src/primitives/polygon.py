"""This module contains the Polygon class."""

from typing import Self
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF
from src.primitives.segment import Segment
from src.primitives.point import Point
from src.maths.utils import find_intersect


class Polygon:
    """Polygon class represents a polygon."""

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

    def load(self, data: dict) -> Self:
        """A method that extracts information from data.

        Args:
            data (dict): The given data.

        Returns:
            Self: The polygon that extracted from the data.
        """
        return Polygon(data.points)

    @staticmethod
    def union(polygons: list) -> list:
        """Find all segments in a list of polygons. If a segment appears in two or more
        polygons, only one of them is kept.

        Args:
            polygons (list): The list of polygons to search for unique segments

        Returns:
            list: A list of all unique segments
        """
        for i in range(len(polygons) - 1):
            for j in range(i, len(polygons)):
                polygons[i].break_segments(polygons[j])
        kept_segments = []
        for i, polygon_i in enumerate(polygons):
            for segment in polygon_i.segments:
                keep = True
                for j, polygon_j in enumerate(polygons):
                    if i != j:
                        if polygon_j.contains_segment(segment):
                            keep = False
                            break
                if keep:
                    kept_segments.append(segment)
        return kept_segments

    def break_segments(self, other: Self) -> None:
        """this method breaks down segments of this polygon and the other given polygon
        from intersection points.

        Args:
            other (Self): The other polygon to break down segments.
        """
        segments_1 = self.segments
        segments_2 = other.segments
        for i, _ in enumerate(segments_1):
            for j, _ in enumerate(segments_2):
                intersection = find_intersect(
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
        """Check if the given segment is inside the polygon.

        Args:
            segment (Segment): The segment to check.

        Returns:
            bool: True if the segment is inside the polygon otherwise False.
        """
        return self.contains_point(segment.midpoint())

    def contains_point(self, point: Point, threshold: float = 0.01) -> bool:
        """Check if the given point is inside the polygon.

        Args:
            point (Point): The point to check.

        Returns:
            bool: True if the point is inside the polygon otherwise False.
        """
        px = point.x
        py = point.y
        intersections = 0
        for segment in self.segments:
            x1 = segment.start.x
            y1 = segment.start.y
            x2 = segment.end.x
            y2 = segment.end.y
            if (py < y1) != (py < y2):
                if px - threshold < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
                    intersections += 1
        if intersections % 2 == 1:
            return True
        return False

    def distance_to_point(self, point: Point) -> float:
        """Calculate the minimum distance from this polygon to the given point.

        Args:
            point (Point): The point to calculate the distance.

        Returns:
            float: The distance from the given point to the polygon.
        """
        distances = []
        for segment in self.segments:
            distances.append(segment.distance_to_point(point))
        return min(distances)

    def distance_to_polygon(self, other: Self) -> float:
        """Calculate the minimum distance from this polygon to the given polygon.

        Args:
            other (Self): The polygon to calculate the distance.

        Returns:
            float: The distance from the given polygon to this polygon.
        """
        distances = []
        for point in self.points:
            distances.append(other.distance_to_point(point))
        return min(distances)

    def intersect_with_polygon(self, other: Self) -> bool:
        """Check if the given polygon has an intersection with this polygon.

        Args:
            other (Self): The polygon to Check for an intersection.

        Returns:
            bool: True if there is at least one intersection between two polygons otherwise False.
        """
        for segment_1 in self.segments:
            for segment_2 in other.segments:
                if find_intersect(
                    segment_1.start, segment_1.end, segment_2.start, segment_2.end
                ):
                    return True
        return False

    def draw(
        self,
        painter: QPainter,
        color: QColor = QColor(0, 0, 0),
        style: Qt.BrushStyle = Qt.BrushStyle.SolidPattern,
        join_style: Qt.PenJoinStyle = Qt.PenJoinStyle.MiterJoin,
        cap_style: Qt.PenCapStyle = Qt.PenCapStyle.RoundCap,
        dash_style: list | None = None,
        outline_width: float = -1,
        outline_color: QColor = QColor(0, 0, 0),
        outline_style: Qt.PenStyle = Qt.PenStyle.SolidLine,
    ) -> None:
        """Draw the polygon using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            color (QColor, optional): The color to paint the point. Defaults to QColor(0, 0, 0).
            style (Qt.BrushStyle, optional): The style of fill inside of the polygon.
            Defaults to Qt.BrushStyle.SolidPattern.
            join_style (Qt.PenJoinStyle, optional): The style of joining the segments of the
            polygon. Defaults to Qt.PenJoinStyle.MiterJoin.
            cap_style (Qt.PenCapStyle, optional): The style of the cap of each segment of the
            polygon. Defaults to Qt.PenCapStyle.RoundCap.
            dash_style (list | None, optional): The style of the dash pattern. Defaults to None.
            outline_width (float, optional): The width of the outer lines of the polygon to paint.
            Defaults to -1.
            outline_color (QColor, optional): The color of the outer lines of the polygon to paint.
            Defaults to QColor(0, 0, 0).
            outline_style (Qt.PenStyle, optional): The style of the outer lines of the polygon to
            paint. Defaults to Qt.PenStyle.SolidLine.
        """
        points = []
        for point in self.points:
            points.append(QPointF(point.x, point.y))
        polygon = QPolygonF(points)
        pen = QPen(outline_color, outline_width, outline_style)
        pen.setCapStyle(cap_style)
        pen.setJoinStyle(join_style)
        if dash_style:
            pen.setDashPattern(dash_style)
        painter.setPen(pen)
        painter.setBrush(QBrush(color, style))
        painter.drawPolygon(polygon)
