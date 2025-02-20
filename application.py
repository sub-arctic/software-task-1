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
### refactor shape drawing methods to increase maintainability

class SimulationCanvas(tk.Canvas):
    def __init__(self, parent, width=512, height=512):
        self.canvas = tk.Canvas(
            parent,
            bg=Defaults.BACKGROUND,
            width=width, height=height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.parent = parent

        self.update_canvas_dimensions()

        self.simulation_running = False
        self.physics_engine = physics.PhysicsEngine()
        self.speed_factor = 2

        self.mouse_positions = physics.DataPointList(2)
        self.canvas.tag_bind("body", "<ButtonPress-1>", self.body_press)
        self.canvas.tag_bind("body", "<B1-Motion>", self.body_drag_motion)
        self.canvas.tag_bind("body", "<ButtonRelease-1>", self.body_drag_release)

    def temp_draw_square(self):
        square = shapes.draw_square(200, 100, 100, 100)
        self.physics_engine.add_rigid_body(square)
        self.draw_polygon(square.get_vertices(), outline="white")

    def draw_polygon(self, vertices, *args, **kwargs):
        tags = ("body", f"body_{id}")
        return self.canvas.create_polygon(
            *vertices, tags=tags, *args, **kwargs
        )

    def body_press(self, _):
        self.pressed_body_id = self.canvas.find_withtag("current")[0]
        self.current_body = self.physics_engine.get_body(self.pressed_body_id)
        self.canvas.itemconfigure(self.pressed_body_id, dash=(3, 5))

    def body_drag_motion(self, event):
        self.current_body = self.physics_engine.get_body(self.pressed_body_id)
        if self.current_body is not None:
            new_position = physics.Vector2D(event.x, event.y)
            new_velocity = physics.Vector2D(0, 0)

            self.current_body.move(new_position, new_velocity)

            time_ = time.perf_counter_ns()

            self.mouse_positions.add_data_point(time_, new_position)
    
    def body_drag_release(self, _):
        new_velocity = physics.calculate_velocity(self.mouse_positions)
        if self.current_body is not None:
            self.current_body.move(velocity=new_velocity)
            self.canvas.itemconfigure(self.pressed_body_id, dash=())

    def play_pause_simulation(self):
        dt = 0.016

        if self.simulation_running == True:
            self.simulation_running = False
            self.parent.play_pause_text.set("Play")
        else:
            self.simulation_running = True
            self.parent.play_pause_text.set("Pause")
            self.step_simulation(dt)

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
            if self.canvas.find_withtag(id):
                self.canvas.coords(id, *vertices)
                
    def update_canvas_dimensions(self):
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

class SimulationScreen(Application):
    def __init__(self, parent, simulation_canvas, width=512, height=512):
        super().__init__(parent)
        self.parent = parent
        self.canvas = simulation_canvas

        self.add_square_button = ttk.Button(self, text="add", command=self.canvas.temp_draw_square)
        self.add_square_button.grid(row=1, column=0)

        self.parent.play_pause_text = tk.StringVar()
        self.parent.play_pause_text.set("Play")
        self.play_pause_button = ttk.Button(self, text="Start", textvariable=self.parent.play_pause_text, command=self.canvas.play_pause_simulation)
        self.play_pause_button.grid(row=1, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title(Defaults.TITLE)
    root.geometry(Defaults.WINDOW_GEOMETRY)

    canvas = SimulationCanvas(root)
    
    app = SimulationScreen(root, canvas)
    app.pack()

    root.mainloop()
