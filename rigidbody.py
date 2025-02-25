from vec2 import *


class RigidBody:
    def __init__(self, vertices, mass, velocity, restitution):
        self.vertices = vertices
        self.mass = mass
        self.velocity = velocity
        self.restitution = restitution
        self.position = Vec2()
        self.angle = 0

    def __getitem__(self, index):
        return self.vertices[index]

    def rotate(self, angle):
        return [vertex.rotate(angle) for vertex in self.vertices]

    def get_vertices(self):
        pass
