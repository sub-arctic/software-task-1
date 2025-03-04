from typing import Union

from rigidbody import RigidBody
from vec2 import Vec2

Real = Union[int, float]

PENETRATION_SLOP: Real = 0.01
POSITION_BIAS: Real = 0.8


def resolve_collision(
    body_a: RigidBody,
    body_b: RigidBody,
    penetration: Real,
    collision_normal: Vec2,
    contact_point: Vec2,
) -> None:
    inv_mass_a: Real = 1 / body_a.mass if body_a.mass > 0 else 0
    inv_mass_b: Real = 1 / body_b.mass if body_b.mass > 0 else 0
    total_inv_mass: Real = inv_mass_a + inv_mass_b

    if total_inv_mass == 0:
        return

    penetration_error: Real = max(penetration - PENETRATION_SLOP, 0)
    correction: Vec2 = collision_normal * (
        penetration_error * POSITION_BIAS / total_inv_mass
    )
    body_a.position = body_a.position - correction * inv_mass_a
    body_b.position = body_b.position + correction * inv_mass_b

    r_a: Vec2 = contact_point - body_a.position
    r_b: Vec2 = contact_point - body_b.position

    vel_a: Vec2 = body_a.velocity + Vec2(
        -body_a.angular_velocity * r_a.y, body_a.angular_velocity * r_a.x
    )
    vel_b: Vec2 = body_b.velocity + Vec2(
        -body_b.angular_velocity * r_b.y, body_b.angular_velocity * r_b.x
    )
    relative_velocity: Vec2 = vel_b - vel_a

    vel_along_normal: Real = relative_velocity.dot(collision_normal)
    if vel_along_normal > 0:
        return

    restitution: Real = min(body_a.restitution, body_b.restitution)

    r_a_cross_n: Real = r_a.cross(collision_normal)
    r_b_cross_n: Real = r_b.cross(collision_normal)
    inv_inertia_a: Real = (
        1 / body_a.moment_of_inertia if body_a.moment_of_inertia > 0 else 0
    )
    inv_inertia_b: Real = (
        1 / body_b.moment_of_inertia if body_b.moment_of_inertia > 0 else 0
    )

    effective_mass: Real = (
        total_inv_mass
        + (r_a_cross_n**2) * inv_inertia_a
        + (r_b_cross_n**2) * inv_inertia_b
    )

    impulse_scalar: Real = -(1 + restitution) * vel_along_normal / effective_mass
    impulse: Vec2 = collision_normal * impulse_scalar

    body_a.velocity = body_a.velocity - impulse * inv_mass_a
    body_b.velocity = body_b.velocity + impulse * inv_mass_b

    body_a.angular_velocity -= inv_inertia_a * r_a.cross(impulse)
    body_b.angular_velocity += inv_inertia_b * r_b.cross(impulse)
