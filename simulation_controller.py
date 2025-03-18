from __future__ import annotations
import engine
import vec2

DELTA_TIME = 0.016
SPEED_FACTOR = 3

class SimulationController:
    def __init__(self, canvas) -> None:
        self.running = False
        self.dt = DELTA_TIME
        self.speed = SPEED_FACTOR
        self.canvas = canvas
        self.physics_engine = engine.Engine(canvas=self.canvas)

    def step(self) -> None:
        scaled_dt = self.dt * self.speed
        self.canvas.update_dimensions()
        self.physics_engine.update(
            scaled_dt, vec2.Vec2(self.canvas.width, self.canvas.height)
        )
        if self.running:
            self.update()
            self.canvas.after(int(self.dt * 1000 / self.speed), self.step)
        self.canvas.parent.properties_frame.update_properties()

    def reset(self) -> None:
        self.dt = DELTA_TIME
        self.running = False
        self.speed = SPEED_FACTOR
        self.physics_engine.reset()
        self.canvas.delete("all")

    def update(self) -> None:
        for id, body in self.physics_engine.bodies:
            self.canvas.coords(id, *body.get_vertices().unpack())

    def set_gravity(self, new_gravity: str) -> None:
        self.physics_engine.gravity = float(new_gravity)

    def set_speed_factor(self, value: str) -> None:
        self.speed = float(value)

