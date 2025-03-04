import tkinter

from physics import PhysicsEngine


class SimulationController:
    def __init__(
        self, simulation_canvas: tkinter.Canvas, delta_time: float = 0.016
    ) -> None:
        self.canvas: tkinter.Canvas = simulation_canvas
        self._delta_time: float = delta_time
        self._running: bool = False
        self.physics = PhysicsEngine()

    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self):
        if self.running:
            self.running = False
            return
        self.running = True

    def step(self, delta_time: float):
        self.physics.update(
            delta_time, self.canvas.winfo_width(), self.canvas.winfo_height()
        )

        if self.running:
            self.render()
            self.canvas.after(int(delta_time * 1000), self.step, 0.016)

    def render(self) -> None:
        for id, polygon in self.physics.bodies:
            self.canvas.coords(id, *polygon.get_vertices())
        pass
