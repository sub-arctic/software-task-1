import math
from typing import Any

from vec2 import Vec2, Vec2List

type Real = int | float


class RigidBody:
    def __init__(
        self, vertices: Vec2List, position: Vec2, velocity: Vec2, angle: Real = 0, mass: Real = 5, restitution: Real = 0.5
    ):
        self._vertices: Vec2List = vertices
        self._position: Vec2 = position
        self._velocity: Vec2 = velocity
        self._angle: Real = angle
        self._mass: Real = mass
        self._restitution: Real = restitution

    @property
    def velocity(self) -> Vec2:
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity: Vec2):
        self._velocity = new_velocity

    @property
    def angle(self) -> Real:
        return self._angle

    @angle.setter
    def angle(self, new_angle: Real):
        self._angle = new_angle

    @property
    def mass(self) -> Real:
        return self._mass

    @mass.setter
    def mass(self, new_mass: Real):
        self._mass = new_mass

    @property
    def restitution(self) -> Real:
        return self._restitution

    @restitution.setter
    def restitution(self, new_restitution: Real):
        if new_restitution < 0 or new_restitution > 1:
            raise ValueError("Restitution must be between 0 and 1")
        if type(new_restitution) is not Real:
            raise TypeError("Restitution must be a real number")
        self._restitution = new_restitution

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, new_position: Vec2):
        self._position = new_position

    @property
    def vertices(self) -> Vec2List:
        return self._vertices

    def get_vertices(self) -> Vec2List:
        translated_vertices: Vec2List = Vec2List()
        for vertex in self.rotate(self.vertices, self.angle):
            translated_vertices.append(vertex + self.position)
        return translated_vertices

    def rotate(self, vertices: Vec2List, angle: Real) -> Vec2List:
        angle_radians = math.radians(angle)

        cx = sum(x for x, _ in vertices) / len(vertices)
        cy = sum(y for y, y in vertices) / len(vertices)

        rotated_vertices = Vec2List()

        for x, y in vertices:
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

    def update(self, delta_time: Real, gravity: Real = 9.8) -> None:
        self.position = self.position + self.velocity * delta_time
        self.velocity.y += gravity * delta_time

    def get_state(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "velocity": self.velocity,
            "angle": self.angle,
            "mass": self.mass,
            "restitution": self.restitution,
        }
