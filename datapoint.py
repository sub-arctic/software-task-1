class DataPoint:
    def __init__(self, time, position):
        self.time = time
        self.x = position.x
        self.y = position.y


class DataPointList:
    def __init__(self, max_entries):
        self.max_entries = max_entries
        self.data_points = []

    def __len__(self):
        return len(self.data_points)

    def add_data_point(self, time, position):
        new_point = DataPoint(time, position)
        self.data_points.append(new_point)

        if len(self.data_points) > self.max_entries:
            self.data_points.pop(0)

    def __getitem__(self, index):
        return self.data_points[index]
