import vec2


def support(shape_a, shape_b, direction):
    point_a = max(shape_a, key=lambda v: v.dot(direction))
    point_b = max(shape_b, key=lambda v: v.dot(direction))
    return point_a - point_b


def triple_cross(a, b, c):
    return b * a.dot(c) - a * b.dot(c)


def gjk(shape_a, shape_b):
    direction = vec2.Vec2(1, 0)
    simplex = [support(shape_a, shape_b, direction)]
    direction = -simplex[0]
    while True:
        point = support(shape_a, shape_b, direction)
        if point.dot(direction) < 0:
            return False, None, None, None
        simplex.append(point)
        if handle_simplex(simplex, direction):
            contact_point, contact_normal, penetration_depth = get_contact_info(
                simplex, shape_b
            )
            return True, contact_point, contact_normal, penetration_depth


def handle_simplex(simplex, direction):
    if len(simplex) == 2:
        return handle_line(simplex, direction)
    elif len(simplex) == 3:
        return handle_triangle(simplex, direction)
    return False


def handle_line(simplex, direction):
    a = simplex[-1]
    b = simplex[-2]
    ao = -a
    ab = b - a
    if ab.dot(ao) > 0:
        new_direction = triple_cross(ab, ao, ab)
        if new_direction.magnitude() == 0:
            new_direction = ab.perpendicular()
        direction.x = new_direction.x
        direction.y = new_direction.y
    else:
        simplex[:] = [a]
        direction.x = ao.x
        direction.y = ao.y
    return False


def handle_triangle(simplex, direction):
    a = simplex[-1]
    b = simplex[-2]
    c = simplex[-3]
    ao = -a
    ab = b - a
    ac = c - a
    ab_perp = triple_cross(ac, ab, ab)
    ac_perp = triple_cross(ab, ac, ac)
    if ab_perp.dot(ao) > 0:
        simplex.pop(-3)
        direction.x = ab_perp.x
        direction.y = ab_perp.y
        return False
    elif ac_perp.dot(ao) > 0:
        simplex.pop(-2)
        direction.x = ac_perp.x
        direction.y = ac_perp.y
        return False
    else:
        return True


def get_contact_info(simplex, shape_b):
    contact_point = simplex[-1]
    contact_normal = contact_point.normalized()
    penetration_depth = float("inf")
    for vertex in shape_b:
        distance = (contact_point - vertex).dot(contact_normal)
        penetration_depth = min(penetration_depth, distance)
    penetration_depth = abs(penetration_depth)
    return contact_point, contact_normal, penetration_depth


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
