"""This module contains the Viewport class."""

from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.maths.utils import sign


class Viewport:
    """Viewport class represents a viewport."""

    def __init__(
        self,
        center_x: float,
        center_y: float,
        zoom: float = 1,
        offset: Point | None = None,
    ) -> None:
        self.zoom = zoom
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

    def get_offset(self) -> Point:
        """Calculate the offset from the zero position of the logical coordinate system.

        Returns:
            Point: The offset.
        """
        return self.offset + self.drag["offset"]

    def get_mouse(self, position: Point, subtract_drag_offset: bool = False) -> Point:
        """Calculate the position of the mouse in the viewport.

        Args:
            position (Point): The position of the mouse in the window.
            subtract_drag_offset (bool, optional): Set it to true if you want to subtract
            the dragging offset from the mouse position. Defaults to False.

        Returns:
            Point: The position of the mouse in the viewport.
        """
        point = Point(
            (position.x - self.center.x) * self.zoom - self.offset.x,
            (position.y - self.center.y) * self.zoom - self.offset.y,
        )
        if subtract_drag_offset:
            point -= self.drag["offset"]
        return point

    def mouse_middle_button_down(self, mouse_position: Point) -> None:
        """The mouse_middle_button_down method is an event handler.
        It is called whenever the middle button of the mouse is pressed.

        Args:
            mouse_position (Point): The position of the mouse in the window.
        """
        position = self.get_mouse(mouse_position)
        self.drag["start"] = position
        self.drag["active"] = True

    def mouse_move(self, position: Point) -> None:
        """The mouse_move method is an event handler.
        It is called whenever the mouse's middle button is pressed and the mouse moves.

        Args:
            position (Point): The position of the mouse in the window.
        """
        self.drag["end"] = self.get_mouse(position)
        self.drag["offset"] = self.drag["end"] - self.drag["start"]

    def mouse_middle_button_up(self) -> None:
        """The mouse_middle_button_up method is an event handler.
        It is called whenever the mouse's middle button is released."""
        self.offset += self.drag["offset"]
        self.drag = {
            "start": Point(0, 0),
            "end": Point(0, 0),
            "offset": Point(0, 0),
            "active": False,
        }

    def mouse_wheel_scroll(self, steps: int):
        """The mouse_wheel_scroll method is an event handler.
        It is called whenever the mouse wheel turned.

        Args:
            steps (int): The steps that the mouse wheel was turned.
        """
        direction = sign(steps)
        step = 0.2
        self.zoom += -step * direction
        self.zoom = max(0.4, min(5, self.zoom))

    def reset(self, painter: QPainter, area_rect: QRect):
        """Reset the scene based on the viewport using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            area_rect (QRect): The scene area.
        """
        painter.fillRect(area_rect, QColor(35, 170, 85))
        painter.translate(self.center.x, self.center.y)
        painter.scale(1 / self.zoom, 1 / self.zoom)
        offset = self.get_offset()
        painter.translate(offset.x, offset.y)
