from custom_types import Scalar
from vec2 import Vec2


class DataPoint:
    def __init__(self, time: Scalar, position: Vec2) -> None:
        self._time = time
        self._x = position.x
        self._y = position.y

    @property
    def time(self) -> Scalar:
        return self._time

    @time.setter
    def time(self, new_time: Scalar) -> None:
        self.time = new_time

    @property
    def x(self) -> Scalar:
        return self._x

    @x.setter
    def x(self, new_x) -> None:
        self.x = new_x

    @property
    def y(self) -> Scalar:
        return self._y

    @y.setter
    def y(self, new_y) -> None:
        self.y = new_y


class DataPointList:
    def __init__(self, max_entries: int) -> None:
        self.max_entries = max_entries
        self.data_points = []

    def __len__(self) -> int:
        return len(self.data_points)

    def add_data_point(self, time: Scalar, position: Vec2) -> None:
        new_point = DataPoint(time, position)
        self.data_points.append(new_point)

        if len(self.data_points) > self.max_entries:
            self.data_points.pop(0)

    def __getitem__(self, index: int) -> DataPoint:
        return self.data_points[index]
