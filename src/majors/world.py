"""This module contains the World class."""

from typing import Self
from math import floor
from random import random
from PyQt6.QtGui import QPainter, QColor
from src.primitives.point import Point
from src.primitives.segment import Segment
from src.primitives.polygon import Polygon
from src.maths.graph import Graph
from src.primitives.envelope import Envelope
from src.items.building import Building
from src.items.tree import Tree
from src.maths.utils import lerp
from data.backups.test_graph import test_graph


class World:
    """World class represents a world."""

    def __init__(self) -> None:
        self.graph = Graph()
        self.graph.load(test_graph)
        self.road_lane_width = 120
        self.road_roundness = self.road_lane_width // 10
        self.building_width = 200
        self.building_minimum_length = 150
        self.space_between_objects = 50
        self.tree_size = 160
        self.roads = []
        self.road_borders = []
        self.buildings = []
        self.trees = []
        self.lane_guides = []
        self.markings = []
        self.generate()

    def load(self, data: dict) -> Self:
        """A method that extracts information from data.

        Args:
            data (dict): The given data.
        """
        world = World()
        world.graph = data.graph
        return world

    def generate(self) -> None:
        """Generate the world objects like roads, trees, buildings, and others."""
        self.generate_roads()
        self.buildings = self.generate_buildings()
        self.trees = self.generate_trees()

    def generate_roads(self) -> None:
        """Generate roads, road borders, and lane guides."""
        self.roads.clear()
        self.lane_guides.clear()
        for segment in self.graph.segments:
            self.roads.append(
                Envelope(segment, self.road_lane_width, self.road_roundness)
            )
        road_polygon = []
        for road in self.roads:
            road_polygon.append(road.polygon)
        self.road_borders = Polygon([]).union(road_polygon)
        self.lane_guides = self.generate_lane_guides()

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
        guides = Polygon([]).union(polygons)
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
        return Polygon([]).union(polygons)

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
        for road in self.roads:
            road.draw(
                painter,
                color=QColor(51, 51, 51),
                outline_width=15,
                outline_color=QColor(51, 51, 51),
            )
        for segment in self.graph.segments:
            segment.draw(
                painter,
                color=QColor(255, 255, 255),
                width=4,
                dash_style=[5, 5],
            )
        for segment in self.road_borders:
            segment.draw(painter, color=QColor(255, 255, 255), width=4)
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
