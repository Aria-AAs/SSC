"""This module contains the Road class."""

from PyQt6.QtGui import QPainter, QColor
from src.primitives.segment import Segment
from src.primitives.polygon import Polygon
from src.primitives.envelope import Envelope
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
        segments = Envelope(self.segment, self.width, 0).polygon.segments
        self.outer_lines = []
        self.middle_dashed_lines = []
        self.middle_line = None
        if len(segments) == 4:
            self.outer_lines = [segments[1], segments[3]]
            if is_start_connected:
                self.outer_lines.append(segments[0])
            for i in range(self.number_of_lanes - 1):
                t = (i + 1) / self.number_of_lanes
                if t == number_of_lanes_in_right_side / self.number_of_lanes:
                    self.middle_line = Segment(
                        lerp_2d(self.outer_lines[0].start, self.outer_lines[1].end, t),
                        lerp_2d(self.outer_lines[0].end, self.outer_lines[1].start, t),
                    )
                else:
                    self.middle_dashed_lines.append(
                        Segment(
                            lerp_2d(
                                self.outer_lines[0].start, self.outer_lines[1].end, t
                            ),
                            lerp_2d(
                                self.outer_lines[0].end, self.outer_lines[1].start, t
                            ),
                        )
                    )
        polygon = Envelope(segment, self.width / 2, 0).polygon
        self.lane_guides = Polygon.union([polygon])
        if len(self.lane_guides) == 4:
            self.lane_guides = [self.lane_guides[1], self.lane_guides[3]]

    def draw(self, painter: QPainter) -> None:
        """Draw the intersection area using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        # self.envelope.draw(
        #     painter,
        #     color=QColor(51, 51, 51),
        #     outline_width=15,
        #     outline_color=QColor(51, 51, 51),
        # )
        # for segment in self.polygon.segments:
        #     segment.draw(painter, color=QColor(255, 255, 255), width=5)
        if self.middle_line:
            self.middle_line.draw(painter, color=QColor(255, 255, 255), width=5)
        for segment in self.middle_dashed_lines:
            segment.draw(
                painter,
                color=QColor(255, 255, 255),
                width=5,
                dash_style=[5, 5],
            )
