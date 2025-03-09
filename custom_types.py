from typing import Optional

from vec2 import Vec2, Vec2List

Scalar = int | float
# Vec2 = Vec2
# Vec2List = Vec2List


class CollisionResult:
    def __init__(
        self,
        collided: bool,
        penetration: Optional[Scalar] = 0,
        normal: Optional[Vec2] = None,
        contacts: Optional[Vec2List] = None,
    ):
        self.collided = collided
        self.penetration = penetration
        self.normal = normal
        self.contacts = contacts

    def __iter__(self):
        return iter((self.penetration, self.normal, self.contacts))

    @property
    def is_collision(self) -> bool:
        return self.collided
