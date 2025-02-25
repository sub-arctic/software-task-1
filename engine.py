import gjk
import sat


class Bodies:
    def __init__(self):
        self.objects = {}
        self.next_id = 0

    def __iter__(self):
        return iter(self.objects.values())

    def __getitem__(self, index):
        return self.objects[index]

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
        self.objects[id] = self.objects.pop(id)

    def items(self):
        return self.objects.items()


class Engine:
    def __init__(self, gravity=9.81):
        self.bodies = Bodies()
        self.gravity = gravity

    def __getitem__(self, index):
        return self.bodies[index]

    def get_bodies(self):
        return self.bodies

    def get_body(self, id):
        return self.bodies.get(id)

    def update(self, delta_time):
        for body in self.bodies:
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
