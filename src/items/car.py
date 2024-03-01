"""This module contains the Car class."""

from math import pi, sqrt, atan2, sin, cos, radians, degrees
from pathlib2 import Path
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPixmap, QRegion, QBitmap, QColor
from src.items.sensor import Sensor
from src.primitives.point import Point
from src.primitives.polygon import Polygon
from src.brains.neural_network import NeuralNetwork
from src.maths.utils import change_range, lerp


class Car:
    """Car class represents a car."""

    max_speed = 5

    def __init__(
        self,
        position: Point,
        angle: float = 0,
        control_type: str = "user",
        width: float = 30,
        height: float = 50,
        color: QColor = QColor(255, 0, 0),
    ) -> None:
        self.position = position
        self.width = width
        self.height = height
        self.angle = angle
        self.color = color
        self.control_type = control_type
        self.speed = 0
        self.friction = 0.05
        self.age = 0
        self.acceleration = 0.2
        self.damaged = False
        self.fitness = 0
        if control_type != "dummy":
            self.sensor_count = 15
            self.sensor_spread = 160
            self.sensor_length = 150
            self.sensors = []
            for _ in range(self.sensor_count):
                self.sensors.append(Sensor(self.sensor_length))
            self.brain = NeuralNetwork([self.sensor_count + 1, 32, 32, 16, 4])
        if control_type == "ai":
            self.use_brain = True
        else:
            self.use_brain = False
        self.polygon = self.create_polygon()
        image = QPixmap(
            str(Path(Path(__file__).parent.parent.parent, "asset/images/car.png"))
        )
        self.image = image.scaledToWidth(
            self.width, Qt.TransformationMode.SmoothTransformation
        )
        self.mask = self.image.toImage().createAlphaMask()

    def update(self, road_borders: list) -> None:
        """Calculate the situation of the car.

        Args:
            road_borders (list): The borders of roads where cars get damaged.
        """
        if not self.damaged:
            self.age += 1
            self.move()
            self.fitness += self.speed + change_range(self.age, 0, 10000, 0, 1)
            self.polygon = self.create_polygon()
            self.damaged = self.assess_damage(road_borders)
            if self.sensors:
                offsets = []
                for i in range(self.sensor_count):
                    if self.sensor_count == 1:
                        t = 0.5
                    else:
                        t = i / (self.sensor_count - 1)
                    sensor_angle = (
                        lerp(self.sensor_spread / 2, -self.sensor_spread / 2, t)
                        + self.angle
                    )
                    self.sensors[i].update(road_borders, sensor_angle, self.position)
                    if self.sensors[i].read():
                        offsets.append(self.sensors[i].read())
                    else:
                        offsets.append(0)
                offsets.append(
                    change_range(self.speed, -self.max_speed / 2, self.max_speed, -1, 1)
                )
                outputs = self.brain.feedforward(offsets)
                if self.use_brain:
                    if outputs[0]:
                        self.accelerate_forward()
                    if outputs[1]:
                        self.accelerate_backward()
                    if outputs[2]:
                        self.turn_steering_wheel(degrees(0.03))
                    if outputs[3]:
                        self.turn_steering_wheel(degrees(-0.03))

    def create_polygon(self) -> Polygon:
        """Create a polygon that the car fits into it.

        Returns:
            Polygon: The created polygon.
        """
        points = []
        radius = sqrt(self.width**2 + self.height**2) / 2
        alpha = atan2(self.width, self.height)
        points.append(
            Point(
                self.position.x + sin(radians(self.angle) - alpha) * radius,
                self.position.y - cos(radians(self.angle) - alpha) * radius,
            )
        )
        points.append(
            Point(
                self.position.x + sin(radians(self.angle) + alpha) * radius,
                self.position.y - cos(radians(self.angle) + alpha) * radius,
            )
        )
        points.append(
            Point(
                self.position.x + sin(pi + radians(self.angle) - alpha) * radius,
                self.position.y - cos(pi + radians(self.angle) - alpha) * radius,
            )
        )
        points.append(
            Point(
                self.position.x + sin(pi + radians(self.angle) + alpha) * radius,
                self.position.y - cos(pi + radians(self.angle) + alpha) * radius,
            )
        )
        return Polygon(points)

    def assess_damage(self, road_borders: list) -> bool:
        """Check if the car crashed.

        Args:
            road_borders (list): The borders of roads where cars get damaged.

        Returns:
            bool: True if the car crashed and false if the car is still intact.
        """
        i = 0
        while i < len(road_borders):
            if self.polygon.intersect_with_polygon(road_borders[i]):
                self.speed = 0
                return True
            i += 1
        return False

    def move(self):
        """Calculate the physics of the car movement."""
        if self.speed > 0:
            self.speed -= self.friction
        elif self.speed < 0:
            self.speed += self.friction
        if abs(self.speed) < self.friction:
            self.speed = 0
        self.position.x += sin(radians(self.angle)) * self.speed
        self.position.y -= cos(radians(self.angle)) * self.speed

    def turn_steering_wheel(self, amount: float):
        """Simulate turning the steering wheel by changing the angle of the car.

        Args:
            amount (float): The amount of turning.
        """
        if self.speed != 0:
            self.angle += amount

    def accelerate_forward(self):
        """Simulate accelerating forward by changing the speed."""
        if not self.damaged:
            self.speed += self.acceleration
            if self.speed > self.max_speed:
                self.speed = self.max_speed

    def accelerate_backward(self):
        """Simulate accelerating backward by changing the speed."""
        if not self.damaged:
            self.speed -= self.acceleration
            if self.speed < -self.max_speed / 2:
                self.speed = -self.max_speed / 2

    def draw(self, painter: QPainter, transparency: float = 1):
        """Draw the car using the given painter.

        Args:
            painter (QPainter): The painter is used for drawing.
            transparency (float, optional): The percentage of transparency.
            0 means invisible and 1 means fully solid. Defaults to 1.
        """
        rect = QRect(-self.width // 2, -self.height // 2, self.width, self.height)
        painter.save()
        painter.translate(self.position.x, self.position.y)
        painter.rotate(self.angle)
        painter.setOpacity(transparency)
        painter.drawPixmap(rect, self.image)
        if not self.damaged:
            painter.setOpacity(1)
            painter.translate(-self.width / 2, -self.height / 2)
            painter.setClipRegion(QRegion(QBitmap.fromImage(self.mask)))
            painter.setCompositionMode(painter.CompositionMode.CompositionMode_Multiply)
            painter.translate(self.width / 2, self.height / 2)
            painter.fillRect(rect, QColor(255, 0, 0))
        painter.restore()
