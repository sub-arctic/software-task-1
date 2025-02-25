import math


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def __add__(self, other):
        return Vec2(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        return Vec2(self._x - other.x, self._y - other.y)

    def __mul__(self, scalar):
        return Vec2(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar):
        return Vec2(self._x / scalar, self._y / scalar)

    def dot(self, other):
        return self._x * other.x + self._y * other.y

    def cross(self, other):
        return self._x * other.y - self._y * other.x

    def magnitude(self):
        return math.hypot(self._x, self._y)

    def normalized(self):
        mag = self.magnitude()
        return self / mag if mag else Vec2(0, 0)

    def rotated(self, angle):
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return Vec2(
            self._x * cos_a - self._y * sin_a, self._x * sin_a + self._y * cos_a
        )

    def perpendicular(self):
        return Vec2(-self._y, self._x)
