from typing import Self
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.polygon import Polygon


class Building:
    def __init__(self, base: Polygon, height: float = 200) -> None:
        self.base = base
        self.height = height

    def load(self, data) -> Self:
        return Building(Polygon([]).load(data.base), data.height)

    def preparing_to_draw(self, view_point: Point) -> tuple:
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
        sides, ceiling, roofs = self.preparing_to_draw(view_point)
        self.base.draw(
            painter,
            color=QColor(255, 255, 255),
            outline_color=QColor(0, 0, 0, 20),
            width=20,
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
            width=6,
        )
        for roof in roofs:
            roof.draw(
                painter,
                color=QColor(221, 68, 68),
                outline_color=QColor(204, 68, 68),
                width=8,
                join_style=Qt.PenJoinStyle.RoundJoin,
            )
