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


class SimulationCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, background="black")

        self.parent = parent

        self.simulation_controller = SimulationController(self)

        self.body_renderer = BodyRenderer(self, self.simulation_controller)

        self.interaction_manager = InteractionManager(self, self.simulation_controller)

        self.interaction_manager.setup_handlers()

    def update_dimensions(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()


class SimulationController:
    def __init__(self, canvas):
        self.dt = 0.016
        self.running = False

        self.force_arrows = tk.IntVar(value=1)

        self.canvas = canvas

        self.physics_engine = physics.PhysicsEngine()
        self.bodies = self.physics_engine.get_bodies()

    def step(self, dt=0.016, speed_factor=2):
        scaled_dt = dt * speed_factor

        self.canvas.update_dimensions()

        self.physics_engine.update(scaled_dt, self.canvas.width, self.canvas.height)
        if self.running:
            self.update()
            self.canvas.after(int(dt * 1000 / speed_factor), self.step)
            self.canvas.parent.properties_frame.update_properties()
            self.canvas.body_renderer.draw_vector_lines()

    def update(self):
        if self.bodies is None:
            return
        for id, body in self.bodies.items():
            vertices = []

            for vec in body.get_corners():
                vertices.extend([vec.x, vec.y])
            if self.canvas.find_withtag(id):
                self.canvas.coords(id, *vertices)


class BodyRenderer:
    def __init__(self, canvas, simulation_controller):
        self.canvas = canvas
        self.simulation_controller = simulation_controller

    def clean_force_arrows(self):
        self.canvas.delete("vec_line")

    def draw_vector_lines(self):
        if (
            self.simulation_controller.bodies is None
            or self.simulation_controller.force_arrows.get() == 0
        ):
            self.clean_force_arrows()
            return
        for id, body in self.simulation_controller.bodies.items():
            state = body.get_state()
            position = state["position"]
            velocity = state["velocity"]
            x, y = drawing.draw_velocity_arrows(position.x, position.y, velocity)

            if self.canvas.find_withtag(f"{id}_vec_line") != ():
                self.canvas.coords(f"{id}_vec_line_x", *x)
                self.canvas.coords(f"{id}_vec_line_y", *y)
            else:
                self.canvas.create_line(
                    *x,
                    arrow=tk.LAST,
                    fill="green",
                    tags=("vec_line", f"{id}_vec_line_x", f"{id}_vec_line"),
                )
                self.canvas.create_line(
                    *y,
                    arrow=tk.LAST,
                    fill="red",
                    tags=("vec_line", f"{id}_vec_line_y", f"{id}_vec_line"),
                )

    def draw_square(self):
        square = drawing.draw_square(200, 100, 100, 100)
        id = self.draw_polygon(square.get_vertices(), outline="white")
        self.simulation_controller.physics_engine.add_rigid_body(square, id)
        self.simulation_controller.bodies = (
            self.simulation_controller.physics_engine.get_bodies()
        )

    def test(self):
        polygon = drawing.draw_polygon(200, 100, 50, 4)
        id = self.draw_polygon(polygon.get_vertices(), outline="white")
        self.simulation_controller.physics_engine.add_rigid_body(polygon, id)
        self.simulation_controller.bodies = (
            self.simulation_controller.physics_engine.get_bodies()
        )

    def draw_polygon(self, vertices, *args, **kwargs):
        tags = ("body", f"body_{id}")
        return self.canvas.create_polygon(*vertices, tags=tags, *args, **kwargs)


class InteractionManager:
    def __init__(self, canvas, simulation_controller):
        self.canvas = canvas

        self.current_body = None

        self.simulation_controller = simulation_controller
        self.mouse_positions = physics.DataPointList(2)
        self.dt = 0.016

    def setup_handlers(self):
        self.canvas.tag_bind("body", "<ButtonPress-1>", self.body_press)
        self.canvas.tag_bind("body", "<B1-Motion>", self.body_drag_motion)
        self.canvas.tag_bind("body", "<ButtonRelease-1>", self.body_drag_release)

    def play_pause(self):
        if self.simulation_controller.running:
            self.simulation_controller.running = False
            self.canvas.parent.play_pause_text.set("Play")
        else:
            self.simulation_controller.running = True
            self.canvas.parent.play_pause_text.set("Pause")
            self.simulation_controller.step(self.dt)

    def body_press(self, _):
        self.pressed_body_id = self.canvas.find_withtag("current")[0]
        self.current_body = self.simulation_controller.physics_engine.get_body(
            self.pressed_body_id
        )
        self.canvas.itemconfigure(self.pressed_body_id, dash=(3, 5))

    def body_drag_motion(self, event):
        self.current_body = self.simulation_controller.physics_engine.get_body(
            self.pressed_body_id
        )
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
        self.canvas.itemconfigure(self.pressed_body_id, dash=())


class Toolbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.simulation_canvas = parent.simulation_canvas

        self.parent.play_pause_text = tk.StringVar()

        self.add_square_button = ttk.Button(
            self,
            text="Add square",
            command=self.simulation_canvas.body_renderer.test,
        )

        self.parent.play_pause_text = tk.StringVar()
        self.parent.play_pause_text.set("Play")
        self.play_pause_button = ttk.Button(
            self,
            text="Start",
            textvariable=self.parent.play_pause_text,
            command=self.simulation_canvas.interaction_manager.play_pause,
        )

        self.force_arrows_toggle = ttk.Checkbutton(
            self,
            text="Force Arrows",
            variable=self.simulation_canvas.simulation_controller.force_arrows,
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
        if self.simulation_canvas.interaction_manager.current_body is None:
            return
        state = self.simulation_canvas.interaction_manager.current_body.get_state()

        velocity_x = round(state["velocity"].x)
        velocity_y = round(state["velocity"].y)

        self.velocity.set(f"x: {velocity_x}, y: {velocity_y}")


if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    Application(root)
    root.mainloop()
