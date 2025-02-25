import gjk
import sat


class Bodies:
    def __init__(self):
        self.objects = {}
        self.next_id = 0
        self._iter_index = 0

    def __iter__(self):
        self._iter_index = 0
        self._keys = list(self.objects.keys())
        return self

    def __next__(self):
        if self._iter_index < len(self._keys):
            key = self._keys[self._iter_index]
            self._iter_index += 1
            return key, self.objects[key]
        else:
            raise StopIteration

    def __getitem__(self, id):
        return self.objects[id]

    def __len__(self):
        return len(self.objects)

    def add(self, obj, id=None):
        if id is None:
            id = self.next_id
            self.next_id += 1
        self.objects[id] = obj
        return id

    def delete(self, id):
        if id in self.objects:
            del self.objects[id]

    def get(self, id):
        return self.objects.get(id)

    def change_id(self, id, new_id):
        if new_id in self.objects:
            raise ValueError(f"ID {new_id} already exists")
        self.objects[new_id] = self.objects.pop(id)

    def items(self):
        return self.objects.items()


class Engine:
    def __init__(self, gravity=9.81):
        self.bodies = Bodies()
        self.gravity = gravity
        self.bounds = False

    def __getitem__(self, id):
        return self.bodies[id]

    def get_bodies(self):
        return self.bodies

    def update(self, delta_time):
        for _, body in self.bodies:
            body.update(delta_time, gravity=self.gravity)
        self.collisions()

    def collisions(self):
        num_bodies = len(self.bodies)
        for i in range(num_bodies):
            for j in range(i + 1, num_bodies):
                body_a = self.bodies[i]
                body_b = self.bodies[j]
                colliding, normal, penetration, contact, _ = sat.sat_collision(
                    body_a, body_b
                )
                if colliding:
                    sat.resolve_collision(body_a, body_b, normal, penetration, contact)
