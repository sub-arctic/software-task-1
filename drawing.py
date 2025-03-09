import math

from custom_types import Scalar
from vec2 import Vec2, Vec2List


def draw_polygon(side_length: Scalar, sides: int) -> Vec2List:
    circumcircle_radius = side_length / (2 * math.sin(math.pi / sides))
    vertices = Vec2List()
    for i in range(sides):
        xi = circumcircle_radius * math.cos((2 * math.pi * i) / sides)
        yi = circumcircle_radius * math.sin((2 * math.pi * i) / sides)
        vertices.append(Vec2(xi, yi))
    return vertices


def draw_rectangle(width: float, height: float) -> Vec2List:
    vertices = Vec2List()
    vertices.append(Vec2(0, 0))
    vertices.append(Vec2(width, 0))
    vertices.append(Vec2(width, height))
    vertices.append(Vec2(0, height))
    return vertices


def draw_velocity_arrows(
    x: Scalar, y: Scalar, velocity: Vec2
) -> tuple[list[Scalar], list[Scalar]]:
    x2 = x + velocity.x
    y2 = y - velocity.y
    x_component_line = [x, y, x2, y]
    y_component_line = [x, y, x, y2]
    return x_component_line, y_component_line
