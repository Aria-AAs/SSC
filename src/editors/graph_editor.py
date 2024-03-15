"""This module contains the GraphEditor class."""

from PyQt6.QtGui import QPainter, QColor
from src.maths.graph import Graph
from src.majors.viewport import Viewport
from src.primitives.point import Point
from src.primitives.segment import Segment
from src.primitives.circle import Circle
from src.maths.utils import nearest_point


class GraphEditor:
    """GraphEditor class allows editing the graph."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.selected = None
        self.hovered = None
        self.mouse_position = None
        self.dragging = None

    def mouse_left_button_down(self, mouse_position: Point) -> None:
        """The mouse_left_button_down method is an event handler.
        It is called whenever the mouse's left button is pressed inside the editor window.

        Args:
            mouse_position (Point): The position of the mouse in the window.
        """
        if self.hovered:
            self.select(self.hovered)
            self.dragging = True
        else:
            self.graph.add_point(mouse_position)
            self.select(mouse_position)
            self.hovered = mouse_position

    def mouse_right_button_down(self) -> None:
        """The mouse_right_button_down method is an event handler.
        It is called whenever the mouse's right button is pressed inside the editor window.
        """
        if self.selected:
            self.selected = None
        elif self.hovered:
            self.graph.remove_point(self.hovered)
            self.hovered = None

    def mouse_move(self, position: Point, viewport: Viewport) -> None:
        """The mouse_move method is an event handler.
        It is called whenever the mouse moves inside the editor window.

        Args:
            position (Point): The position of the mouse in the window.
            viewport (Viewport): The viewport of the application.
        """
        self.mouse_position = viewport.get_mouse(position, True)
        self.hovered = nearest_point(
            self.mouse_position, self.graph.points, 10 * viewport.zoom
        )
        if self.dragging:
            self.selected.x = self.mouse_position.x
            self.selected.y = self.mouse_position.y

    def mouse_left_button_up(self) -> None:
        """The mouse_left_button_up method is an event handler.
        It is called whenever the mouse's left button is released inside the editor window.
        """
        self.dragging = False

    def select(self, point: Point) -> None:
        """Select the given point and try to add a segment if a point was selected before.

        Args:
            point (Point): The point to select.
        """
        if self.selected:
            self.graph.add_segment(Segment(self.selected, point))
        self.selected = point

    def draw(self, painter: QPainter, zoom: float) -> None:
        """Draw the graph editor using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            zoom (float): _description_
        """
        self.graph.draw(painter, zoom)
        if self.hovered:
            Circle(self.hovered.x, self.hovered.y, zoom * 10).draw(
                painter, QColor(0, 0, 0), outline_thickness=3 * zoom, transparency=0.6
            )
        if self.selected:
            if self.hovered:
                intent_point = self.hovered
            else:
                intent_point = self.mouse_position
            Circle(self.selected.x, self.selected.y, 7 * zoom).draw(
                painter,
                outline_thickness=3 * zoom,
                outline_color=QColor(255, 255, 0),
            )
            Segment(self.selected, intent_point).draw(
                painter, 3 * zoom, dash_style=[3 * zoom, 3 * zoom]
            )
