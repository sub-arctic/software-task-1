import math
class Coordinate:
    """Represents a 2D coordinate."""

    def __init__(self, x=0.0, y=0.0):
        """Initialize the coordinate with x and y values."""
        self._x = x
        self._y = y

    @property
    def x(self):
        """Get the x coordinate."""
        return self._x

    @x.setter
    def x(self, value):
        """Set the x coordinate."""
        self._x = value

    @property
    def y(self):
        """Get the y coordinate."""
        return self._y

    @y.setter
    def y(self, value):
        """Set the y coordinate."""
        self._y = value

    def __iter__(self):
        """Return an iterator for unpacking."""
        return iter((self.x, self.y))
    
    def midpoint(self, p2):
        mx = (self.x + p2.x) / 2
        my = (self.y + p2.y) / 2
        return Coordinate(mx, my)

    def distance(self, p2):
        return math.sqrt((p2.x - self.x) ** 2 + (p2.y - self.y) ** 2)

