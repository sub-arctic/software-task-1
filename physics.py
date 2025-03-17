import vec2


def compute_polygon_inertia(vertices, mass):
    """Calculates the moment of inertia of a polygon defined by its vertices.

    The moment of inertia is calculated using the formula that incorporates the
    area of the polygon and the vertices' positions. The function assumes that
    the polygon is defined in a 2D space and that the vertices are provided in
    a counter-clockwise order.

    Args:
        vertices (list[vec2.Vec2]): A list of Vec2 objects representing the
                                      vertices of the polygon.
        mass (float): The mass of the polygon.

    Returns:
        float: The moment of inertia of the polygon. Returns 0 if the area of
               the polygon is zero (i.e., the polygon is degenerate).
    """
    area = compute_polygon_area(vertices)
    if area == 0:
        return 0
    n = len(vertices)
    sum_val = 0
    for i, vertex in enumerate(vertices):
        j = (i + 1) % n
        cross_val = abs(vertex.cross(vertices[j]))
        sum_val += cross_val * (
            vertex.dot(vertex) + vertex.dot(vertices[j]) + vertices[j].dot(vertices[j])
        )
    return (mass * sum_val) / (6 * area)


def compute_polygon_area(vertices):
    """Calculates the area of a polygon defined by its vertices.

    The area is computed using the shoelace formula, which sums the cross products
    of the vertices. The function assumes that the vertices are provided in a
    counter-clockwise order.

    Args:
        vertices (list[vec2.Vec2]): A list of Vec2 objects representing the
                                      vertices of the polygon.

    Returns:
        float: The area of the polygon. Returns 0 if the polygon is degenerate.
    """
    area = 0
    for i, vertex in enumerate(vertices):
        j = (i + 1) % len(vertices)
        area += vertex.cross(vertices[j])
    return abs(area) / 2


def calculate_velocity(data_points):
    """Calculates the velocity based on a list of data points.

    The function computes the velocity vector based on the last two data points
    in the list. It calculates the change in position over the change in time.
    If the calculated speed exceeds a maximum threshold, it normalizes the velocity.

    Args:
        data_points (list[vec2.Vec2]): A list of Vec2 objects, each containing
                                         position and time information.

    Returns:
        vec2.Vec2: A Vec2 object representing the calculated velocity. Returns
                    a zero vector if there are fewer than two data points or if
                    the time difference is non-positive.
    """
    if len(data_points) < 2:
        return vec2.Vec2(0, 0)

    dp1 = data_points[-2]
    dp2 = data_points[-1]

    dx = dp2.x - dp1.x
    dy = dp2.y - dp1.y

    dt = (dp2.time - dp1.time) / 1_000_000_000

    if dt > 0:
        vx = dx / dt
        vy = dy / dt

        max_velocity = 100
        speed = (vx**2 + vy**2) ** 0.5

        if speed > max_velocity:
            vx = (vx / speed) * max_velocity
            vy = (vy / speed) * max_velocity

        return vec2.Vec2(vx, vy)
    else:
        return vec2.Vec2(0, 0)
