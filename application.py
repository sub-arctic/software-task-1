import tkinter as tk
from tkinter import ttk
import physics
class Defaults:
    TITLE = "root"
    WINDOW_GEOMETRY="1920x1080"
    BACKGROUND="black"
    FOREGROUND="white"

    @classmethod
    def get_defaults(cls):
        return {
            "title": cls.TITLE,
            "geometry": cls.WINDOW_GEOMETRY,
            "background": cls.BACKGROUND,
            "foreground": cls.FOREGROUND
        }

class Application(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

### TODO:
### implement basic "toolbar", for shape creation, relocation etc.
### allow adding constant force arrows to shapes
### make cursor have physics
### make shapes draggable (reimplement from old program)
class SimulationScreen(Application):
    def __init__(self, parent, width=512, height=512):
        super().__init__(parent)
        self.parent = parent
        self.canvas = tk.Canvas(self, bg=Defaults.BACKGROUND, width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_button = ttk.Button(self, text="Start", command=self.start_simulation)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(padx=10)

        self.simulation_running = False
        self.physics_engine = physics.PhysicsEngine()
        self.speed_factor = 2

        shapes = [
            physics.RigidBody(mass=2, bbox=(50, 30), position=physics.Vector2D(100, 50),
                              velocity=physics.Vector2D(30, 0), restitution=0.7),
            physics.RigidBody(mass=1, bbox=(40, 40), position=physics.Vector2D(300, 100),
                              velocity=physics.Vector2D(-20, 10), restitution=0.7),
            physics.RigidBody(mass=50, bbox=(100, 100), position=physics.Vector2D(200, 300),
                              velocity=physics.Vector2D(0, -15), restitution=0.6)
        ]
        for body in shapes:
            self.physics_engine.add_rigid_body(body)

    def draw_shape(self, vertices, *args, **kwargs):
        id = self.canvas.create_polygon(vertices, *args, **kwargs)
        return id

    def start_simulation(self, dt=0.016):
        if not self.simulation_running:
            self.simulation_running = True
            self.step_simulation(dt)

    def stop_simulation(self):
        if self.simulation_running:
            self.simulation_running = False

    def step_simulation(self, dt=0.016):
        scaled_dt = dt * self.speed_factor
        self.physics_engine.update(scaled_dt, self.canvas.winfo_width(), self.canvas.winfo_height())
        if self.simulation_running:
            self.update_canvas()
            self.parent.after(int(dt * 1000 / self.speed_factor), self.step_simulation)

    def update_canvas(self):
        # probably should move this
        def get_coordinates(v):
            return (v.x, v.y)
        self.bodies = self.physics_engine.get_bodies()
        self.canvas.delete("all")
        for _, vectors in self.bodies.items():
            coordinates = [get_coordinates(i) for i in vectors]
            self.draw_shape(coordinates, outline="white")

if __name__ == "__main__":
    root = tk.Tk()
    root.title(Defaults.TITLE)
    root.geometry(Defaults.WINDOW_GEOMETRY)

    app = SimulationScreen(root, 512, 512)
    app.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
