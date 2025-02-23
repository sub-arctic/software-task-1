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


def draw_velocity_arrows(x, y, velocity):
    x2 = x + velocity.x
    y2 = y - velocity.y

    x_component_line = [x, y, x2, y]
    y_component_line = [x, y, x, y2]

    return x_component_line, y_component_line
