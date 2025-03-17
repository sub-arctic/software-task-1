from custom_types import CollisionResult
from sat import sat


def safe_inverse(value):
    return 0 if value == 0 else 1 / value


# interface, could interchange for gjk in future
def handle_collision(body_a, body_b, method="sat"):
    """Handles the collision between two bodies using the specified method.

    This function checks for a collision between two rigid bodies (`body_a` and `body_b`)
    using the specified collision detection method. Currently, it supports the
    Separating Axis Theorem (SAT). If a collision is detected, it resolves the collision
    by calling the appropriate resolution function.

    Args:
        body_a: The first rigid body involved in the collision.
        body_b: The second rigid body involved in the collision.
        method (str, optional): The method to use for collision detection.
                                Defaults to "sat".

    Returns:
        None: The function does not return a value. It resolves the collision
              if one is detected.
    """
    if method == "sat":
        result: CollisionResult = sat(body_a, body_b)
    else:
        return
    if result is not False:
        resolve_collision(body_a, body_b, result)


def resolve_collision(body_a, body_b, result: CollisionResult):
    """Resolves the collision between two rigid bodies based on the collision result.

    This function applies impulse-based resolution to two rigid bodies (`body_a` and `body_b`)
    based on the collision information provided in the `result`. It updates the velocities and
    positions of the bodies to reflect the collision response, taking into account restitution
    and the physical properties of the bodies.

    Args:
        body_a: The first rigid body involved in the collision.
        body_b: The second rigid body involved in the collision.
        result (CollisionResult): An object containing the collision result, including
                                  contact points, penetration depth, and collision normal.

    Returns:
        None: The function modifies the state of the bodies directly and does not return a value.
    """
    contacts = result.contacts
    penetration = result.penetration
    normal = result.normal

    if not contacts:
        return

    restitution = min(body_a.restitution, body_b.restitution)

    inv_mass_a = safe_inverse(body_a.mass)
    inv_mass_b = safe_inverse(body_b.mass)
    inv_inertia_a = safe_inverse(body_a.moment_of_inertia)
    inv_inertia_b = safe_inverse(body_b.moment_of_inertia)

    for contact in contacts:
        r_a = contact - body_a.position
        r_b = contact - body_b.position

        relative_velocity = (
            body_b.velocity + r_b.perpendicular() * body_b.angular_velocity
        ) - (body_a.velocity + r_a.perpendicular() * body_a.angular_velocity)
        vel_along_normal = relative_velocity.dot(normal)

        if vel_along_normal > 0:
            continue

        ra_cross_n = r_a.cross(normal)
        rb_cross_n = r_b.cross(normal)
        denom = (
            inv_mass_a
            + inv_mass_b
            + (ra_cross_n**2) * inv_inertia_a
            + (rb_cross_n**2) * inv_inertia_b
        )

        if denom == 0:
            continue

        j = -(1 + restitution) * vel_along_normal
        j /= denom
        j /= len(contacts)

        impulse = normal * j

        if not body_a.pinned:
            body_a.velocity -= impulse * inv_mass_a
            body_a.angular_velocity -= ra_cross_n * j * inv_inertia_a

        if not body_b.pinned:
            body_b.velocity += impulse * inv_mass_b
            body_b.angular_velocity += rb_cross_n * j * inv_inertia_b

    PERCENT = 0.8
    SLOP = 0.01
    if penetration is None or normal is None:
        return
    if penetration > SLOP:
        correction = normal * (penetration * PERCENT / (inv_mass_a + inv_mass_b))
        if not body_a.pinned:
            body_a.position -= correction * inv_mass_a
        if not body_b.pinned:
            body_b.position += correction * inv_mass_b
