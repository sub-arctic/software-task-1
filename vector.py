from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Generator

type real = int | float

@dataclass
class Vector:
    def __init__(self, x: real = 0, y: real = 0):
        self._x = x
        self._y = y

    @property
    def x(self) -> real:
        return self._x

    @x.setter
    def x(self, new_x: real = 0) -> None:
        self._x = new_x

    @property
    def y(self) -> real:
        return self._y

    @y.setter
    def y(self, new_y: real = 0) -> None:
        self._y = new_y

    def __add__(self, other: Vector) -> Vector:
        return Vector(self._x + other.x, self._y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self._x - other.x, self._y - other.y)

    def __mul__(self, scalar: real) -> Vector:
        return Vector(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar: real) -> Vector:
        return Vector(self._x / scalar, self._y / scalar)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def dot(self, other: Vector) -> real:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vector) -> real:
        return self.x * other.y - self.y * other.x

    def magnitude(self) -> real:
        return math.hypot(self.x, self.y)

    def normalized(self) -> Vector:
        mag = self.magnitude()
        return self / mag if mag else Vector(0, 0)

    def rotated(self, angle: real) -> Vector:
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return Vector(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def perpendicular(self) -> Vector:
        return Vector(-self.y, self.x)

class VectorList:
    def __init__(self, vectors: list[Vector] | None = None, *args: Vector):
        if vectors is not None:
            self._vectors  = vectors
            return
        self._vectors = list(args)

    @property
    def vectors(self) -> list[Vector]:
        return self._vectors

    @vectors.setter
    def vectors(self, new_vectors: list[Vector]) -> None:
        self._vectors = new_vectors

    def __iter__(self) -> Generator[Vector, None, None]:
        for vector in self.vectors:
            yield vector

    def __getitem__(self, index: int) -> Vector:
        return self.vectors[index]

    def __len__(self) -> int:
        return len(self.vectors)

    def append(self, item: Vector) -> None:
        self.vectors.append(item)

    def unpack(self):
        return [vector for vec in self.vectors for vector in (vec.x, vec.y)]

