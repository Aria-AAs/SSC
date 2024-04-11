"""This module contains the Envelope class."""

from typing import Self
from math import pi
from PyQt6.QtGui import QPainter
from src.primitives.point import Point
from src.primitives.segment import Segment
from src.primitives.polygon import Polygon


class Envelope:
    """Envelope class represents an envelope."""

    def __init__(
        self,
        segment: Segment,
        width: float = 2,
        roundness: int = 1,
        offset: Point = Point(),
    ) -> None:
        point_1 = segment.start + offset
        point_2 = segment.end + offset
        radius = width / 2
        alpha = (point_1 - point_2).angle()
        alpha_cw = alpha + pi / 2
        alpha_ccw = alpha - pi / 2
        points = []
        step = pi / max(1, roundness)
        i = alpha_ccw
        while i <= alpha_cw:
            points.append(point_1.translate(i, radius))
            i += step
        i = alpha_ccw
        while i <= alpha_cw:
            points.append(point_2.translate(pi + i, radius))
            i += step
        self.polygon = Polygon(points)

    def __str__(self) -> str:
        return f"An Envelope with {self.polygon.__str__()}"

    def load(self, data: dict) -> Self:
        """A method that extracts information from data.

        Args:
            data (dict): The given data.
        """
        envelope = Envelope(Segment(Point(), Point()))
        envelope.polygon = Polygon([]).load(data.polygon)
        return envelope

    def draw(self, painter: QPainter, *args, **kwargs):
        """Draw the envelope using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        self.polygon.draw(painter, *args, **kwargs)
