"""This module contains the World class."""

from typing import Self
from math import floor, inf
from json import dump, load
from random import random
from pathlib2 import Path
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.segment import Segment
from src.primitives.polygon import Polygon
from src.maths.graph import Graph
from src.primitives.envelope import Envelope
from src.items.building import Building
from src.items.tree import Tree
from src.items.road import Road
from src.items.intersection import Intersection
from src.maths.utils import lerp, find_intersect


class World:
    """World class represents a world."""

    left_hand_rule = False

    def __init__(self) -> None:
        self.graph = Graph()
        self.road_lane_width = 50
        self.road_roundness = self.road_lane_width // 10
        self.building_width = 200
        self.building_minimum_length = 150
        self.space_between_objects = 50
        self.tree_size = 160
        self.roads = []
        self.intersections = []
        self.road_borders = []
        self.buildings = []
        self.trees = []
        self.lane_guides = []
        self.markings = []
        self.road_network = {}
        self.generate()

    def save(self) -> None:
        """Save the state of the application"""
        data = {"graph": self.graph, "roads": [], "markings": self.markings}
        for road in self.roads:
            data["roads"].append(
                {
                    "segment": road.segment,
                    "number_of_lanes_in_right_side": road.number_of_lanes_in_right_side,
                    "number_of_lanes_in_left_side": road.number_of_lanes_in_left_side,
                    "priority": road.priority,
                    "elevation": road.elevation,
                    "is_oneway": road.is_oneway,
                    "is_start_connected": road.is_start_connected,
                    "is_end_connected": road.is_end_connected,
                    "lefthand_rule": road.lefthand_rule,
                    "lane_width": road.lane_width,
                    "name": road.name,
                }
            )
        with open(
            Path(Path(__file__).parent.parent.parent, "data/backups/world_backup.json"),
            "wt",
            encoding="UTF-8",
        ) as file:
            dump(
                data,
                file,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
            )

    def load(self) -> Self:
        """A method that extracts information from data."""
        with open(
            Path(Path(__file__).parent.parent.parent, "data/backups/world_backup.json"),
            "rt",
            encoding="UTF-8",
        ) as file:
            data = load(file)
            for point in data["graph"]["points"]:
                self.graph.add_point(Point(point["x"], point["y"]))
            for segment in data["graph"]["segments"]:
                self.graph.add_segment(
                    Segment(
                        Point(segment["start"]["x"], segment["start"]["y"]),
                        Point(segment["end"]["x"], segment["end"]["y"]),
                    )
                )
            for road in data["roads"]:
                self.roads.append(
                    Road(
                        Segment(
                            Point(
                                road["segment"]["start"]["x"],
                                road["segment"]["start"]["y"],
                            ),
                            Point(
                                road["segment"]["end"]["x"], road["segment"]["end"]["y"]
                            ),
                        ),
                        road["number_of_lanes_in_left_side"],
                        road["number_of_lanes_in_right_side"],
                        road["name"],
                        road["lane_width"],
                        road["priority"],
                        road["elevation"],
                        road["is_oneway"],
                        self.left_hand_rule,
                        road["is_start_connected"],
                        road["is_end_connected"],
                    )
                )

    def generate(self) -> None:
        """Generate the world objects like roads, trees, buildings, and others."""
        # self.generate_roads()
        self.generate_road_network()
        self.generate_intersections()
        # self.buildings = self.generate_buildings()
        # self.trees = self.generate_trees()

    def generate_road_network(self) -> None:
        envelopes = []
        polygons = []
        for road in self.roads:
            envelopes.append(road.envelope)
            polygons.append(road.envelope.polygon)
        segments = Polygon.union(polygons)
        self.road_network["envelopes"] = envelopes
        self.road_network["outer_lines"] = segments

    def generate_roads(
        self, number_of_left_lanes: int, number_of_right_lanes: int, is_oneway: bool
    ) -> None:
        """Generate roads, road borders, and lane guides."""
        roads = []
        segments = self.graph.segments.copy()
        for road in self.roads:
            if road.segment in segments:
                roads.append(
                    Road(
                        road.segment,
                        road.number_of_lanes_in_left_side,
                        road.number_of_lanes_in_right_side,
                        road.name,
                        road.lane_width,
                        road.priority,
                        road.elevation,
                        road.is_oneway,
                        road.lefthand_rule,
                        road.is_start_connected,
                        road.is_end_connected,
                    )
                )
                segments.remove(road.segment)
                continue
        for segment in segments:
            for road in self.roads:
                if (
                    road.segment.distance_to_point(segment.start) < road.width
                    or road.segment.distance_to_point(segment.end) < road.width
                ):
                    self.add_road(
                        segment, number_of_left_lanes, number_of_right_lanes, is_oneway
                    )
        self.roads = roads
        self.generate_intersections()

    def generate_intersections(self) -> None:
        """Find and generate intersections."""
        self.intersections.clear()
        for point in self.graph.points:
            roads = []
            for road in self.roads:
                if road.segment.contains_point(point):
                    roads.append(road)
            if roads:
                self.intersections.append(Intersection(point, roads))

    def generate_buildings(self) -> list:
        """Generate buildings.

        Returns:
            list: A list of generated buildings.
        """
        envelopes = []
        for segment in self.graph.segments:
            envelopes.append(
                Envelope(
                    segment,
                    self.road_lane_width
                    + self.building_width
                    + self.space_between_objects * 2,
                    self.road_roundness,
                )
            )
        polygons = []
        for envelope in envelopes:
            polygons.append(envelope.polygon)
        guides = Polygon.union(polygons)
        i = 0
        while i < len(guides):
            if guides[i].length() < self.building_minimum_length:
                guides.pop(i)
                continue
            i += 1
        supports = []
        for segment in guides:
            length = segment.length() + self.space_between_objects
            building_count = floor(
                length / (self.building_minimum_length + self.space_between_objects)
            )
            building_length = length / building_count - self.space_between_objects
            direction = segment.direction()
            point_1 = segment.start
            point_2 = point_1 + direction.scale(building_length)
            supports.append(Segment(point_1, point_2))
            i = 2
            while i <= building_count:
                point_1 = point_2 + direction.scale(self.space_between_objects)
                point_2 = point_1 + direction.scale(building_length)
                supports.append(Segment(point_1, point_2))
                i += 1
        bases = []
        for segment in supports:
            bases.append(Envelope(segment, self.building_width).polygon)
        i = 0
        while i < len(bases) - 1:
            j = i + 1
            while j < len(bases):
                if (
                    bases[i].intersect_with_polygon(bases[j])
                    or bases[i].distance_to_polygon(bases[j])
                    < self.space_between_objects
                ):
                    bases.pop(j)
                    continue
                j += 1
            i += 1
        buildings = []
        for base in bases:
            if len(base.points) == 4:
                buildings.append(Building(base))
        return buildings

    def generate_trees(self) -> list:
        """Generate trees.

        Returns:
            list: A list of generated trees.
        """
        points = []
        illegal_polygons = []
        for road in self.roads:
            illegal_polygons.append(road.polygon)
        for road_boarder in self.road_borders:
            points.append(road_boarder.start)
            points.append(road_boarder.end)
        for building in self.buildings:
            illegal_polygons.append(building.base)
            for point in building.base.points:
                points.append(point)
        trees = []
        if points:
            points.sort(key=lambda point: point.x)
            most_left_point = points[0]
            most_right_point = points[-1]
            points.sort(key=lambda point: point.y)
            most_top_point = points[0]
            most_bottom_point = points[-1]
            try_counter = 0
            while try_counter < 100:
                point = Point(
                    lerp(most_left_point.x, most_right_point.x, random()),
                    lerp(most_top_point.y, most_bottom_point.y, random()),
                )
                keep = True
                for polygon in illegal_polygons:
                    if (
                        polygon.contains_point(point)
                        or polygon.distance_to_point(point) < self.tree_size / 2
                    ):
                        keep = False
                        break
                if keep:
                    for tree in trees:
                        if point.distance_to_point(tree.center) < self.tree_size:
                            keep = False
                            break
                if keep:
                    close_to_something = False
                    for polygon in illegal_polygons:
                        if polygon.distance_to_point(point) < self.tree_size * 2.2:
                            close_to_something = True
                            break
                    keep = close_to_something
                if keep:
                    trees.append(Tree(point, self.tree_size))
                    try_counter = 0
                    continue
                try_counter += 1
        return trees

    def generate_lane_guides(self) -> list:
        """Generate lane guides. Lane guides are Segments in the middle of lanes of roads.

        Returns:
            list: A list of generated lane guides.
        """
        polygons = []
        for segment in self.graph.segments:
            envelope = Envelope(segment, self.road_lane_width / 2, self.road_roundness)
            polygons.append(envelope.polygon)
        return Polygon.union(polygons)

    def add_road(
        self,
        segment: Segment,
        number_of_lanes_in_left_side: int,
        number_of_lanes_in_right_side: int,
        is_oneway: bool,
    ) -> None:
        if (
            segment.length()
            <= (
                self.road_lane_width
                * (number_of_lanes_in_left_side + number_of_lanes_in_right_side)
            )
            + 50
        ):
            return
        if not self.roads:
            self.graph.add_segment(segment)
            self.roads.append(
                Road(
                    segment,
                    number_of_lanes_in_left_side,
                    number_of_lanes_in_right_side,
                    "",
                    self.road_lane_width,
                    0,
                    0,
                    is_oneway,
                    self.left_hand_rule,
                )
            )
        for intersection in self.intersections:
            if intersection.location in (segment.start, segment.end):
                for road in intersection.connected_roads:
                    if road.segment.angle() - segment.angle() < 30:
                        return
        for road in self.roads:
            distance_1 = inf
            distance_2 = inf
            if road.segment == segment:
                continue
            project = road.segment.project_point(segment.start)
            if 0 <= project["offset"] <= 1:
                distance_1 = segment.start.distance_to_point(project["point"])
            project = road.segment.project_point(segment.end)
            if 0 <= project["offset"] <= 1:
                distance_2 = segment.end.distance_to_point(project["point"])
            distance = min(distance_1, distance_2)
            if distance == 0:
                continue
            if distance < 20 + (road.width / 2) + (
                (
                    self.road_lane_width
                    * (number_of_lanes_in_left_side + number_of_lanes_in_right_side)
                )
                / 2
            ):
                return
            if distance_1 < distance_2:
                distance_1 = segment.start.distance_to_point(road.segment.start)
                distance_2 = segment.start.distance_to_point(road.segment.end)
                distance = min(distance_1, distance_2)
            else:
                distance_1 = segment.end.distance_to_point(road.segment.start)
                distance_2 = segment.end.distance_to_point(road.segment.end)
                distance = min(distance_1, distance_2)
            if distance == 0:
                continue
            if distance < 20 + (road.width / 2) + (
                (
                    self.road_lane_width
                    * (number_of_lanes_in_left_side + number_of_lanes_in_right_side)
                )
                / 2
            ):
                return
            for graph_segment in self.graph.segments:
                intersect = find_intersect(
                    segment.start, segment.end, graph_segment.start, graph_segment.end
                )
                if intersect and 0 < intersect["offset"] < 1:
                    existing_road = None
                    for road in self.roads:
                        if road.segment == graph_segment:
                            existing_road = road
                            break
                    if not existing_road:
                        print("error")
                    point = Point(intersect["x"], intersect["y"])
                    if point.distance_to_point(graph_segment.start) < (
                        existing_road.width + 50
                    ):
                        return
                    if point.distance_to_point(graph_segment.end) < (
                        existing_road.width + 50
                    ):
                        return
                    if point.distance_to_point(segment.start) < (
                        (
                            self.road_lane_width
                            * (
                                number_of_lanes_in_left_side
                                + number_of_lanes_in_right_side
                            )
                        )
                        + 50
                    ):
                        return
                    if point.distance_to_point(segment.end) < (
                        (
                            self.road_lane_width
                            * (
                                number_of_lanes_in_left_side
                                + number_of_lanes_in_right_side
                            )
                        )
                        + 50
                    ):
                        return
                    self.graph.add_point(point)
                    new_segment = Segment(graph_segment.start, point)
                    self.add_road(
                        new_segment,
                        existing_road.number_of_lanes_in_left_side,
                        existing_road.number_of_lanes_in_right_side,
                        existing_road.is_oneway,
                    )
                    new_segment = Segment(point, graph_segment.end)
                    self.add_road(
                        new_segment,
                        existing_road.number_of_lanes_in_left_side,
                        existing_road.number_of_lanes_in_right_side,
                        existing_road.is_oneway,
                    )
                    new_segment = Segment(segment.start, point)
                    self.add_road(
                        new_segment,
                        number_of_lanes_in_left_side,
                        number_of_lanes_in_right_side,
                        is_oneway,
                    )
                    new_segment = Segment(point, segment.end)
                    self.add_road(
                        new_segment,
                        number_of_lanes_in_left_side,
                        number_of_lanes_in_right_side,
                        is_oneway,
                    )
                    if graph_segment in self.graph.segments:
                        self.graph.remove_segment(graph_segment)
                    return
            self.graph.add_segment(segment)
            self.roads.append(
                Road(
                    segment,
                    number_of_lanes_in_left_side,
                    number_of_lanes_in_right_side,
                    "",
                    self.road_lane_width,
                    0,
                    0,
                    is_oneway,
                    self.left_hand_rule,
                )
            )
        self.generate_intersections()

    def draw(
        self,
        painter: QPainter,
        view_point: Point,
        render_radius: float = 1000,
    ) -> None:
        """Draw the world using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            view_point (Point): The center of the viewport.
            render_radius (float, optional): Objects that are outside of this radius relative to
            view_point will not draw. Defaults to 1000.
        """
        # for road in self.roads:
        #     road.draw(painter)
        for envelope in self.road_network["envelopes"]:
            envelope.draw(
                painter,
                color=QColor(51, 51, 51),
                outline_width=15,
                outline_color=QColor(51, 51, 51),
            )
        for segment in self.road_network["outer_lines"]:
            segment.draw(painter, color=QColor(255, 255, 255), width=5)
        for road in self.roads:
            road.draw(painter)
        for marking in self.markings:
            if marking.type != "start":
                marking.draw(painter)
        items = []
        for building in self.buildings:
            if building.base.distance_to_point(view_point) < render_radius:
                items.append(building)
        for tree in self.trees:
            if tree.base.distance_to_point(view_point) < render_radius:
                items.append(tree)
        items.sort(
            reverse=True, key=lambda item: item.base.distance_to_point(view_point)
        )
        for item in items:
            item.draw(painter, view_point)
        # for intersection in self.intersections:
        #     intersection.draw(painter)
