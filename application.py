import time
import tkinter as tk
from tkinter import ttk

import physics
import shapes

# TODO:
# implement basic "toolbar", for shape creation, relocation etc.
# allow adding constant force arrows to shapes
# make cursor have physics
# potentially make simulationscreen just a canvas
# refactor shape drawing methods to increase maintainability


class Toolbar(ttk.Frame):
    def __init__(self, parent, simulation_canvas):
        super().__init__(parent, borderwidth=3)
        self.pack()

        self.parent = parent

        self.add_square_button = ttk.Button(
            self, text="Add square", command=simulation_canvas.draw_square
        )
        self.add_square_button.grid()

        self.parent.play_pause_text = tk.StringVar()
        self.parent.play_pause_text.set("Play")
        self.play_pause_button = ttk.Button(
            self,
            text="Start",
            textvariable=self.parent.play_pause_text,
            command=simulation_canvas.play_pause_simulation,
        )
        self.play_pause_button.grid()


class PropertiesFrame(ttk.Frame):
    def __init__(self, parent, simulation_canvas):
        super().__init__(parent, borderwidth=3)

        self.pack()
        self.simulation_canvas = simulation_canvas

        self.velocity_x_text = ttk.Label(
            textvariable=self.simulation_canvas.velocity_x
        ).pack()
        self.velocity_y_text = ttk.Label(
            textvariable=self.simulation_canvas.velocity_y
        ).pack()

    def call(self):
        if self.simulation_canvas.current_body is not None:
            state = self.simulation_canvas.current_body.get_state()
            self.simulation_canvas.velocity_x.set(state["velocity"].x)
            self.simulation_canvas.velocity_y.set(state["velocity"].y)


def test(frame):
    frame.call()


class SimulationFrame(ttk.Frame):
    def __init__(self, parent, width=512, height=512):
        super().__init__(parent, width=width, height=height)
        self.parent = parent
        self.pack(side="left", fill="both", padx=10, pady=10, expand=True)

        self.canvas = tk.Canvas(self, background="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.update_canvas_dimensions()

        self.velocity_x = tk.DoubleVar()
        self.velocity_y = tk.DoubleVar()

        self.current_body = None

        self.simulation_running = False
        self.physics_engine = physics.PhysicsEngine()
        self.speed_factor = 2

        self.mouse_positions = physics.DataPointList(2)
        self.canvas.tag_bind("body", "<ButtonPress-1>", self.body_press)
        self.canvas.tag_bind("body", "<B1-Motion>", self.body_drag_motion)
        self.canvas.tag_bind("body", "<ButtonRelease-1>", self.body_drag_release)

    def draw_square(self):
        square = shapes.draw_square(200, 100, 100, 100)
        self.physics_engine.add_rigid_body(square)
        self.draw_polygon(square.get_vertices(), outline="white")

    def draw_polygon(self, vertices, *args, **kwargs):
        tags = ("body", f"body_{id}")
        return self.canvas.create_polygon(*vertices, tags=tags, *args, **kwargs)

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

        if self.simulation_running:
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
            global frame
            test(frame)

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


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("512x512")

    canvas_frame = SimulationFrame(root)
    toolbar = Toolbar(root, canvas_frame)
    properties_frame = PropertiesFrame(root, canvas_frame)
    frame = properties_frame

    root.mainloop()
