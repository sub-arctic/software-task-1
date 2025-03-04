from itertools import combinations
from typing import Iterator

import sat
from collision import resolve_collision
from rigidbody import RigidBody

type Real = int | float
type ObjectsMap = dict[int, RigidBody]

class Bodies:
    def __init__(self):
        self._objects: ObjectsMap = {}
        self._next_id: int = 0
        self._iter_index: int = 0

    @property
    def objects(self) -> ObjectsMap:
        return self._objects

    def add(self, new_body: RigidBody, id: int | None = None) -> int:
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

    def __next__(self) -> tuple[int, RigidBody]:
        if self._iter_index < len(self._keys):
            key = self._keys[self._iter_index]
            self._iter_index += 1
            return key, self.objects[key]
        else:
            raise StopIteration

    def __getitem__(self, index: int) -> RigidBody:
        items = list(self.objects.items())
        return items[index][1]

    def __len__(self) -> int:
        return len(self.objects)

    def delete(self, id) -> None:
        if id in self.objects:
            del self.objects[id]

    def get(self, id: int) -> RigidBody | None:
        return self.objects.get(id)

    def items(self):
        return self.objects.items()


class Engine:
    def __init__(self, gravity: Real = 9.81) -> None:
        self._bodies = Bodies()
        self._gravity: Real = gravity

    @property
    def bodies(self) -> Bodies:
        return self._bodies

    @property
    def gravity(self) -> Real:
        return self._gravity

    @gravity.setter
    def gravity(self, new_gravity: Real) -> None:
        self.gravity = new_gravity

    def __getitem__(self, id: int) -> RigidBody:
        return self.bodies[id]

    def get_bodies(self) -> Bodies:
        return self.bodies

    def get_body(self, id: int) -> RigidBody | None:
        return self.bodies.get(id)

    def update(self, delta_time: Real, cwidth: int, cheight: int) -> None:
        for _, body in self.bodies:
            body.update(delta_time)
        for body_a, body_b in combinations(self.bodies, 2):
            body_a = body_a[1]
            body_b = body_b[1]
            collision, depth, normal, contact = sat.is_colliding(body_a, body_b)
            if (collision) and normal is not None:
                resolve_collision(body_a, body_b, depth, normal, contact)



