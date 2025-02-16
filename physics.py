import math
class PhysicsObject:
    def __init__(
        self,
        mass,
        bbox,
        position=(0, 0),
        velocity=(0, 0),
    ):
        self.mass = mass
        self.bbox = bbox
        self.position = position
        self.velocity = velocity

    def update_position(self, time):
        self.position = (self.position[0] + self.velocity[0] * time,
                         self.position[1] + self.velocity[1] * time)

    def get_position(self):
        return self.position

    def apply_gravity(self, gravity, time):
        self.velocity = (self.velocity[0], self.velocity[1] + gravity * time)

class Physics:
    def __init__(self, gravity=9.81):
        self.objects = []
        self.gravity = gravity
    def update_gravity(self, gravity):
        self.gravity = gravity

    def add_object(self, obj):
        self.objects.append({'id': len(self.objects) + 1, 'object': obj})

    def update(self, time=1.0):
        for obj in self.objects:
            obj['object'].apply_gravity(self.gravity, time)
            obj['object'].update_position(time)

    def get_position(self, objId):
        object_ = next((obj['object'] for obj in self.objects if obj['id'] == objId), None)
        if object_ is not None:
            return object_.get_position()
        else:
            return None

    def get_object_states(self):
        return [obj['object'] for obj in self.objects]
