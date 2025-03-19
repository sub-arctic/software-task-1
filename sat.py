from custom_types import CollisionResult, Scalar
from rigidbody import RigidBody
from vec2 import Vec2, Vec2List


def project_polygon(axis: Vec2, corners: Vec2List) -> tuple[Scalar, Scalar]:
    """Projects a polygon onto a given axis and returns the minimum and maximum
    scalar values of the projection.

    Args:
        axis: A vector representing the axis onto which the polygon
                     will be projected.
        corners: A list of 2D vectors representing the corners of
                            the polygon.

    Returns:
        tuple[Scalar, Scalar]: A tuple containing the minimum and maximum
                               scalar values of the projection of the polygon
                               onto the specified axis.
    """
    dots = [corner.dot(axis) for corner in corners]
    return min(dots), max(dots)


def overlap_intervals(
    min_a: Scalar, max_a: Scalar, min_b: Scalar, max_b: Scalar
) -> Scalar:
    """Calculates the overlap length between two intervals.

    This function takes the minimum and maximum values of two intervals
    and returns the length of their overlap. If the intervals do not
    overlap, the function will return a negative value.

    Args:
        min_a: The minimum value of the first interval.
        max_a: The maximum value of the first interval.
        min_b: The minimum value of the second interval.
        max_b: The maximum value of the second interval.

    Returns:
        The length of the overlap between the two intervals.
                 If there is no overlap, the result will be negative.
    """
    return min(max_a, max_b) - max(min_a, min_b)


def find_contact_points(a: Vec2List, b: Vec2List, normal: Vec2) -> Vec2List:
    """Finds the contact points between two sets of 2D vectors based on a given normal vector.

    This function identifies the closest points between two shapes represented by
    lists of vectors (`a` and `b`) along a specified normal direction. If the
    closest points are the same, only one contact point is returned; otherwise, both
    contact points are returned.

    Args:
        a: A list of vectors representing the first shape.
        b: A list of vectors representing the second shape.
        normal: A vector representing the normal direction for the contact
                       point calculation.

    Returns:
        Vec2List: A list of vectors representing the contact points between the
                   two shapes. The list may contain one or two contact points.
    """
    min_a = min(a, key=lambda v: v.dot(-normal))
    min_b = min(b, key=lambda v: v.dot(normal))

    contacts = Vec2List()

    if min_a == min_b:
        contacts.append(min_a)
    else:
        contacts.append(min_a)
        contacts.append(min_b)

    return contacts


def sat(a: RigidBody, b: RigidBody) -> CollisionResult:
    """Performs the Separating Axis Theorem (SAT) test to determine
    if two rigid bodies are colliding.

    Also known as the hyperplane seperation theorem:
    https://en.wikipedia.org/wiki/Hyperplane_separation_theorem

    This function checks for collisions between two rigid
    bodies by projecting their vertices onto potential
    separating axes derived from their edges. If a collision
    is detected, it calculates the penetration depth, the
    collision normal, and the contact points.

    Args:
        a: The first rigid body to test for collision.
        b: The second rigid body to test for collision.

    Returns:
        An object containing the result of the
            collision test. If a collision occurs,
            it includes the penetration depth, the
            collision normal, and the contact points;
            otherwise, it indicates no collision.
    """
    body_a = a.get_vertices()
    body_b = b.get_vertices()
    axes: Vec2List = Vec2List()
    penetration: float = float("inf") # Arbitrary upper bound for searching.
    normal = Vec2()
    contact_points = Vec2List()

    # Find all axes to check seperation on.
    for poly in (body_a, body_b):
        for i in range(len(poly)):
            edge = poly[(i + 1) % len(poly)] - poly[i]
            axes.append(edge.perpendicular().normalized())

    if not axes:
        return CollisionResult(False)

    for axis in axes:
        # We project the polygon on the axis. The minimum and maximum
        # of each respective body is the minimum and maximum vector,
        # representing the vertex at that position.
        min_a, max_a = project_polygon(axis, body_a)
        min_b, max_b = project_polygon(axis, body_b)

        # We overlap the minimum and maximum values of both bodies to
        # get the offset, or translation vector. This is the overlap
        # distance between both bodies. Negative values indicate that
        # there is seperation between the bodies, and vice-versa.
        offset: Scalar = overlap_intervals(min_a, max_a, min_b, max_b)

        if offset <= 0:
            return CollisionResult(False)

        if offset < penetration:
            penetration = offset
            normal = axis

    d = b.position - a.position
    # Reverse the normal direction if it points away from the other body.
    if d.dot(normal) < 0:
        normal = -normal

    contact_points = find_contact_points(body_a, body_b, normal)

    return CollisionResult(True, penetration, normal, contact_points)
