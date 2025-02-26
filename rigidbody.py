import math
from typing import Any

from vec2 import Vec2

type Vec2List = list[Vec2]
type Real = int | float


class RigidBody:
    def __init__(
        self, vertices: Vec2List, position: Vec2, velocity: Vec2, constant_force: Vec2
    ):
        self._vertices: Vec2List = vertices
        self._position: Vec2 = position
        self._velocity: Vec2 = velocity
        self.angle: Real = 90
        self.mass: Real = 5
        self.angular_velocity: Real = 0
        self.inertia: Real = 1
        self.force: Vec2 = constant_force
        self.torque: Real = 1
        self.constant_force: Vec2 = constant_force
        self.restitution: Real = 0.5
        self.update_vertices()

    @property
    def velocity(self) -> Vec2:
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity: Vec2):
        self._velocity = new_velocity

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, new_position: Vec2):
        self._position = new_position

    @property
    def vertices(self) -> Vec2List:
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: Vec2List):
        self._vertices = vertices

    def rotate(self, angle: Real) -> None:
        self._angle = angle
        self.update_vertices()

    def apply_force(self, force: Vec2, point: Vec2 | None) -> None:
        if point is not None:
            r = point - self.position
            self.torque += r.cross(force)
        self.force = self.force + force

    def rotate_vertices(self) -> Vec2List:
        angle_radians = math.radians(self.angle)

        cx = sum(x for x, _ in self.vertices) / len(self.vertices)
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

            rotated_vertices.append(Vec2(x_rotated, y_rotated))

        return rotated_vertices

    def update_vertices(self) -> None:
        self.transformed_vertices = []
        self.rotated_vertices = self.rotate_vertices()
        for vertex in self.rotated_vertices:
            new_vertex = vertex + self.position
            self.transformed_vertices.append(new_vertex)

    def update(self, delta_time: Real, gravity: Real = 9.8) -> None:
        acceleration: Vec2 = self.force / self.mass
        self.velocity = self.velocity + acceleration * delta_time
        self.velocity = self.velocity + Vec2(0, gravity) * delta_time
        self.position = self.position + self.velocity * delta_time

        angular_acc = self.torque / self.inertia
        self.angular_velocity += angular_acc * delta_time
        self.angle += self.angular_velocity * delta_time

        self.update_vertices()

        self.force = self.constant_force
        self.torque = 0

    def get_vertices(self, unpacked: bool | None=None) -> Vec2List:
        if unpacked:
            vertices = []
            for vertex in self.transformed_vertices:
                vertices.extend([vertex.x, vertex.y])
            return vertices
        return self.transformed_vertices

    def get_state(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "velocity": self.velocity,
            "angle": self.angle,
            "mass": self.mass,
            "force": self.force,
            "restitution": self.restitution,
        }
