from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from src.primitives.segment import Segment


class Lane:
    def __init__(
        self,
        segment: Segment,
        is_most_left_lane: bool,
        is_most_right_lane: bool,
        traffic_speed: int,
        elevation: int = 0,
        width: int = 50,
    ) -> None:
        self.segment = segment
        self.is_most_left_lane = is_most_left_lane
        self.is_most_right_lane = is_most_right_lane
        self.traffic_speed = traffic_speed
        self.elevation = elevation
        self.width = width
        if self.is_most_left_lane:
            self.left_line = self.segment.make_parallel_with_offset(self.width / 2)
        self.right_line = self.segment.make_parallel_with_offset(-self.width / 2)

    def draw(self, painter: QPainter) -> None:
        """Draw the intersection area using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
        """
        # self.segment.draw(painter, self.width / 3, color=QColor(255, 0, 0))
        if self.is_most_left_lane and self.is_most_right_lane:
            self.left_line.draw(painter, 5, color=QColor(255, 255, 255))
            self.right_line.draw(painter, 5, color=QColor(255, 255, 255))
        elif self.is_most_left_lane:
            self.left_line.draw(painter, 5, color=QColor(255, 255, 255))
            self.right_line.draw(
                painter, 5, color=QColor(255, 255, 255), dash_style=[10, 10]
            )
        elif self.is_most_right_lane:
            self.right_line.draw(painter, 5, color=QColor(255, 255, 255))
        else:
            self.right_line.draw(
                painter, 5, color=QColor(255, 255, 255), dash_style=[10, 10]
            )
        painter.save()
        painter.translate(
            self.segment.start.midpoint(self.segment.end).x,
            self.segment.start.midpoint(self.segment.end).y,
        )
        painter.rotate(-self.segment.angle() + 90)
        painter.scale(1, 3)
        font = painter.font()
        font.setPixelSize(20)
        painter.setFont(font)
        painter.drawText(
            -round(self.width / 2),
            -round(self.width / 2),
            round(self.width),
            round(self.width),
            Qt.AlignmentFlag.AlignCenter,
            f"🡩\n{self.traffic_speed}",
        )
        painter.restore()
