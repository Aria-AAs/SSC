"""This module contains some utility functions."""

from math import inf
from random import random
from PyQt6.QtGui import QColor
from src.primitives.point import Point
from src.primitives.segment import Segment


def nearest_point(reference_point: Point, points: list) -> Point:
    """Find the nearest point to the given reference point from the given list of points.

    Args:
        reference_point (Point): The given reference point.
        points (list): A list of points.

    Returns:
        Point: The nearest point to the given reference point.
    """
    minimum_distance = inf
    nearest = None
    for point in points:
        distance = point.distance_to_point(reference_point)
        if distance < minimum_distance:
            minimum_distance = distance
            nearest = point
    return nearest


def nearest_segment(reference_point: Point, segments: list) -> Segment:
    """Find the nearest segment to the given reference point from the given list of segments.

    Args:
        reference_point (Point): The given reference point.
        segments (list): A list of segments.

    Returns:
        Segment: The nearest segment to the given reference point.
    """
    minimum_distance = inf
    nearest = None
    for segment in segments:
        distance = segment.distance_to_point(reference_point)
        if distance < minimum_distance:
            minimum_distance = distance
            nearest = segment
    return nearest


def lerp(a: float, b: float, t: float) -> float:
    """Calculate a linear interpolation.

    Args:
        a (float): First value.
        b (float): Second value.
        t (float): The alpha value

    Returns:
        float: A value between the a and the b.
    """
    return a + (b - a) * t


def lerp_inverse(a: float, b: float, v: float) -> float:
    """Calculate the inverse of linear interpolation.

    Args:
        a (float): First value.
        b (float): Second value.
        v (float): A value between first value and second value.

    Returns:
        float: The alpha value.
    """
    return (v - a) / (b - a)


def lerp_2d(a: Point, b: Point, t: float) -> Point:
    """Calculate a linear interpolation for points.

    Args:
        a (Point): First point.
        b (Point): Second point.
        t (float): The alpha value.

    Returns:
        Point: A point between the a and the b.
    """
    return Point(lerp(a.x, b.x, t), lerp(a.y, b.y, t))


def find_intersection(a1: Point, a2: Point, b1: Point, b2: Point) -> dict | None:
    """Find the intersection between two line.

    Args:
        a1 (Point): Start of the first line.
        a2 (Point): end of the first line.
        b1 (Point): Start of the second line.
        b2 (Point): end of the second line.

    Returns:
        dict | None: Intersection information if exists.
    """
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
    """Find a random color in the given range of hues.

    Args:
        start_hue (float): Start of the hue range.
        end_hue (float): End of the hue range.

    Returns:
        QColor: The random color
    """
    hue = start_hue + random() * (end_hue - start_hue)
    return QColor.fromHsv(hue, 1, 1, 1)


def change_range(
    value: float,
    input_minimum: float,
    input_maximum: float,
    output_minimum: float,
    output_maximum: float,
) -> float:
    """Change the range of a value.

    Args:
        value (float): The value to change range.
        input_minimum (float): minimum of the old range.
        input_maximum (float): maximum of the old range.
        output_minimum (float): minimum of the new range.
        output_maximum (float): maximum of the new range.

    Returns:
        float: The value in new range.
    """
    return (value - input_minimum) * (output_maximum - output_minimum) / (
        input_maximum - input_minimum
    ) + output_minimum


def red_green_color(value: float) -> QColor:
    """Calculate an RGBA color based on a value. black if the value is 0, red if the value is -1,
    and green if the value is 1 otherwise in between.

    Args:
        value (float): The value to calculate the RGBA color.

    Returns:
        QColor: The calculated color
    """
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


def green_red_color(value: float) -> QColor:
    """Calculate an RGBA color based on a value. black if the value is 0, green if the value is -1,
    and red if the value is 1 otherwise in between.

    Args:
        value (float): The value to calculate the RGBA color.

    Returns:
        QColor: The calculated color
    """
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
    """Find the sign of a value. 1 if the value is greater than 0 and positive,
    -1 if the value is less than 0 and negative, and 0 if the value is 0.

    Args:
        x (float): the value to find the sign.

    Returns:
        int: The sign of the value
    """
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
