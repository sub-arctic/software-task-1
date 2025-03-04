from rigidbody import RigidBody
from vec2 import Vec2, Vec2List

type Real = int | float

def project_polygon(axis: Vec2, corners: Vec2List) -> tuple[Real, Real]:
    dots = [corner.dot(axis) for corner in corners]
    return min(dots), max(dots)

def overlap_intervals(min_a: Real, max_a: Real, min_b: Real, max_b: Real) -> Real:
    return min(max_a, max_b) - max(min_a, min_b)

def is_colliding(a: RigidBody, b: RigidBody) -> tuple[bool, Real, Vec2 | None, Vec2]:
    body_a = a.get_vertices()
    body_b = b.get_vertices()
    axes: Vec2List = Vec2List()
    min_penetration = float('inf')
    collision_normal = None

    for poly in (body_a, body_b):
        poly_len = len(poly)
        for i, vector in enumerate(poly):
            edge: Vec2 = poly[(i + 1) % poly_len] - vector
            if edge.length() == 0:
                continue
            axes.append(edge.perpendicular().normalized())

    if not axes:
        return False, 0, Vec2(), Vec2()

    for axis in axes:
        min_a, max_a = project_polygon(axis, body_a)
        min_b, max_b = project_polygon(axis, body_b)
        offset: Real = overlap_intervals(min_a, max_a, min_b, max_b)

        if offset < 0:
            return False, 0, Vec2(), Vec2()

        if offset < min_penetration:
            min_penetration = offset
            collision_normal = axis

    contact_point = (a.position + b.position) * 0.5

    return True, min_penetration, collision_normal, contact_point

