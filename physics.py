import math
import itertools

# compute the area of a polygon using the shoelace formula
def compute_polygon_area(vertices):
    # loop over each edge and sum up the cross products
    area = 0
    n = len(vertices)
    for i in range(n):
        j = (i + 1) % n  # wrap index to create a closed polygon
        area += vertices[i].cross(vertices[j])
    return abs(area) / 2

# compute moment of inertia for a uniform polygon relative to its centroid
def compute_polygon_inertia(vertices, mass):
    # formula:
    # i = (mass/(6*area)) * sum(|cross(v_i, v_(i+1))| * (v_i·v_i + v_i·v_(i+1) + v_(i+1)·v_(i+1)))
    area = compute_polygon_area(vertices)
    if area == 0:
        return 0
    n = len(vertices)
    sum_val = 0
    for i in range(n):
        j = (i + 1) % n
        cross_val = abs(vertices[i].cross(vertices[j]))
        sum_val += cross_val * (vertices[i].dot(vertices[i]) +
                                vertices[i].dot(vertices[j]) +
                                vertices[j].dot(vertices[j]))
    return (mass * sum_val) / (6 * area)

class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def magnitude(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        mag = self.magnitude()
        return self / mag if mag else Vector2D(0, 0)

    def rotated(self, angle):
        # rotate by angle using basic trig functions
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return Vector2D(self.x * cos_a - self.y * sin_a,
                        self.x * sin_a + self.y * cos_a)

    def perp(self):
        # get a perpendicular vector
        return Vector2D(-self.y, self.x)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("index out of range for vector2d")

class RigidBody:
    def __init__(self, mass, bbox=None, vertices=None, position=None, velocity=None,
                 angle=0, angular_velocity=0, moment_of_inertia=None, restitution=0.5):
        self.mass = mass
        # if vertices are provided, use them; otherwise, if bbox is provided, use a rectangle
        if vertices is not None:
            self.original_vertices = vertices
            self.bbox = None
        elif bbox is not None:
            self.bbox = bbox
            w, h = bbox
            hw, hh = w / 2, h / 2
            self.original_vertices = [Vector2D(-hw, -hh), Vector2D(hw, -hh),
                                        Vector2D(hw,  hh), Vector2D(-hw, hh)]
        else:
            self.bbox = (50, 50)
            hw, hh = 25, 25
            self.original_vertices = [Vector2D(-hw, -hh), Vector2D(hw, -hh),
                                        Vector2D(hw, hh), Vector2D(-hw, hh)]
        # allow uniform scaling for arbitrary polygons
        self.scale = 1.0
        self.vertices = [v * self.scale for v in self.original_vertices]

        self.position = position if position is not None else Vector2D(0, 0)
        self.velocity = velocity if velocity is not None else Vector2D(0, 0)
        self.angle = angle
        self.angular_velocity = angular_velocity
        if moment_of_inertia is None:
            self.moment_of_inertia = compute_polygon_inertia(self.vertices, mass)
        else:
            self.moment_of_inertia = moment_of_inertia
        self.force = Vector2D(0, 0)
        self.torque = 0
        self.constant_force = Vector2D(0, 0)  # persistent force applied by user
        self.restitution = restitution
        self.drag_coefficient = 0.1  # air resistance coefficient

    def get_corners(self):
        # rotate and translate each vertex
        return [v.rotated(self.angle) + self.position for v in self.vertices]

    def get_bounding_radius(self):
        # compute maximum distance from center
        return max(v.magnitude() for v in self.vertices)

    def apply_force(self, force, point=None):
        self.force = self.force + force
        if point is not None:
            r = point - self.position
            self.torque += r.cross(force)

    def apply_gravity(self, gravity):
        # apply force in the y-direction due to gravity
        self.apply_force(Vector2D(0, self.mass * gravity))

    def update(self, dt):
        # update linear motion
        acceleration = self.force / self.mass
        self.velocity = self.velocity + acceleration * dt
        self.velocity = self.velocity * (1 - self.drag_coefficient * dt)
        self.position = self.position + self.velocity * dt

        # update rotational motion
        angular_acc = self.torque / self.moment_of_inertia
        self.angular_velocity += angular_acc * dt
        self.angular_velocity *= (1 - self.drag_coefficient * dt)
        self.angle += self.angular_velocity * dt

        # reset forces for next step
        self.force = self.constant_force
        self.torque = 0

    def get_state(self):
        return {"position": self.position,
                "velocity": self.velocity,
                "angle": self.angle,
                "angular_velocity": self.angular_velocity}

    def update_moment_of_inertia(self):
        self.moment_of_inertia = compute_polygon_inertia(self.vertices, self.mass)

# --- collision helper functions ---

def project_polygon(axis, points):
    # project each point on axis; return (min, max) dot products
    dots = [p.dot(axis) for p in points]
    return min(dots), max(dots)

def overlap_intervals(min_a, max_a, min_b, max_b):
    # calculate overlap length of two intervals
    return min(max_a, max_b) - max(min_a, min_b)

def sat_collision(body_a, body_b):
    corners_a = body_a.get_corners()
    corners_b = body_b.get_corners()
    axes = []
    # loop over both sets of polygon corners
    for poly in (corners_a, corners_b):
        for i in range(len(poly)):
            edge = poly[(i + 1) % len(poly)] - poly[i]
            axes.append(edge.perp().normalized())
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
            mtv_axis = mtv_axis * -1
    contact_point = (body_a.position + body_b.position) * 0.5
    return True, mtv_axis, mtv_overlap, contact_point, d

def resolve_collision(body_a, body_b, normal, penetration, contact_point):
    total_inv_mass = (1 / body_a.mass) + (1 / body_b.mass)
    if total_inv_mass == 0:
        return
    # move bodies out of collision
    correction = normal * (penetration / total_inv_mass * 0.8)
    body_a.position = body_a.position - correction * (1 / body_a.mass)
    body_b.position = body_b.position + correction * (1 / body_b.mass)
    r_a = contact_point - body_a.position
    r_b = contact_point - body_b.position
    vel_a = body_a.velocity + Vector2D(-body_a.angular_velocity * r_a.y,
                                         body_a.angular_velocity * r_a.x)
    vel_b = body_b.velocity + Vector2D(-body_b.angular_velocity * r_b.y,
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

class PhysicsEngine:
    def __init__(self, gravity=9.81):
        self.rigid_bodies = []
        self.gravity = gravity
        self.next_id = 1

    def add_rigid_body(self, body):
        self.rigid_bodies.append({"id": self.next_id, "body": body})
        self.next_id += 1

    def update(self, dt, canvas_width, canvas_height):
        for item in self.rigid_bodies:
            body = item["body"]
            body.apply_gravity(self.gravity)
            body.update(dt)
        self.resolve_collisions()
        self.enforce_bounds(dt, canvas_width, canvas_height)

    def resolve_collisions(self):
        for a, b in itertools.combinations(self.rigid_bodies, 2):
            body_a = a["body"]
            body_b = b["body"]
            colliding, normal, penetration, contact_point, _ = sat_collision(body_a, body_b)
            if colliding:
                resolve_collision(body_a, body_b, normal, penetration, contact_point)

    def enforce_bounds(self, dt, canvas_width, canvas_height, friction_coefficient=0.2):
        for item in self.rigid_bodies:
            body = item["body"]
            radius = body.get_bounding_radius()
            if body.position.x - radius < 0:
                body.position.x = radius
                if body.velocity.x < 0:
                    body.velocity.x = -body.velocity.x * body.restitution
            if body.position.x + radius > canvas_width:
                body.position.x = canvas_width - radius
                if body.velocity.x > 0:
                    body.velocity.x = -body.velocity.x * body.restitution
            if body.position.y - radius < 0:
                body.position.y = radius
                if body.velocity.y < 0:
                    body.velocity.y = -body.velocity.y * body.restitution
            if body.position.y + radius > canvas_height:
                body.position.y = canvas_height - radius
                if body.velocity.y > 0:
                    body.velocity.y = -body.velocity.y * body.restitution
                body.velocity.x *= (1 - friction_coefficient * dt)

    def get_body_state(self, body_id):
        for item in self.rigid_bodies:
            if item["id"] == body_id:
                return item["body"].get_state()
        return None
    def get_bodies(self):
        return {item["id"]: item["body"].get_corners() for item in self.rigid_bodies}
