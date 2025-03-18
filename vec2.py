from __future__ import annotations

import math
from typing import Generator

type Scalar = int | float


class Vec2List:
    """A class to manage a list of 2D vectors.

    Attributes:
        vectors (list[Vec2]): A list of Vec2 objects.
    """

    def __init__(self, vectors: list[Vec2] | None = None):
        """Initializes a Vec2List with an optional list of Vec2 vectors.

        Args:
            vectors (list[Vec2] | None): A list of Vec2 objects. If None, initializes an empty list.
        """
        if vectors is None:
            self._vectors = []
        else:
            self._vectors = vectors

    @property
    def vectors(self) -> list[Vec2]:
        """Gets the list of vectors.

        Returns:
            list[Vec2]: The list of Vec2 objects.
        """
        return self._vectors

    @vectors.setter
    def vectors(self, vectors: list[Vec2]) -> None:
        """Sets the list of vectors.

        Args:
            vectors (list[Vec2]): A new list of Vec2 objects.
        """
        self._vectors = vectors

    def __iter__(self) -> Generator[Vec2, None, None]:
        """Iterates over the vectors in the list.

        Yields:
            Vec2: Each Vec2 object in the list.
        """
        for vector in self.vectors:
            yield vector

    def __getitem__(self, index: int) -> Vec2:
        """Gets a vector by index.

        Args:
            index (int): The index of the vector to retrieve.

        Returns:
            Vec2: The Vec2 object at the specified index.
        """
        return self.vectors[index]

    def __len__(self) -> int:
        """Gets the number of vectors in the list.

        Returns:
            int: The number of Vec2 objects in the list.
        """
        return len(self.vectors)

    def append(self, item: Vec2) -> None:
        """Appends a Vec2 object to the list.

        Args:
            item (Vec2): The Vec2 object to append.
        """
        self.vectors.append(item)

    def unpack(self) -> list[Scalar]:
        """Unpacks the list of vectors into a flat list of x and y coordinates.

        Returns:
            list[Scalar]: A flat list containing the x and y coordinates of each vector.
        """
        return [vector for vec in self.vectors for vector in (vec.x, vec.y)]


class Vec2:
    """A class representing a 2D vector.

    Attributes:
        x (Scalar): The x-coordinate of the vector.
        y (Scalar): The y-coordinate of the vector.
    """

    def __init__(self, x: Scalar = 0.0, y: Scalar = 0.0):
        """Initializes a Vec2 object with x and y coordinates.

        Args:
            x (Scalar): The x-coordinate. Defaults to 0.0.
            y (Scalar): The y-coordinate. Defaults to 0.0.
        """
        self._x: Scalar = x
        self._y: Scalar = y

    @property
    def x(self) -> Scalar:
        """Gets the x-coordinate of the vector.

        Returns:
            Scalar: The x-coordinate.
        """
        return self._x

    @property
    def y(self) -> Scalar:
        """Gets the y-coordinate of the vector.

        Returns:
            Scalar: The y-coordinate.
        """
        return self._y

    @x.setter
    def x(self, new_x: Scalar):
        """Sets the x-coordinate of the vector.

        Args:
            new_x (Scalar): The new x-coordinate.
        """
        self._x = new_x

    @y.setter
    def y(self, new_y: Scalar):
        """Sets the y-coordinate of the vector.

        Args:
            new_y (Scalar): The new y-coordinate.
        """
        self._y = new_y

    def __iter__(self):
        """Iterates over the x and y coordinates of the vector.

        Returns:
            Iterator[Scalar]: An iterator over the x and y coordinates.
        """
        return iter((self._x, self._y))

    def __add__(self, other: Vec2) -> Vec2:
        """Adds another vector to this vector.

        Args:
            other (Vec2): The vector to add.

        Returns:
            Vec2: The resulting vector after addition.
        """
        return Vec2(self._x + other.x, self._y + other.y)
    def __sub__(self, other: Vec2) -> Vec2:
        """Subtracts another vector from this vector
                    Args:
            other (Vec2): The vector to subtract.

        Returns:
            Vec2: The resulting vector after subtraction.
        """
        return Vec2(self._x - other.x, self._y - other.y)

    def __mul__(self, scalar: Scalar) -> Vec2:
        """Multiplies this vector by a scalar.

        Args:
            scalar (Scalar): The scalar to multiply by.

        Returns:
            Vec2: The resulting vector after multiplication.
        """
        return Vec2(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar: Scalar) -> Vec2:
        """Divides this vector by a scalar.

        Args:
            scalar (Scalar): The scalar to divide by.

        Returns:
            Vec2: The resulting vector after division.
        """
        return Vec2(self._x / scalar, self._y / scalar)

    def __neg__(self) -> Vec2:
        """Negates the vector.

        Returns:
            Vec2: The negated vector.
        """
        return Vec2(-self.x, -self.y)

    def dot(self, other: Vec2) -> Scalar:
        """Calculates the dot product with another vector.

        Args:
            other (Vec2): The vector to calculate the dot product with.

        Returns:
            Scalar: The dot product of the two vectors.
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vec2) -> Scalar:
        """Calculates the cross product with another vector.

        Args:
            other (Vec2): The vector to calculate the cross product with.

        Returns:
            Scalar: The cross product of the two vectors.
        """
        return self.x * other.y - self.y * other.x

    def magnitude(self) -> Scalar:
        """Calculates the magnitude (length) of the vector.

        Returns:
            Scalar: The magnitude of the vector.
        """
        return math.hypot(self.x, self.y)

    def rotated(self, angle: Scalar) -> Vec2:
        """Rotates the vector by a given angle in radians.

        Args:
            angle (Scalar): The angle in radians to rotate the vector.

        Returns:
            Vec2: A new Vec2 object representing the rotated vector.
        """
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vec2(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

    def perpendicular(self) -> Vec2:
        """Calculate the perpendicular vector.

        This method returns a new vector that is perpendicular to the current vector.
        The perpendicular vector is obtained by swapping the x and y components and 
        negating the y component.

        Returns:
            Vec2: A new Vec2 instance representing the perpendicular vector.
        """
        return Vec2(-self._y, self._x)

    def normalized(self) -> Vec2:
        """Normalize the vector.

        This method returns a new vector that is a normalized version of the current vector.
        Normalization is the process of scaling the vector to have a length of 1 while 
        maintaining its direction. If the vector is a zero vector (magnitude is zero), 
        it will return a zero vector.

        Returns:
            Vec2: A new Vec2 instance representing the normalized vector. 
                  If the vector is a zero vector, a zero vector is returned.

        Example:
            >>> v = Vec2(3, 4)
            >>> normalized_v = v.normalized()
            >>> print(normalized_v)  # Output: Vec2(0.6, 0.8)

        Raises:
            ValueError: If the vector is a zero vector, normalization is undefined.
        """
        mag = self.magnitude()
        return self / mag if mag else Vec2(0, 0)

