from math import inf
from random import random
from PyQt6.QtGui import QColor
from src.primitives.point import Point
from src.primitives.segment import Segment


def nearest_point(reference_point: Point, points: list) -> Point:
    minimum_distance = inf
    nearest = None
    for point in points:
        distance = point.distance_to_point(reference_point)
        if distance < minimum_distance:
            minimum_distance = distance
            nearest = point
    return nearest


def nearest_segment(reference_point: Point, segments: list) -> Segment:
    minimum_distance = inf
    nearest = None
    for segment in segments:
        distance = segment.distance_to_point(reference_point)
        if distance < minimum_distance:
            minimum_distance = distance
            nearest = segment
    return nearest


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def lerp_inverse(a: float, b: float, v: float) -> float:
    return (v - a) / (b - a)


def lerp_2d(a: Point, b: Point, t: float) -> Point:
    return Point(lerp(a.x, b.x, t), lerp(a.y, b.y, t))


def find_intersection(a1: Point, a2: Point, b1: Point, b2: Point) -> dict | None:
    t_top = (b2.x - b1.x) * (a1.y - b1.y) - (b2.y - b1.y) * (a1.x - b1.x)
    u_top = (b1.y - a1.y) * (a1.x - a2.x) - (b1.x - a1.x) * (a1.y - a2.y)
    bottom = (b2.y - b1.y) * (a2.x - a1.x) - (b2.x - b1.x) * (a2.y - a1.y)
    if bottom != 0:
        t = t_top / bottom
        u = u_top / bottom
        if 0 <= t <= 1 and 0 <= u <= 1:
            return {
                "x": lerp(a1.x, a2.x, t),
                "y": lerp(a1.y, a2.y, t),
                "offset": t,
            }
    return None


def get_random_color(start_hue: float, end_hue: float) -> QColor:
    hue = start_hue + random() * (end_hue - start_hue)
    return QColor.fromHsv(hue, 1, 1, 1)


def change_range(
    value: float,
    input_minimum: float,
    input_maximum: float,
    output_minimum: float,
    output_maximum: float,
) -> float:
    return (value - input_minimum) * (output_maximum - output_minimum) / (
        input_maximum - input_minimum
    ) + output_minimum


def get_rgba(value: float) -> QColor:
    a = abs(value)
    b = 0
    if value == 0:
        r = 0
        g = 0
    elif value > 0:
        r = 0
        g = 255
    else:
        r = 255
        g = 0
    return QColor(r, g, b, a)


def get_rgba_reverse(value: float) -> QColor:
    a = abs(value)
    b = 0
    if value == 0:
        r = 0
        g = 0
    elif value > 0:
        r = 255
        g = 0
    else:
        r = 0
        g = 255
    return QColor(r, g, b, a)


def sign(x: float) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
