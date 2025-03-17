from custom_types import Scalar
from vec2 import Vec2


class DataPoint:
    """Represents a data point with time and position.

    Attributes:
        time (Scalar): The time associated with the data point.
        x (Scalar): The x-coordinate of the position.
        y (Scalar): The y-coordinate of the position.
    """

    def __init__(self, time: Scalar, position: Vec2) -> None:
        """Initializes a DataPoint with time and position.

        Args:
            time (Scalar): The time of the data point.
            position (Vec2): The position of the data point.
        """
        self._time = time
        self._x = position.x
        self._y = position.y

    @property
    def time(self) -> Scalar:
        """Gets the time of the data point."""
        return self._time

    @time.setter
    def time(self, new_time: Scalar) -> None:
        """Sets the time of the data point.

        Args:
            new_time (Scalar): The new time to set.
        """
        self.time = new_time

    @property
    def x(self) -> Scalar:
        """Gets the x-coordinate of the position."""
        return self._x

    @x.setter
    def x(self, new_x: Scalar) -> None:
        """Sets the x-coordinate of the position.

        Args:
            new_x (Scalar): The new x-coordinate to set.
        """
        self.x = new_x

    @property
    def y(self) -> Scalar:
        """Gets the y-coordinate of the position."""
        return self._y

    @y.setter
    def y(self, new_y: Scalar) -> None:
        """Sets the y-coordinate of the position.

        Args:
            new_y (Scalar): The new y-coordinate to set.
        """
        self.y = new_y


class DataPointList:
    """Represents a list of data points with a maximum entry limit.

    Attributes:
        max_entries (int): The maximum number of data points allowed.
        data_points (list): The list of data points.
    """

    def __init__(self, max_entries: int) -> None:
        """Initializes a DataPointList with a maximum entry limit.

        Args:
            max_entries (int): The maximum number of data points.
        """
        self.max_entries = max_entries
        self.data_points = []

    def __len__(self) -> int:
        """Returns the number of data points in the list."""
        return len(self.data_points)

    def add_data_point(self, time: Scalar, position: Vec2) -> None:
        """Adds a new data point to the list.

        If the number of data points exceeds max_entries, the oldest point is removed.

        Args:
            time (Scalar): The time of the new data point.
            position (Vec2): The position of the new data point.
        """
        new_point = DataPoint(time, position)
        self.data_points.append(new_point)

        if len(self.data_points) > self.max_entries:
            self.data_points.pop(0)

    def __getitem__(self, index: int) -> DataPoint:
        """Gets a data point by index.

        Args:
            index (int): The index of the data point to retrieve.

        Returns:
            DataPoint: The data point at the specified index.
        """
        return self.data_points[index]
