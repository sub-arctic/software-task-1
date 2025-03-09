from __future__ import annotations

import math
from typing import Generator

type Scalar = int | float


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
    def __init__(self, x: Scalar = 0.0, y: Scalar = 0.0):
        self._x: Scalar = x
        self._y: Scalar = y

    @property
    def x(self) -> Scalar:
        return self._x

    @property
    def y(self) -> Scalar:
        return self._y

    @x.setter
    def x(self, new_x: Scalar):
        self._x = new_x

    @y.setter
    def y(self, new_y: Scalar):
        self._y = new_y

    def __iter__(self):
        return iter((self._x, self._y))

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self._x + other.x, self._y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self._x - other.x, self._y - other.y)

    def __mul__(self, scalar: Scalar) -> Vec2:
        return Vec2(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar: Scalar) -> Vec2:
        return Vec2(self._x / scalar, self._y / scalar)

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)

    def dot(self, other: Vec2) -> Scalar:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vec2) -> Scalar:
        return self.x * other.y - self.y * other.x

    def magnitude(self) -> Scalar:
        return math.hypot(self.x, self.y)

    def normalized(self) -> Vec2:
        mag = self.magnitude()
        return self / mag if mag else Vec2(0, 0)

    def rotated(self, angle: Scalar) -> Vec2:
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return Vec2(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def perpendicular(self) -> Vec2:
        return Vec2(-self.y, self.x)

    def length(self) -> Scalar:
        return math.sqrt(self.x**2 + self.y**2)
