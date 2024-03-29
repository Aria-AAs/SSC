"""This module contains the StartEditor class."""

from src.editors.graph_editor import GraphEditor
from src.primitives.point import Point
from src.markings.start_marking import StartMarking
from src.editors.marking_editor import MarkingEditor


class StartEditor(MarkingEditor):
    """StartEditor class allows editing start markings. Inherited from MarkingEditor."""

    def __init__(self, graph_editor: GraphEditor) -> None:
        super().__init__(graph_editor, graph_editor.world.lane_guides)

    def create_marking(
        self, center_of_segment: Point, direction_of_segment: Point
    ) -> StartMarking:
        return StartMarking(
            center_of_segment,
            direction_of_segment,
            self.graph_editor.world.road_lane_width / 2,
            self.graph_editor.world.road_lane_width / 2,
        )
