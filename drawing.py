import math

import rigidbody
import vec2


def draw_polygon(x, y, side_length, sides, mass=5):
    circumcircle_radius = side_length / (2 * math.sin(math.pi / sides))
    vertices = []
    for i in range(sides):
        xi = x + circumcircle_radius * math.cos((2 * math.pi * i) / sides)
        yi = y + circumcircle_radius * math.sin((2 * math.pi * i) / sides)
        vertices.append(vec2.Vec2(xi, yi))
    return rigidbody.RigidBody(
        vertices=vertices,
        position=vec2.Vec2(x, y),
        velocity=vec2.Vec2(),
        constant_force=vec2.Vec2(),
    )


def draw_velocity_arrows(x, y, velocity):
    x2 = x + velocity.x
    y2 = y - velocity.y
    x_component_line = [x, y, x2, y]
    y_component_line = [x, y, x, y2]
    return x_component_line, y_component_line
