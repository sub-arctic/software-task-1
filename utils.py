class DataPointList:
    def __init__(self, max_size: int = 100) -> None:
        self.max_size = max_size
        self.data_points = []

    def add_data_point(self, timestamp: int, point) -> None:
        if len(self.data_points) >= self.max_size:
            self.data_points.pop(0)
        self.data_points.append((timestamp, point))


