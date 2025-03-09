import math
from typing import Any, Optional

import physics
from custom_types import Scalar
from vec2 import Vec2, Vec2List


class RigidBody:
    def __init__(
        self,
        vertices: Vec2List,
        position: Vec2,
        velocity: Vec2,
        angle: Scalar = 0,
        mass: Scalar = 5,
        restitution: Scalar = 0.5,
    ):
        self._vertices: Vec2List = vertices
        self._position: Vec2 = position
        self._velocity: Vec2 = velocity
        self._angle: Scalar = angle
        self._mass: Scalar = mass
        self._restitution: Scalar = restitution
        self.moment_of_inertia: Scalar = physics.compute_polygon_inertia(
            self.vertices, mass
        )
        self.angular_velocity: Scalar = 0
        self.force = Vec2()
        self.torque = 0
        self.pinned = False

    @property
    def velocity(self) -> Vec2:
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity: Vec2):
        self._velocity = new_velocity

    @property
    def angle(self) -> Scalar:
        return self._angle

    @angle.setter
    def angle(self, new_angle: Scalar):
        self._angle = new_angle

    @property
    def mass(self) -> Scalar:
        return self._mass

    @mass.setter
    def mass(self, new_mass: Scalar):
        self._mass = new_mass

    @property
    def restitution(self) -> Scalar:
        return self._restitution

    @restitution.setter
    def restitution(self, new_restitution: Scalar):
        if new_restitution < 0 or new_restitution > 1:
            raise ValueError("Restitution must be between 0 and 1")
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

    def get_vertices(self):
        return Vec2List([v.rotated(self.angle) + self.position for v in self.vertices])

    def apply_force(self, force, point=None):
        self.force = self.force + force
        if point is not None:
            r = point - self.position
            self.torque += r.cross(force)

    def pin(self, position: Optional[Vec2] = None) -> None:
        if self.pinned:
            self.unpin()
            return

        if position is not None:
            self.position = position
        self.velocity = Vec2()
        self.angular_velocity = 0
        self.restitution = 0.9
        self.pinned = True

    def unpin(self) -> None:
        self.pinned = False

    def update(self, delta_time: Scalar, gravity: Scalar = 9.8) -> None:
        if self.pinned:
            return
        self.apply_force(Vec2(0, self.mass * gravity))

        acceleration = self.force / self.mass
        self.velocity = self.velocity + acceleration * delta_time
        self.position = self.position + self.velocity * delta_time

        angular_acc = self.torque / self.moment_of_inertia
        self.angular_velocity += angular_acc * delta_time
        self.angle += self.angular_velocity * delta_time

        self.force = Vec2()

    def get_state(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "velocity": self.velocity,
            "angle": self.angle,
            "mass": self.mass,
            "restitution": self.restitution,
        }
