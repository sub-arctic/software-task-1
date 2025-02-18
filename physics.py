import math
import itertools

# compute the area of a polygon using the shoelace formula
def compute_polygon_area(vertices):
    # loop over each edge and sum up the cross products
    area = 0
    for i, vertex in enumerate(vertices):
        j = (i + 1) % len(vertices)  # wrap index to create a closed polygon
        area += vertex.cross(vertices[j])
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
    for i, vertex in enumerate(vertices):
        j = (i + 1) % n
        cross_val = abs(vertex.cross(vertices[j]))
        sum_val += cross_val * (vertex.dot(vertex) +
                                vertex.dot(vertices[j]) +
                                vertices[j].dot(vertices[j]))
    return (mass * sum_val) / (6 * area)

def calculate_velocity(data_points):
    if len(data_points) < 2:
        return Vector2D(0, 0)

    dp1 = data_points[-2]
    dp2 = data_points[-1]

    dx = dp2.x - dp1.x
    dy = dp2.y - dp1.y

    dt = (dp2.time - dp1.time) / 1_000_000_000

    if dt > 0:
        vx = dx / dt
        vy = dy / dt

        max_velocity = 800
        speed = (vx**2 + vy**2) ** 0.5

        if speed > max_velocity:
            vx = (vx / speed) * max_velocity
            vy = (vy / speed) * max_velocity

        return Vector2D(vx, vy)
    else:
        return Vector2D(0, 0)

class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def __add__(self, other):
        return Vector2D(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        return Vector2D(self._x - other.x, self._y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self._x / scalar, self._y / scalar)

    def dot(self, other):
        return self._x * other.x + self._y * other.y

    def cross(self, other):
        return self._x * other.y - self._y * other.x

    def magnitude(self):
        return math.hypot(self._x, self._y)

    def normalized(self):
        mag = self.magnitude()
        return self / mag if mag else Vector2D(0, 0)

    def rotated(self, angle):
        # rotate by angle using basic trig functions
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return Vector2D(self._x * cos_a - self._y * sin_a,
                        self._x * sin_a + self._y * cos_a)

    def perp(self):
        # get a perpendicular vector
        return Vector2D(-self._y, self._x)

class DataPoint:
    def __init__(self, time, position):
        self.time = time
        self.x = position.x
        self.y = position.y

class DataPointList:
    def __init__(self, max_entries):
        self.max_entries = max_entries
        self.data_points = []

    def __len__(self):
        return len(self.data_points)

    def add_data_point(self, time, position):
        new_point = DataPoint(time, position)
        self.data_points.append(new_point)

        if len(self.data_points) > self.max_entries:
            self.data_points.pop(0)

    def __getitem__(self, index):
        return self.data_points[index]

class PhysicsEngine:
    def __init__(self, gravity=9.81):
        self.rigid_bodies = []
        self.gravity = gravity
        self.next_id = 1

    def add_rigid_body(self, body):
        self.rigid_bodies.append({"id": self.next_id, "body": body})
        self.next_id += 1

    def update_id(self, id, new_id):
        for item in self.rigid_bodies:
            if item.get('id') == id:
                item['id'] = new_id
            return True
        return False

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
        def check_boundary(position, radius, canvas_limit, velocity):
            if position - radius < 0:
                position = radius
                if velocity < 0:
                    velocity = -velocity * body.restitution
            elif position + radius > canvas_limit:
                position = canvas_limit - radius
                if velocity > 0:
                    velocity = -velocity * body.restitution
            return position, velocity

        for item in self.rigid_bodies:
            body = item["body"]
            radius = body.get_bounding_radius()

            body.position.x, body.velocity.x = check_boundary(
                body.position.x, radius, canvas_width, body.velocity.x
            )

            body.position.y, body.velocity.y = check_boundary(
                body.position.y, radius, canvas_height, body.velocity.y
                )

            if body.position.y + radius >= canvas_height:
                body.velocity.x *= (1 - friction_coefficient * dt)

    def get_body_state(self, body_id):
        for item in self.rigid_bodies:
            if item["id"] == body_id:
                return item["body"].get_state()
        return None

    def get_bodies(self):
        return {item["id"]: item["body"].get_corners() for item in self.rigid_bodies}

    def get_body(self, id):
        for item in self.rigid_bodies:
            if item['id'] == id:
                return item['body']

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
        self.constant_force = Vector2D(0, 0)
        self.restitution = restitution
        self.drag_coefficient = 0.1
        
    def move(self, position=None, velocity=None):
        if position is not None:
            self.position = position
        if velocity is not None:
            self.velocity = velocity

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
        for i, _ in enumerate(poly):
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
