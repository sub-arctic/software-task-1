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
