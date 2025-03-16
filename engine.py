from itertools import combinations

import drawing
from bodies import Bodies
from collision import handle_collision
from custom_types import Scalar
from rigidbody import RigidBody
from vec2 import Vec2


class Engine:
    def __init__(self, gravity: Scalar = 9.81, canvas=None) -> None:
        self._bodies = Bodies()
        self._gravity: Scalar = gravity
        self.canvas = canvas

    @property
    def bodies(self) -> Bodies:
        return self._bodies

    @property
    def gravity(self) -> Scalar:
        return self._gravity

    @gravity.setter
    def gravity(self, new_gravity: Scalar) -> None:
        self._gravity = new_gravity

    def __getitem__(self, id: int) -> RigidBody:
        return self.bodies[id]

    def get_bodies(self) -> Bodies:
        return self.bodies

    def get_body(self, id: int) -> RigidBody | None:
        return self.bodies.get(id)

    def reset(self) -> None:
        self._bodies = Bodies()

    def create_bounds(self, dimensions: Vec2) -> list:
        walls = [
            (dimensions.x, 1, 0, 0),
            (dimensions.x, 1, 0, dimensions.y),
            (1, dimensions.y, 0, 0),
            (1, dimensions.y, dimensions.x, 0),
        ]

        return [
            RigidBody(
                drawing.draw_rectangle(width, height),
                Vec2(x, y),
                Vec2(),
                mass=100,
                restitution=0.9,
            )
            for width, height, x, y in walls
        ]

    def update(self, delta_time: Scalar, dimensions: Vec2) -> None:
        walls = self.create_bounds(dimensions)
        for _, body in self.bodies:
            body.update(delta_time, gravity=self.gravity)
            for wall in walls:
                handle_collision(body, wall)
        for body_a, body_b in combinations(self.bodies, 2):
            body_a = body_a[1]
            body_b = body_b[1]
            handle_collision(body_a, body_b)
