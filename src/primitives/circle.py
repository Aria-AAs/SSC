from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from src.primitives.point import Point


class Circle:
    def __init__(
        self, center_x: float = 0, center_y: float = 0, radius: float = 50
    ) -> None:
        self.center = Point(center_x, center_y)
        self.radius = radius

    def draw(
        self,
        painter: QPainter,
        color: QColor | None = None,
        style: Qt.BrushStyle = Qt.BrushStyle.SolidPattern,
        transparency: float = 1,
        outline_thickness: int = 1,
        outline_color: QColor = QColor(0, 0, 0),
        outline_style: Qt.PenStyle = Qt.PenStyle.SolidLine,
    ) -> None:
        painter.save()
        painter.setOpacity(transparency)
        painter.setPen(QPen(outline_color, outline_thickness, outline_style))
        if color:
            painter.setBrush(QBrush(color, style))
        painter.drawEllipse(
            QPointF(self.center.x, self.center.y), self.radius, self.radius
        )
        painter.restore()
