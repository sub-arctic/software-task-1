from custom_types import CollisionResult
from sat import sat
from rigidbody import RigidBody
from vec2 import Vec2, Vec2List
from custom_types import Scalar


# Prevent excessive overlap.
SLOP = 0.8
THRESHOLD = 0.01

def safe_inverse(value: Scalar):
    """Calculate the safe inverse of a given numeric value."""
    return 0 if value == 0 else 1 / value


def handle_collision(body_a: RigidBody, body_b: RigidBody, method="sat") -> CollisionResult | None:
    """Interface for managing the collision between two bodies using the specified method.

    This function checks for a collision between two rigid bodies (`body_a` and `body_b`)
    using the specified collision detection method. Currently, it supports the
    Separating Axis Theorem (SAT), GJK was too hard to implement. If a collision is detected, 
    it resolves the collision by calling the appropriate resolution function.

    Args:
        body_a: The first rigid body involved in the collision.
        body_b: The second rigid body involved in the collision.
        method (str, optional): The method to use for collision detection.
                                Defaults to "sat".
    """
    if method == "sat":
        result: CollisionResult = sat(body_a, body_b)
    else:
        return None
    if result is not False:
        resolve_collision(body_a, body_b, result)


def resolve_collision(body_a: RigidBody, body_b: RigidBody, result: CollisionResult) -> None:
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
    """
    contacts: Vec2List | None = result.contacts
    penetration: Scalar | None = result.penetration
    collision_normal: Vec2 | None = result.normal

    if not contacts or not collision_normal or not penetration:
        return

    restitution: Scalar = min(body_a.restitution, body_b.restitution)

    # We calculate inverse as impulses are based on *change* in velocity.
    # Specifically, a body's impulse is directly proportional to the change in velocity.
    # An impulse is force applied over time, and in this context it is the required change
    # in velocity for bodies to resolve their collisions.
    inv_mass_a: Scalar = safe_inverse(body_a.mass)
    inv_mass_b: Scalar = safe_inverse(body_b.mass)
    inv_inertia_a: Scalar = safe_inverse(body_a.moment_of_inertia)
    inv_inertia_b: Scalar = safe_inverse(body_b.moment_of_inertia)

    for contact_point in contacts:
        a_to_contact: Vec2 = contact_point - body_a.position
        b_to_contact: Vec2 = contact_point - body_b.position

        # Determines how fast bodies are moving proportional to one another.
        relative_velocity: Vec2 = (
            body_b.velocity + b_to_contact.perpendicular() * body_b.angular_velocity
        ) - (body_a.velocity + a_to_contact.perpendicular() * body_a.angular_velocity)
        
        velocity_along_normal: Scalar = relative_velocity.dot(collision_normal)

        if velocity_along_normal > 0:
            continue

        ra_cross_n: Scalar = a_to_contact.cross(collision_normal)
        rb_cross_n: Scalar = b_to_contact.cross(collision_normal)
        
        # The denominator is calculated to determine if the impulse is proportional
        # to the combined mass and inertia of both bodies.
        denominator: Scalar = (
            inv_mass_a
            + inv_mass_b
            + (ra_cross_n**2) * inv_inertia_a
            + (rb_cross_n**2) * inv_inertia_b
        )

        # No impulse can be applied.
        if denominator == 0:
            continue

        impulse: Scalar = -(1 + restitution) * velocity_along_normal
        impulse: Scalar = impulse / denominator
        impulse: Scalar = impulse / len(contacts)

        impulse_vector: Vec2 = collision_normal * impulse

        if not body_a.pinned:
            body_a.velocity -= impulse_vector * inv_mass_a
            body_a.angular_velocity -= ra_cross_n * impulse * inv_inertia_a

        if not body_b.pinned:
            body_b.velocity += impulse_vector * inv_mass_b
            body_b.angular_velocity += rb_cross_n * impulse * inv_inertia_b


    # Ensure there is minimal overlap between bodies due to time steps.
    if penetration > THRESHOLD:
        total_inv_mass: Scalar = inv_mass_a + inv_mass_b
        penetration_correction: Scalar = penetration * SLOP / total_inv_mass
        correction_vector = collision_normal * (
            penetration * SLOP / (inv_mass_a + inv_mass_b)
        )
        
        if not body_a.pinned:
            body_a.position -= correction_vector * inv_mass_a
        if not body_b.pinned:
            body_b.position += correction_vector * inv_mass_b

