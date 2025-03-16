from custom_types import CollisionResult, Scalar
from rigidbody import RigidBody
from vec2 import Vec2, Vec2List


def project_polygon(axis: Vec2, corners: Vec2List) -> tuple[Scalar, Scalar]:
    dots = [corner.dot(axis) for corner in corners]
    return min(dots), max(dots)


def overlap_intervals(
    min_a: Scalar, max_a: Scalar, min_b: Scalar, max_b: Scalar
) -> Scalar:
    return min(max_a, max_b) - max(min_a, min_b)


def find_contact_points(a: Vec2List, b: Vec2List, normal: Vec2) -> Vec2List:
    min_a = min(a, key=lambda v: v.dot(-normal))
    min_b = min(b, key=lambda v: v.dot(normal))

    contacts = Vec2List()

    if min_a == min_bb:
        contacts.append(min_a)
    else:
        contacts.append(min_a)
        contacts.append(min_b)

    return contacts


def sat(a: RigidBody, b: RigidBody) -> CollisionResult:
    body_a = a.get_vertices()
    body_b = b.get_vertices()
    axes: Vec2List = Vec2List()
    penetration = float("inf")
    normal = Vec2()
    contact_points = Vec2List()

    for poly in (body_a, body_b):
        for i in range(len(poly)):
            edge = poly[(i + 1) % len(poly)] - poly[i]
            axes.append(edge.perpendicular().normalized())

    if not axes:
        return CollisionResult(False)

    for axis in axes:
        min_a, max_a = project_polygon(axis, body_a)
        min_b, max_b = project_polygon(axis, body_b)
        offset: Scalar = overlap_intervals(min_a, max_a, min_b, max_b)

        if offset <= 0:
            return CollisionResult(False)

        if offset < penetration:
            penetration = offset
            normal = axis

    d = b.position - a.position
    if d.dot(normal) < 0:
        normal = -normal

    contact_points = find_contact_points(body_a, body_b, normal)

    return CollisionResult(True, penetration, normal, contact_points)
