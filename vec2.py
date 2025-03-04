from __future__ import annotations

import math
from typing import Generator

type Real = int | float

class Vec2List:
    def __init__(self, vectors: list[Vec2] | None = None):
        if vectors is None:
            self._vectors = []
        else:
            self._vectors = vectors

    @property
    def vectors(self) -> list[Vec2]:
        return self._vectors

    @vectors.setter
    def vectors(self, vectors: list[Vec2]) -> None:
         self._vectors = vectors

    def __iter__(self) -> Generator[Vec2, None, None]:
        for vector in self.vectors:
            yield vector

    def __getitem__(self, index: int) -> Vec2:
        return self.vectors[index]

    def __len__(self) -> int:
        return len(self.vectors)

    def append(self, item: Vec2) -> None:
        self.vectors.append(item)

    def unpack(self):
        return [vector for vec in self.vectors for vector in (vec.x, vec.y)]

class Vec2:
    def __init__(self, x: Real = 0.0, y: Real = 0.0):
        self._x: Real = x
        self._y: Real = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, new_x: Real):
        self._x = new_x

    @y.setter
    def y(self, new_y: Real):
        self._y = new_y

    def __iter__(self):
        return iter((self._x, self._y))

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self._x + other.x, self._y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self._x - other.x, self._y - other.y)

    def __mul__(self, scalar: Real) -> Vec2:
        return Vec2(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar: Real) -> Vec2:
        return Vec2(self._x / scalar, self._y / scalar)

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)

    def dot(self, other: Vec2) -> Real:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vec2) -> Real:
        return self.x * other.y - self.y * other.x

    def magnitude(self) -> Real:
        return math.hypot(self.x, self.y)

    def normalized(self) -> Vec2:
        mag = self.magnitude()
        return self / mag if mag else Vec2(0, 0)

    def rotated(self, angle: Real) -> Vec2:
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return Vec2(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def perpendicular(self) -> Vec2:
        return Vec2(-self.y, self.x)

    def length(self) -> Real:
        return math.sqrt(self.x ** 2 + self.y ** 2)
