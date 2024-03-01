"""This module contains the Graph class."""

from PyQt6.QtGui import QPainter
from src.primitives.segment import Segment
from src.primitives.circle import Circle
from src.primitives.point import Point


class Graph:
    """Graph class represents a graph."""

    def __init__(
        self, points: list | None = None, segments: list | None = None
    ) -> None:
        self.points = points
        self.segments = segments

    def load(self, data: dict) -> None:
        """A method that extracts information from data.

        Args:
            data (dict): The given data.
        """
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

    def get_hash(self) -> int:
        """Make and return the hash of the current graph object.

        Returns:
            int: The hash of the current object.
        """
        return hash(self)

    def add_point(self, point: Point) -> None:
        """Add the given point object to the current graph.

        Args:
            point (Point): The point to add to the current graph.
        """
        if not self.contains_point(point):
            self.points.append(point)

    def contains_point(self, point: Point) -> bool:
        """Check if the given point is a point of the graph.

        Args:
            point (Point): The point to check.

        Returns:
            bool: True if the point is a point of the graph otherwise False.
        """
        return point in self.points

    def add_segment(self, segment: Segment) -> None:
        """Add the given segment object to the current graph.

        Args:
            segment (Segment): The segment to add to the current graph.
        """
        if not self.contains_segment(segment):
            self.segments.append(segment)

    def contains_segment(self, segment: Segment) -> bool:
        """Check if the given segment is a segment of the graph.

        Args:
            segment (Segment): The segment to check.

        Returns:
            bool: True if the segment is a segment of the graph otherwise False.
        """
        return segment in self.segments

    def remove_point(self, point: Point) -> None:
        """Remove the given point and all the segments that contain that point from the graph.

        Args:
            point (Point): The point to remove.
        """
        segments = self.segments_contain_point(point)
        for segment in segments:
            self.remove_segment(segment)
        self.points.remove(point)

    def remove_segment(self, segment: Segment) -> None:
        """Remove the given segment from the graph.

        Args:
            segment (Segment): The segment to remove.
        """
        self.segments.remove(segment)

    def segments_contain_point(self, point: Point) -> list[Segment]:
        """Find all the segments that contain the given point.

        Args:
            point (Point): The point to find all segments that contain it.

        Returns:
            list[Segment]: A list of all segments that contain the given point
        """
        segments = []
        for segment in self.segments:
            if segment.contains_point(point):
                segments.append(segment)
        return segments

    def clear(self) -> None:
        """Clear the graph from points and segments."""
        self.points.clear()
        self.segments.clear()

    def draw(self, painter: QPainter, zoom: float) -> None:
        """Draw the graph using the given painter.
        It also changes the drawing size based on the given zoom.

        Args:
            painter (QPainter): The painter is used for drawing.
            zoom (float): The amount zoom.
        """
        for segment in self.segments:
            segment.draw(painter, zoom * 3)
        for point in self.points:
            Circle(point.x, point.y, zoom * 15).draw(painter)
