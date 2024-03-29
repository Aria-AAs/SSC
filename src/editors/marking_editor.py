"""This module contains the MarkingEditor class."""

from PyQt6.QtGui import QPainter
from src.editors.graph_editor import GraphEditor
from src.majors.viewport import Viewport
from src.markings.marking import Marking
from src.primitives.point import Point
from src.maths.utils import nearest_segment


class MarkingEditor:
    """MarkingEditor is an abstract class for different marking editors."""

    def __init__(self, graph_editor: GraphEditor, target_segments: list) -> None:
        self.graph_editor = graph_editor
        self.target_segments = target_segments
        self.intent = None

    def disable(self) -> None:
        """Disable the marking editor functionality."""
        self.intent = None

    def create_marking(
        self, center_of_segment: Point, direction_of_segment: Point
    ) -> Marking:
        """Create an object from the marking class. This is an abstract method.

        Args:
            center_of_segment (Point): The center of the segment to make marking.
            direction_of_segment (Point): The direction of the segment to make marking

        Returns:
            Marking: The marking that was created.
        """
        return Marking(center_of_segment, direction_of_segment, 0, 0)

    def mouse_left_button_down(self) -> None:
        """The mouse_left_button_down method is an event handler.
        It is called whenever the mouse's left button is pressed inside the marking editor window.

        Args:
            mouse_position (Point): The position of the mouse in the window.
        """
        if self.intent:
            self.graph_editor.world.markings.append(self.intent)
            self.intent = None

    def mouse_right_button_down(self, position: Point, viewport: Viewport) -> None:
        """The mouse_right_button_down method is an event handler.
        It is called whenever the mouse's right button is pressed inside the marking editor window.
        """
        mouse_position = viewport.get_mouse(position)
        for marking in self.graph_editor.world.markings:
            if marking.polygon.contains_point(mouse_position):
                self.graph_editor.world.markings.remove(marking)

    def mouse_move(self, position: Point, viewport: Viewport) -> None:
        """The mouse_move method is an event handler.
        It is called whenever the mouse moves inside the marking editor window.

        Args:
            position (Point): The position of the mouse in the window.
            viewport (Viewport): The viewport of the application.
        """
        mouse_position = viewport.get_mouse(position, True)
        segment = nearest_segment(mouse_position, self.target_segments)
        if segment:
            project = segment.project_point(mouse_position)
            if 0 <= project["offset"] <= 1:
                self.intent = self.create_marking(project["point"], segment.direction())
            else:
                self.intent = None
        else:
            self.intent = None

    def draw(self, painter: QPainter, _: None = None) -> None:
        """Draw the graph editor using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            _ (None, optional): An unused argument that no matter. Defaults to None.
        """
        if self.intent:
            self.intent.draw(painter)
