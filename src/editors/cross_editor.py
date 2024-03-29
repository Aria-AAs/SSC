"""This module contains the CrossEditor class."""

from src.editors.graph_editor import GraphEditor
from src.primitives.point import Point
from src.markings.cross_marking import CrossMarking
from src.editors.marking_editor import MarkingEditor


class CrossEditor(MarkingEditor):
    """CrossEditor class allows editing cross markings. Inherited from MarkingEditor."""

    def __init__(self, graph_editor: GraphEditor) -> None:
        super().__init__(graph_editor, graph_editor.world.graph.segments)

    def create_marking(
        self, center_of_segment: Point, direction_of_segment: Point
    ) -> CrossMarking:
        return CrossMarking(
            center_of_segment,
            direction_of_segment,
            self.graph_editor.world.road_lane_width,
            self.graph_editor.world.road_lane_width / 2,
        )
