from typing import Iterator

from vector import Vector, VectorList

type Real = int | float
type Objects = tuple[int, Body]
type ObjectsMap = dict[int, Body]

class Body:
    def __init__(self, vertices: VectorList, position: Vector, velocity: Vector) -> None:
        self._vertices: VectorList = vertices
        self._position: Vector = position
        self._velocity: Vector = velocity

    @property
    def vertices(self) -> VectorList:
        return self._vertices

    @property
    def velocity(self) -> Vector:
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity: Vector) -> None:
        self._velocity = new_velocity

    @property
    def position(self) -> Vector:
        return self._position

    @position.setter
    def position(self, new_position: Vector) -> None:
        self._position = new_position


class Bodies:
    def __init__(self):
        self._objects: ObjectsMap = {}
        self._next_id: int = 0
        self._iter_index: int = 0

    @property
    def objects(self) -> ObjectsMap:
        return self._objects

    def add(self, new_body: Body, id: int | None = None) -> int:
        if id is None:
            id = self.next_id
            self.next_id = 1
        self.objects[id] = new_body
        return id

    @property
    def next_id(self) -> int:
        return self._next_id

    @next_id.setter
    def next_id(self, increment: int = 1) -> int:
        new_id = self.next_id + increment
        self.next_id = new_id
        return new_id

    def __iter__(self) -> Iterator:
        self._iter_index = 0
        self._keys = list(self.objects.keys())
        return self

    def __next__(self) -> Objects:
        if self._iter_index < len(self._keys):
            key = self._keys[self._iter_index]
            self._iter_index += 1
            return key, self.objects[key]
        else:
            raise StopIteration

    def __getitem__(self, index: int) -> Body:
        items = list(self.objects.items())
        return items[index][1]

    def __len__(self) -> int:
        return len(self.objects)

    def delete(self, id) -> None:
        if id in self.objects:
            del self.objects[id]

    def get(self, id: int) -> Body | None:
        return self.objects.get(id)

    def items(self):
        return self.objects.items()
