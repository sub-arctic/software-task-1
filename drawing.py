import math

from rigidbody import RigidBody
from vec2 import Vec2

type Real = int | float

def draw_polygon(x: Real, y: Real, side_length: Real, sides: int) -> RigidBody:
    circumcircle_radius = side_length / (2 * math.sin(math.pi / sides))
    vertices = []
    for i in range(sides):
        xi = x + circumcircle_radius * math.cos((2 * math.pi * i) / sides)
        yi = y + circumcircle_radius * math.sin((2 * math.pi * i) / sides)
        vertices.append(Vec2(xi, yi))
    return RigidBody(
        vertices=vertices,
        position=Vec2(x, y),
        velocity=Vec2(),
        constant_force=Vec2(),
    )


def draw_velocity_arrows(x: Real, y: Real, velocity: Vec2) -> tuple[list[Real], list[Real]]:
    x2 = x + velocity.x
    y2 = y - velocity.y
    x_component_line = [x, y, x2, y]
    y_component_line = [x, y, x, y2]
    return x_component_line, y_component_line
