import math
import itertools

class Vector2D:
    def __init__(self, x=0, y=0):
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
        if mag:
            return self / mag
        return Vector2D(0, 0)

    def rotated(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2D(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def perp(self):
        return Vector2D(-self.y, self.x)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Index out of range for Vector2D")

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

## TODO:
## Implement arbitrary bbox calculations for complex polygons
class RigidBody:
    def __init__(
        self,
        mass,
        bbox,
        position=None,
        velocity=None,
        angle=0,
        angular_velocity=0,
        moment_of_inertia=None,
        restitution=0.5
    ):
        self.mass = mass
        self.bbox = bbox
        self.position = position if position is not None else Vector2D(0, 0)
        self.velocity = velocity if velocity is not None else Vector2D(0, 0)
        self.angle = angle
        self.angular_velocity = angular_velocity
        if moment_of_inertia is None:
            self.moment_of_inertia = mass * (bbox[0] ** 2 + bbox[1] ** 2) / 12
        else:
            self.moment_of_inertia = moment_of_inertia
        self.force = Vector2D(0, 0)
        self.torque = 0
        self.restitution = restitution

    def apply_force(self, force, point=None):
        self.force = self.force + force
        if point is not None:
            r = point - self.position
            self.torque += r.cross(force)

    def apply_gravity(self, gravity):
        self.apply_force(Vector2D(0, self.mass * gravity))

    def update(self, dt):
        acceleration = self.force / self.mass
        self.velocity = self.velocity + acceleration * dt
        self.position = self.position + self.velocity * dt
        angular_acceleration = self.torque / self.moment_of_inertia
        self.angular_velocity += angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        self.force = Vector2D(0, 0)
        self.torque = 0

    def get_state(self):
        return {
            "position": self.position,
            "velocity": self.velocity,
            "angle": self.angle,
            "angular_velocity": self.angular_velocity,
        }

    def get_corners(self):
        w, h = self.bbox
        hw = w / 2
        hh = h / 2
        corners = [
            Vector2D(-hw, -hh),
            Vector2D(hw, -hh),
            Vector2D(hw, hh),
            Vector2D(-hw, hh)
        ]
        return [corner.rotated(self.angle) + self.position for corner in corners]

def project_polygon(axis, points):
    dots = [point.dot(axis) for point in points]
    return min(dots), max(dots)

def overlap_intervals(min_a, max_a, min_b, max_b):
    return min(max_a, max_b) - max(min_a, min_b)

def sat_collision(body_a, body_b):
    corners_a = body_a.get_corners()
    corners_b = body_b.get_corners()
    axes = []
    for i, corner in enumerate(corners_a):
        next_corner = corners_a[(i + 1) % len(corners_a)]
        edge = next_corner - corner
        axes.append(edge.perp().normalized())
    for i, corner in enumerate(corners_b):
        next_corner = corners_b[(i + 1) % len(corners_b)]
        edge = next_corner - corner
        axes.append(edge.perp().normalized())
    mtv_overlap = float("inf")
    mtv_axis = None
    for axis in axes:
        min_a, max_a = project_polygon(axis, corners_a)
        min_b, max_b = project_polygon(axis, corners_b)
        o = overlap_intervals(min_a, max_a, min_b, max_b)
        if o <= 0:
            return False, None, None, None, None
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
    correction = normal * (penetration / total_inv_mass * 0.8)
    body_a.position = body_a.position - correction * (1 / body_a.mass)
    body_b.position = body_b.position + correction * (1 / body_b.mass)
    r_a = contact_point - body_a.position
    r_b = contact_point - body_b.position
    vel_a = body_a.velocity + Vector2D(-body_a.angular_velocity * r_a.y, body_a.angular_velocity * r_a.x)
    vel_b = body_b.velocity + Vector2D(-body_b.angular_velocity * r_b.y, body_b.angular_velocity * r_b.x)
    rv = vel_b - vel_a
    vel_along_normal = rv.dot(normal)
    if vel_along_normal > 0:
        return
    restitution = min(body_a.restitution, body_b.restitution)
    ra_cross_n = r_a.cross(normal)
    rb_cross_n = r_b.cross(normal)
    inv_inertia_a = 1 / body_a.moment_of_inertia
    inv_inertia_b = 1 / body_b.moment_of_inertia
    denom = total_inv_mass + (ra_cross_n ** 2) * inv_inertia_a + (rb_cross_n ** 2) * inv_inertia_b
    j = -(1 + restitution) * vel_along_normal / denom
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

    def update(self, dt):
        for item in self.rigid_bodies:
            body = item["body"]
            body.apply_gravity(self.gravity)
            body.update(dt)
        self.resolve_collisions()

    def resolve_collisions(self):
        for item_a, item_b in itertools.combinations(self.rigid_bodies, 2):
            body_a = item_a["body"]
            body_b = item_b["body"]
            colliding, normal, penetration, contact_point, _ = sat_collision(body_a, body_b)
            if colliding:
                resolve_collision(body_a, body_b, normal, penetration, contact_point)

    def get_body_state(self, body_id):
        for item in self.rigid_bodies:
            if item["id"] == body_id:
                return item["body"].get_state()
        return None

    def get_all_states(self):
        return {item["id"]: item["body"].get_state() for item in self.rigid_bodies}

