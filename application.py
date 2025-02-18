import tkinter as tk
from tkinter import ttk
import physics
import shapes
import random
import time
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
### potentially make simulationscreen just a canvas

class SimulationCanvas(tk.Canvas):
    def __init__(self, parent, width=512, height=512):
        self.canvas = tk.Canvas(parent, bg=Defaults.BACKGROUND, width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.parent = parent

        self.update_canvas_dimensions()

        self.simulation_running = False
        self.physics_engine = physics.PhysicsEngine()
        self.speed_factor = 2

        for _ in range(2):
            self.create_square()

        self.mouse_positions = physics.DataPointList(2)
        self.canvas.tag_bind("body", "<ButtonPress-1>", self.body_press)
        self.canvas.tag_bind("body", "<B1-Motion>", self.body_drag_motion)
        self.canvas.tag_bind("body", "<ButtonRelease-1>", self.body_drag_release)

    def create_square(self):
            size_x = random.randint(30, 100)
            size_y = random.randint(30, 100)
            shape = shapes.draw_square(
                int(self.canvas_width)/2, int(self.canvas_height)/2, size_x, size_y
            )

            self.physics_engine.add_rigid_body(shape)

    def body_press(self, event):
        self.pressed_body_id = self.canvas.find_withtag("current")[0]

    def body_drag_motion(self, event):
        self.current_body = self.physics_engine.get_body(self.pressed_body_id)
        if self.current_body is not None:
            new_position = physics.Vector2D(event.x, event.y)
            new_velocity = physics.Vector2D(0, 0)

            self.current_body.move(new_position, new_velocity)

            time_ = time.perf_counter_ns()

            self.mouse_positions.add_data_point(time_, new_position)
    
    def body_drag_release(self, event):
        new_velocity = physics.calculate_velocity(self.mouse_positions)
        if self.current_body is not None:
            self.current_body.move(velocity=new_velocity)

    def draw_shape(self, vertices, *args, **kwargs):
        return self.canvas.create_polygon(
            *vertices, tags=("body", f"body_{id}"), *args, **kwargs
        )

    def start_simulation(self, dt=0.016):
        if not self.simulation_running:
            self.simulation_running = True
            self.step_simulation(dt)

    def stop_simulation(self):
        if self.simulation_running:
            self.simulation_running = False

    def update_canvas_dimensions(self):
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

    def step_simulation(self, dt=0.016):
        scaled_dt = dt * self.speed_factor
        self.update_canvas_dimensions()
        self.physics_engine.update(scaled_dt, self.canvas_width, self.canvas_height)
        if self.simulation_running:
            self.update_canvas()
            self.parent.after(int(dt * 1000 / self.speed_factor), self.step_simulation)
    
    def update_canvas(self):
        self.bodies = self.physics_engine.get_bodies()
        for id, body in self.bodies.items():
            vertices = []
            for vec in body:
                vertices.extend([vec.x, vec.y])
            if not self.canvas.find_withtag(id):
                new_id = self.draw_shape(vertices, outline="white")
                self.physics_engine.update_id(id, new_id)
            else:
                self.canvas.coords(id, *vertices)

class SimulationScreen(Application):
    def __init__(self, parent, simulation_canvas, width=512, height=512):
        super().__init__(parent)
        self.parent = parent
        self.canvas = simulation_canvas

        self.start_button = ttk.Button(self, text="Start", command=self.canvas.start_simulation)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self, text="Stop", command=self.canvas.stop_simulation)
        self.stop_button.pack(padx=10)

        self.add_square_button = ttk.Button(self, text="Add square", command=self.canvas.create_square)
        self.add_square_button.pack(pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    root.title(Defaults.TITLE)
    root.geometry(Defaults.WINDOW_GEOMETRY)

    canvas = SimulationCanvas(root)
    
    app = SimulationScreen(root, canvas)
    app.pack()

    root.mainloop()
