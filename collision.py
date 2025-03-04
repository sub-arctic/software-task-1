from rigidbody import RigidBody
from vec2 import Vec2

type Real = int | float

def resolve_collision(body_a, body_b, penetration, normal, contact_point):
    total_inv_mass = (1 / body_a.mass) + (1 / body_b.mass)
    if total_inv_mass == 0:
        return
    correction = normal * (penetration / total_inv_mass * 0.8)
    body_a.position = body_a.position - correction * (1 / body_a.mass)
    body_b.position = body_b.position + correction * (1 / body_b.mass)
    r_a = contact_point - body_a.position
    r_b = contact_point - body_b.position
    vel_a = body_a.velocity + Vec2(-body_a.angular_velocity * r_a.y,
                                         body_a.angular_velocity * r_a.x)
    vel_b = body_b.velocity + Vec2(-body_b.angular_velocity * r_b.y,
                                         body_b.angular_velocity * r_b.x)
    rv = vel_b - vel_a
    vel_normal = rv.dot(normal)
    if vel_normal > 0:
        return
    restitution = min(body_a.restitution, body_b.restitution)
    ra_cross_n = r_a.cross(normal)
    rb_cross_n = r_b.cross(normal)
    inv_inertia_a = 1 / body_a.moment_of_inertia
    inv_inertia_b = 1 / body_b.moment_of_inertia
    denom = total_inv_mass + (ra_cross_n ** 2) * inv_inertia_a + (rb_cross_n ** 2) * inv_inertia_b
    j = -(1 + restitution) * vel_normal / denom
    impulse = normal * j
    body_a.velocity = body_a.velocity - impulse * (1 / body_a.mass)
    body_b.velocity = body_b.velocity + impulse * (1 / body_b.mass)
    body_a.angular_velocity -= inv_inertia_a * r_a.cross(impulse)
    body_b.angular_velocity += inv_inertia_b * r_b.cross(impulse)

