"""This module contains the Building class."""

from typing import Self
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.polygon import Polygon


class Building:
    """Building class represents a building."""

    def __init__(self, base: Polygon, height: float = 200) -> None:
        self.base = base
        self.height = height

    def load(self, data: dict) -> Self:
        """A method that extracts information from data.

        Args:
            data (dict): The given data.

        Returns:
            Self: The building that extracted from the data.
        """
        return Building(Polygon([]).load(data.base), data.height)

    def _preparing_to_draw(self, view_point: Point) -> tuple:
        """preparing to draw the building. this method calculates and generates the sides, ceiling,
        and roof of the building.

        Args:
            view_point (Point): The center of the viewport.

        Returns:
            tuple: A tuple includes a list of polygons for sides, a polygon for the ceiling, and
            a list of polygons for the roof.
        """
        top_points = []
        for point in self.base.points:
            top_points.append(point.get_3d_point(view_point, self.height * 0.6))
        ceiling = Polygon(top_points)
        sides = []
        i = 0
        while i < len(self.base.points):
            next_i = (i + 1) % len(self.base.points)
            sides.append(
                Polygon(
                    [
                        self.base.points[i],
                        self.base.points[next_i],
                        top_points[next_i],
                        top_points[i],
                    ]
                )
            )
            i += 1
        sides.sort(reverse=True, key=lambda side: side.distance_to_point(view_point))
        base_midpoints = [
            self.base.points[0].midpoint(self.base.points[1]),
            self.base.points[2].midpoint(self.base.points[3]),
        ]
        top_midpoints = []
        for point in base_midpoints:
            top_midpoints.append(point.get_3d_point(view_point, self.height))
        roof_polygons = [
            Polygon(
                [
                    ceiling.points[0],
                    ceiling.points[3],
                    top_midpoints[1],
                    top_midpoints[0],
                ]
            ),
            Polygon(
                [
                    ceiling.points[2],
                    ceiling.points[1],
                    top_midpoints[0],
                    top_midpoints[1],
                ]
            ),
        ]
        roof_polygons.sort(
            reverse=True,
            key=lambda roof_polygon: roof_polygon.distance_to_point(view_point),
        )
        return sides, ceiling, roof_polygons

    def draw(self, painter: QPainter, view_point: Point) -> None:
        """Draw the building using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            view_point (Point): The center of the viewport.
        """
        sides, ceiling, roofs = self._preparing_to_draw(view_point)
        self.base.draw(
            painter,
            color=QColor(255, 255, 255),
            outline_color=QColor(0, 0, 0, 20),
            outline_width=20,
        )
        for side in sides:
            side.draw(
                painter,
                color=QColor(255, 255, 255),
                outline_color=QColor(170, 170, 170),
            )
        ceiling.draw(
            painter,
            color=QColor(255, 255, 255),
            outline_color=QColor(255, 255, 255),
            outline_width=6,
        )
        for roof in roofs:
            roof.draw(
                painter,
                color=QColor(210, 60, 60),
                outline_color=QColor(190, 50, 50),
                outline_width=8,
                join_style=Qt.PenJoinStyle.RoundJoin,
            )
