import math

import vec2


class RigidBody:
    def __init__(self, vertices, position, velocity, constant_force):
        self.vertices = vertices
        self.position = position
        self.velocity = velocity
        self.mass = 5
        self.angle = 90
        self.angular_velocity = 0
        self.inertia = 1
        self.force = constant_force
        self.torque = 0
        self.constant_force = constant_force
        self.restitution = 0.5
        self.update_vertices()

    def __getitem__(self, index):
        return self.vertices[index]

    def rotate(self, angle):
        self._angle = angle
        self.update_vertices()

    def move(self, delta):
        self.position = delta
        # self.update_vertices()

    def velocity(self, velocity):
        self.velocity = velocity
        # self.update_vertices()

    def apply_force(self, force, point=None):
        self.force = self.force + force
        if point is not None:
            r = point - self.position
            self.torque += r.cross(force)

    def rotate_vertices(self):
        angle_radians = math.radians(self.angle)

        cx = sum(x for x, y in self.vertices) / len(self.vertices)
        cy = sum(y for y, y in self.vertices) / len(self.vertices)

        rotated_vertices = []

        for x, y in self.vertices:
            x_translated = x - cx
            y_translated = y - cy

            x_rotated = (
                x_translated * math.cos(angle_radians)
                - y_translated * math.sin(angle_radians)
            ) + cx
            y_rotated = (
                x_translated * math.sin(angle_radians)
                + y_translated * math.cos(angle_radians)
            ) + cy

            rotated_vertices.append(vec2.Vec2(x_rotated, y_rotated))

        return rotated_vertices

    def update_vertices(self):
        self.transformed_vertices = []
        self.rotated_vertices = self.rotate_vertices()
        for vertex in self.rotated_vertices:
            new_vertex = vertex + self.position
            self.transformed_vertices.append(new_vertex)

    def update(self, delta_time, gravity=9.8):
        acceleration = self.force / self.mass
        self.velocity = self.velocity + acceleration * delta_time
        self.velocity = self.velocity + vec2.Vec2(0, gravity) * delta_time
        self.position = self.position + self.velocity * delta_time

        angular_acc = self.torque / self.inertia
        self.angular_velocity += angular_acc * delta_time
        self.angle += self.angular_velocity * delta_time

        self.update_vertices()

        self.force = self.constant_force
        self.torque = 0

    def get_vertices(self, unpacked=False):
        if unpacked:
            vertices = []
            for vertex in self.transformed_vertices:
                vertices.extend([vertex.x, vertex.y])
            return vertices
        return self.transformed_vertices

    def get_state(self):
        return {
            "position": self.position,
            "velocity": self.velocity,
            "angle": self.angle,
            "mass": self.mass,
            "force": self.force,
            "restitution": self.restitution,
        }
