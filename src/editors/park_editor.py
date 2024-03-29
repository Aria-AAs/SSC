"""This module contains the ParkEditor class."""

from src.editors.graph_editor import GraphEditor
from src.primitives.point import Point
from src.markings.park_marking import ParkMarking
from src.editors.marking_editor import MarkingEditor


class ParkEditor(MarkingEditor):
    """ParkEditor class allows editing park markings. Inherited from MarkingEditor."""

    def __init__(self, graph_editor: GraphEditor) -> None:
        super().__init__(graph_editor, graph_editor.world.lane_guides)

    def create_marking(
        self, center_of_segment: Point, direction_of_segment: Point
    ) -> ParkMarking:
        return ParkMarking(
            center_of_segment,
            direction_of_segment,
            self.graph_editor.world.road_lane_width / 2,
            self.graph_editor.world.road_lane_width / 2,
        )
