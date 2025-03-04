from rigidbody import RigidBody
from vec2 import Vec2, Vec2List

type Real = int | float
type Irrational = float


def project_polygon(axis: Vec2, corners: Vec2List) -> tuple[Real, Real]:
    dots = [corner.dot(axis) for corner in corners]
    return min(dots), max(dots)


def overlap_intervals(min_a: Real, max_a: Real, min_b: Real, max_b: Real) -> Real:
    return min(max_a, max_b) - max(min_a, min_b)


def sat_collision(body_a: RigidBody, body_b: RigidBody) -> tuple[bool, Vec2 | None, Real | None, Vec2 | None, Vec2 | None]:
    corners_a: Vec2List = body_a.vertices
    corners_b: Vec2List = body_b.vertices
    axes: Vec2List = Vec2List()

    for poly in (corners_a, corners_b):
        poly_len = len(poly)
        for i, vector in enumerate(poly):
            edge: Vec2 = poly[(i + 1) % poly_len] - vector
            axes.append(edge.perpendicular().normalized())

    mtv_overlap: Irrational = float("inf")
    mtv_axis = None

    for axis in axes:
        min_a, max_a = project_polygon(axis, corners_a)
        min_b, max_b = project_polygon(axis, corners_b)
        o: Real = overlap_intervals(min_a, max_a, min_b, max_b)

        if o <= 0:
            return False, None, None, None, None

        if o < mtv_overlap:
            mtv_overlap = o
            mtv_axis = axis

    d: Vec2 = body_b.position - body_a.position
    if mtv_axis is not None:
        if d.dot(mtv_axis) < 0:
            mtv_axis = -mtv_axis

    contact_point: Vec2 = (body_a.position + body_b.position) * 0.5
    return True, mtv_axis, mtv_overlap, contact_point, d


def resolve_collision(body_a: RigidBody, body_b: RigidBody, normal: Vec2, penetration: Real, contact_point: Vec2) -> None:
    total_inv_mass: Real = (1 / body_a.mass) + (1 / body_b.mass)
    if total_inv_mass == 0:
        return

    correction: Vec2 = normal * (penetration / total_inv_mass * 0.8)
    body_a.position -= correction * (1 / body_a.mass)
    body_b.position += correction * (1 / body_b.mass)

    r_a: Vec2 = contact_point - body_a.position
    r_b: Vec2 = contact_point - body_b.position

    vel_a: Vec2 = body_a.velocity + Vec2(
        -body_a.angular_velocity * r_a.y, body_a.angular_velocity * r_a.x
    )
    vel_b: Vec2 = body_b.velocity + Vec2(
        -body_b.angular_velocity * r_b.y, body_b.angular_velocity * r_b.x
    )

    rv: Vec2 = vel_b - vel_a
    vel_normal: Real = rv.dot(normal)

    if vel_normal > 0:
        return

    restitution: Real = min(body_a.restitution, body_b.restitution)
    ra_cross_n: Real = r_a.cross(normal)
    rb_cross_n: Real = r_b.cross(normal)
    inv_inertia_a: Real = 1 / body_a.inertia
    inv_inertia_b: Real = 1 / body_b.inertia

    denom: Real = (
        total_inv_mass
        + (ra_cross_n**2) * inv_inertia_a
        + (rb_cross_n**2) * inv_inertia_b
    )
    j: Real = -(1 + restitution) * vel_normal / denom
    impulse: Vec2 = normal * j

    body_a.velocity -= impulse * (1 / body_a.mass)
    body_b.velocity += impulse * (1 / body_b.mass)

    body_a.angular_velocity -= inv_inertia_a * r_a.cross(impulse)
    body_b.angular_velocity += inv_inertia_b * r_b.cross(impulse)
