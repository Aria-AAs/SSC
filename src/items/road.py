"""This module contains the Road class."""

from PyQt6.QtGui import QPainter
from src.primitives.segment import Segment
from src.primitives.envelope import Envelope
from src.items.lane import Lane
from src.maths.utils import lerp_2d


class Road:
    """Road class represents a road."""

    def __init__(
        self,
        segment: Segment,
        number_of_lanes_in_left_side: int,
        number_of_lanes_in_right_side: int,
        name: str = "",
        lane_width: int = 50,
        priority: int = 0,
        elevation: int = 0,
        is_oneway: bool = False,
        lefthand_rule: bool = False,
        is_start_connected: bool = False,
        is_end_connected: bool = False,
    ) -> None:
        self.name = name
        self.number_of_lanes = (
            number_of_lanes_in_left_side + number_of_lanes_in_right_side
        )
        self.lane_width = lane_width
        self.width = self.lane_width * self.number_of_lanes
        self.segment = segment
        road_roundness = self.width // 10
        self.envelope = Envelope(self.segment, self.width, road_roundness)
        self.polygon = self.envelope.polygon
        self.number_of_lanes_in_right_side = number_of_lanes_in_right_side
        self.number_of_lanes_in_left_side = number_of_lanes_in_left_side
        self.priority = priority
        self.elevation = elevation
        self.is_oneway = is_oneway
        self.is_start_connected = is_start_connected
        self.is_end_connected = is_end_connected
        self.lefthand_rule = lefthand_rule
        self.lanes = []
        segments = Envelope(self.segment, self.width, 0).polygon.segments
        if len(segments) != 4:
            return
        min_t = 1 / self.number_of_lanes
        for i in range(self.number_of_lanes):
            t = (i + 1) / self.number_of_lanes - min_t / 2
            is_most_left_lane = False
            is_most_right_lane = False
            if self.is_oneway:
                if i == self.number_of_lanes - 1:
                    is_most_right_lane = True
            else:
                if i in (0, self.number_of_lanes - 1):
                    is_most_right_lane = True
            if i in (self.number_of_lanes_in_left_side,):
                is_most_left_lane = True
            if i < self.number_of_lanes_in_left_side:
                segment = Segment(
                    lerp_2d(segments[1].end, segments[3].start, t),
                    lerp_2d(segments[1].start, segments[3].end, t),
                )
            else:
                segment = Segment(
                    lerp_2d(segments[1].start, segments[3].end, t),
                    lerp_2d(segments[1].end, segments[3].start, t),
                )
            self.lanes.append(
                Lane(
                    segment,
                    is_most_left_lane,
                    is_most_right_lane,
                    50,
                    0,
                    self.lane_width,
                )
            )

    def draw(self, painter: QPainter) -> None:
        """Draw the intersection area using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        for lane in self.lanes:
            lane.draw(painter)
