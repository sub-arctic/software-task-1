from typing import Union

from rigidbody import RigidBody
from vec2 import Vec2, Vec2List

Real = Union[int, float]

PENETRATION_SLOP: Real = 0.01
POSITION_BIAS: Real = 0.8


def resolve_collision(
    body_a: RigidBody,
    body_b: RigidBody,
    penetration: Real,
    collision_normal: Vec2,
    contact: Vec2,
) -> None:

    if penetration > 0 and penetration < 0.5:
        print("close")
