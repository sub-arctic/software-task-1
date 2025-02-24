import math

import physics


def draw_square(x, y, size_x, size_y, mass=5):
    position = physics.Vector2D(x, y)
    velocity = physics.Vector2D(0, 0)
    bbox = physics.Vector2D(size_x, size_y)
    restitution = 0.7

    return physics.RigidBody(
        mass=mass,
        bbox=bbox,
        position=position,
        velocity=velocity,
        restitution=restitution,
    )


def draw_polygon(x, y, side_length, sides, mass=5):
    # S = (n - 2) * 180deg

    circumcircle_radius = side_length / (2 * math.sin(math.pi / sides))

    vertices = []

    for i in range(sides):
        xi = x + circumcircle_radius * math.cos((2 * math.pi * i) / sides)
        yi = y + circumcircle_radius * math.sin((2 * math.pi * i) / sides)

        vertices.append(physics.Vector2D(xi, yi))

    return physics.RigidBody(
        mass=mass, vertices=vertices, position=physics.Vector2D(x, y), restitution=0.7
    )


def draw_velocity_arrows(x, y, velocity):
    x2 = x + velocity.x
    y2 = y - velocity.y

    x_component_line = [x, y, x2, y]
    y_component_line = [x, y, x, y2]

    return x_component_line, y_component_line
