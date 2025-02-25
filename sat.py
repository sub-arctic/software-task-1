import vec2


def project_polygon(axis, corners):
    dots = [corner.dot(axis) for corner in corners]
    return min(dots), max(dots)


def overlap_intervals(min_a, max_a, min_b, max_b):
    return min(max_a, max_b) - max(min_a, min_b)


def sat_collision(body_a, body_b):
    corners_a = body_a.get_vertices()
    corners_b = body_b.get_vertices()
    axes = []

    for poly in (corners_a, corners_b):
        for i in range(len(poly)):
            edge = poly[(i + 1) % len(poly)] - poly[i]
            axes.append(edge.perpendicular().normalized())

    mtv_overlap = float("inf")
    mtv_axis = None

    for axis in axes:
        min_a, max_a = project_polygon(axis, corners_a)
        min_b, max_b = project_polygon(axis, corners_b)
        o = overlap_intervals(min_a, max_a, min_b, max_b)

        if o <= 0:
            return False, None, None, None, None  # no collision

        if o < mtv_overlap:
            mtv_overlap = o
            mtv_axis = axis

    d = body_b.position - body_a.position
    if d.dot(mtv_axis) < 0:
        if mtv_axis is not None:
            mtv_axis = -mtv_axis

    contact_point = (body_a.position + body_b.position) * 0.5
    return True, mtv_axis, mtv_overlap, contact_point, d


def resolve_collision(body_a, body_b, normal, penetration, contact_point):
    total_inv_mass = (1 / body_a.mass) + (1 / body_b.mass)
    if total_inv_mass == 0:
        return

    correction = normal * (penetration / total_inv_mass * 0.8)
    body_a.position -= correction * (1 / body_a.mass)
    body_b.position += correction * (1 / body_b.mass)

    r_a = contact_point - body_a.position
    r_b = contact_point - body_b.position

    vel_a = body_a.velocity + vec2.Vec2(
        -body_a.angular_velocity * r_a.y, body_a.angular_velocity * r_a.x
    )
    vel_b = body_b.velocity + vec2.Vec2(
        -body_b.angular_velocity * r_b.y, body_b.angular_velocity * r_b.x
    )

    rv = vel_b - vel_a
    vel_normal = rv.dot(normal)

    if vel_normal > 0:
        return

    restitution = min(body_a.restitution, body_b.restitution)
    ra_cross_n = r_a.cross(normal)
    rb_cross_n = r_b.cross(normal)
    inv_inertia_a = 1 / body_a.inertia
    inv_inertia_b = 1 / body_b.inertia

    denom = (
        total_inv_mass
        + (ra_cross_n**2) * inv_inertia_a
        + (rb_cross_n**2) * inv_inertia_b
    )
    j = -(1 + restitution) * vel_normal / denom
    impulse = normal * j

    body_a.velocity -= impulse * (1 / body_a.mass)
    body_b.velocity += impulse * (1 / body_b.mass)

    body_a.angular_velocity -= inv_inertia_a * r_a.cross(impulse)
    body_b.angular_velocity += inv_inertia_b * r_b.cross(impulse)
