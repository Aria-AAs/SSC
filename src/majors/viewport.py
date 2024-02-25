from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.maths.utils import sign


class Viewport:
    def __init__(
        self,
        center_x: float,
        center_y: float,
        offset: Point | None = None,
    ) -> None:
        self.zoom = 1
        self.center = Point(center_x, center_y)
        if offset:
            self.offset = offset
        else:
            self.offset = self.center.scale(-1)
        self.drag = {
            "start": Point(0, 0),
            "end": Point(0, 0),
            "offset": Point(0, 0),
            "active": False,
        }

    def reset(self, painter: QPainter, area_rect: QRect):
        painter.fillRect(area_rect, QColor(35, 170, 85))
        painter.translate(self.center.x, self.center.y)
        painter.scale(1 / self.zoom, 1 / self.zoom)
        offset = self.get_offset()
        painter.translate(offset.x, offset.y)

    def get_offset(self) -> Point:
        return self.offset + self.drag["offset"]

    def get_mouse(self, position: Point, subtract_drag_offset: bool = False) -> Point:
        point = Point(
            (position.x - self.center.x) * self.zoom - self.offset.x,
            (position.y - self.center.y) * self.zoom - self.offset.y,
        )
        if subtract_drag_offset:
            point -= self.drag["offset"]
        return point

    def mouse_middle_button_down(self, mouse_position: Point) -> None:
        position = self.get_mouse(mouse_position)
        self.drag["start"] = position
        self.drag["active"] = True

    def mouse_move(self, position: Point) -> None:
        self.drag["end"] = self.get_mouse(position)
        self.drag["offset"] = self.drag["end"] - self.drag["start"]

    def mouse_middle_button_up(self) -> None:
        self.offset += self.drag["offset"]
        self.drag = {
            "start": Point(0, 0),
            "end": Point(0, 0),
            "offset": Point(0, 0),
            "active": False,
        }

    def mouse_wheel_scroll(self, steps: int):
        direction = sign(steps)
        step = 0.2
        self.zoom += -step * direction
        self.zoom = max(0.4, min(5, self.zoom))
