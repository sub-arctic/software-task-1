import time
import tkinter as tk
from tkinter import ttk

import drawing
import physics

# TODO:
# implement basic "toolbar", for shape creation, relocation etc.
# potentially refactor SimulationCanvas into other classes
# split into simulation control, rendering, and event handling
# allow adding constant force arrows to shapes


class Application(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setup_grid()

        self.simulation_canvas = SimulationCanvas(self)
        self.properties_frame = PropertiesFrame(self)
        self.toolbar = Toolbar(self)

        self.simulation_canvas.grid(row=0, column=0, sticky="nsew")
        self.properties_frame.grid(row=0, column=1, sticky="nsew")
        self.toolbar.grid(row=1, column=0)

    def setup_grid(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="nsew")


class Toolbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.simulation_canvas = parent.simulation_canvas

        self.add_square_button = ttk.Button(
            self, text="Add square", command=self.simulation_canvas.draw_square
        )

        self.parent.play_pause_text = tk.StringVar()
        self.parent.play_pause_text.set("Play")
        self.play_pause_button = ttk.Button(
            self,
            text="Start",
            textvariable=self.parent.play_pause_text,
            command=self.simulation_canvas.play_pause_simulation,
        )

        self.force_arrows_toggle = ttk.Checkbutton(
            self, text="Force Arrows", variable=self.simulation_canvas.force_arrows
        )

        self.force_arrows_toggle.grid(column=2, row=1)
        self.play_pause_button.grid(column=0, row=1)
        self.add_square_button.grid(column=1, row=1)


class PropertiesFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(
            parent, text="Properties", borderwidth=3, relief=tk.RIDGE, padding=10
        )

        self.simulation_canvas = parent.simulation_canvas

        self.velocity = tk.StringVar()

        self.velocity_text = ttk.Label(self, textvariable=self.velocity)

        self.velocity_text.grid()

    def update_properties(self):
        if self.simulation_canvas.current_body is None:
            return
        state = self.simulation_canvas.current_body.get_state()

        velocity_x = round(state["velocity"].x)
        velocity_y = round(state["velocity"].y)

        self.velocity.set(f"x: {velocity_x}, y: {velocity_y}")


class SimulationCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, background="black")
        self.parent = parent

        self.update_dimensions()

        self.current_body = None
        self.bodies = None

        self.force_arrows = tk.IntVar(value=1)

        self.simulation_running = False
        self.physics_engine = physics.PhysicsEngine()
        self.speed_factor = 2

        self.mouse_positions = physics.DataPointList(2)
        self.tag_bind("body", "<ButtonPress-1>", self.body_press)
        self.tag_bind("body", "<B1-Motion>", self.body_drag_motion)
        self.tag_bind("body", "<ButtonRelease-1>", self.body_drag_release)

    def draw_square(self):
        square = drawing.draw_square(200, 100, 100, 100)
        id = self.draw_polygon(square.get_vertices(), outline="white")
        self.physics_engine.add_rigid_body(square, id)
        self.bodies = self.physics_engine.get_bodies()

    def draw_polygon(self, vertices, *args, **kwargs):
        tags = ("body", f"body_{id}")
        return self.create_polygon(*vertices, tags=tags, *args, **kwargs)

    def body_press(self, _):
        self.pressed_body_id = self.find_withtag("current")[0]
        self.current_body = self.physics_engine.get_body(self.pressed_body_id)
        self.itemconfigure(self.pressed_body_id, dash=(3, 5))

    def body_drag_motion(self, event):
        self.current_body = self.physics_engine.get_body(self.pressed_body_id)
        if self.current_body is None:
            return
        new_position = physics.Vector2D(event.x, event.y)
        new_velocity = physics.Vector2D(0, 0)

        self.current_body.move(new_position, new_velocity)

        time_ = time.perf_counter_ns()

        self.mouse_positions.add_data_point(time_, new_position)

    def body_drag_release(self, _):
        new_velocity = physics.calculate_velocity(self.mouse_positions)
        if self.current_body is None:
            return
        self.current_body.move(velocity=new_velocity)
        self.itemconfigure(self.pressed_body_id, dash=())

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

        self.update_dimensions()

        self.physics_engine.update(scaled_dt, self.canvas_width, self.canvas_height)
        if self.simulation_running:
            self.update()
            self.parent.after(int(dt * 1000 / self.speed_factor), self.step_simulation)
            self.parent.properties_frame.update_properties()
            self.draw_vector_lines()

    def clean_force_arrows(self):
        self.delete("vec_line")

    def draw_vector_lines(self):
        if self.bodies is None or self.force_arrows.get() == 0:
            self.clean_force_arrows()
            return
        for id, body in self.bodies.items():
            state = body.get_state()
            position = state["position"]
            velocity = state["velocity"]
            x, y = drawing.draw_velocity_arrows(position.x, position.y, velocity)

            if self.find_withtag(f"{id}_vec_line") != ():
                self.coords(f"{id}_vec_line_x", *x)
                self.coords(f"{id}_vec_line_y", *y)

            else:
                self.create_line(
                    *x,
                    fill="green",
                    arrow=tk.LAST,
                    tags=("vec_line", f"{id}_vec_line_x", f"{id}_vec_line"),
                )
                self.create_line(
                    *y,
                    fill="red",
                    arrow=tk.LAST,
                    tags=("vec_line", f"{id}_vec_line_y", "vec_line"),
                )

    def update(self):
        if self.bodies is None:
            return
        for id, body in self.bodies.items():
            vertices = []

            for vec in body.get_corners():
                vertices.extend([vec.x, vec.y])
            if self.find_withtag(id):
                self.coords(id, *vertices)

    def update_dimensions(self):
        self.canvas_width = self.winfo_width()
        self.canvas_height = self.winfo_height()


if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    Application(root)
    root.mainloop()
