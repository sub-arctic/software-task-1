import time
import tkinter as tk
from tkinter import ttk
import os
from markdown import MarkdownParser
import datapoint
import drawing
import engine
import physics
import rigidbody
import vec2
from typing import Optional

DELTA_TIME = 0.016
SPEED_FACTOR = 3


LESSONS_PATH = "lessons"

class Application(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.setup_grid()

        self.lesson_frame = LessonFrame(self)
        self.simulation_canvas = SimulationCanvas(self)

        self.toolbar = Toolbar(self)
        self.toolbar.grid(row=1, column=1, sticky="nsew")

        self.lesson_manager = LessonManager(self, self.lesson_frame, self.simulation_canvas)
        self.lesson_manager.load_lesson("gravity.md")

    def setup_grid(self) -> None:
        self.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)


class SimulationCanvas(tk.Canvas):
    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent
        super().__init__(self.parent, background="black")
        self.simulation_controller = SimulationController(self)
        self.body_renderer = BodyRenderer(self, self.simulation_controller)
        self.interaction_manager = InteractionManager(self, self.simulation_controller)
        self.interaction_manager.setup_handlers()
        self.grid(row=0, column=1, sticky="nsew")

    def update_dimensions(self) -> None:
        self.width = self.winfo_width()
        self.height = self.winfo_height()


class SimulationController:
    def __init__(self, canvas: SimulationCanvas) -> None:
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

    def update(self) -> None:
        for id, body in self.physics_engine.bodies:
            self.canvas.coords(id, *body.get_vertices().unpack())

    def set_gravity(self, new_gravity: str) -> None:
        self.physics_engine.gravity = float(new_gravity)

    def set_speed_factor(self, value: str) -> None:
        self.speed = float(value)


class BodyRenderer:
    def __init__(self, canvas: SimulationCanvas, simulation_controller: SimulationController) -> None:
        self.canvas = canvas
        self.simulation_controller = simulation_controller

    def create_polygon(self, position: Optional[vec2.Vec2] = None, velocity: Optional[vec2.Vec2] = None,
                       sides: int = 4, side_length: int = 100, angle: float = 0, mass: float = 5, restitution: float = 0.5) -> None:
        vertices = drawing.draw_polygon(side_length, sides)

        velocity = velocity if velocity is not None else vec2.Vec2()

        if position == "center" or position is None:
            self.canvas.update_dimensions()
            cwidth = self.canvas.width
            cheight = self.canvas.height
            if cwidth < 10 and cheight < 10:
                position = vec2.Vec2(200, 200)
            else:
                position = vec2.Vec2(cwidth / 2, cheight / 2)

        body = rigidbody.RigidBody(
            vertices, position, velocity, angle, mass, restitution
        )
        canvas_id = self.draw_polygon(*body.get_vertices().unpack(), outline="white")
        self.simulation_controller.physics_engine.bodies.add(body, canvas_id)

    def draw_polygon(self, vertices: list[float], *args, **kwargs) -> int:
        tags = "body"
        return self.canvas.create_polygon(vertices, tags=tags, *args, **kwargs)


class InteractionManager:
    def __init__(self, canvas: SimulationCanvas, simulation_controller: SimulationController) -> None:
        self.canvas = canvas
        self.current_body = None
        self.mouse_positions = datapoint.DataPointList(2)
        self.simulation_controller = simulation_controller

    def setup_handlers(self) -> None:
        self.canvas.tag_bind("body", "<ButtonPress-1>", self.body_press)
        self.canvas.tag_bind("body", "<ButtonPress-3>", self.body_pin)
        self.canvas.tag_bind("body", "<B1-Motion>", self.body_drag_motion)
        self.canvas.tag_bind("body", "<ButtonRelease-1>", self.body_drag_release)

    def play_pause(self) -> None:
        if self.simulation_controller.running:
            self.simulation_controller.running = False
            self.canvas.parent.play_pause_text.set("Play")
        else:
            self.simulation_controller.running = True
            self.canvas.parent.play_pause_text.set("Pause")
            self.simulation_controller.step()

    def search_body(self) -> rigidbody.RigidBody:
        self.pressed_body_id = self.canvas.find_withtag("current")[0]
        self.current_body = self.simulation_controller.physics_engine.get_body(
            self.pressed_body_id
        )
        return self.current_body

    def body_press(self, _) -> None:
        self.search_body()
        if self.current_body is not None:
            self.canvas.itemconfigure(self.pressed_body_id, dash=(3, 5))

    def body_pin(self, event) -> None:
        self.search_body()
        if self.current_body is not None:
            self.current_body.pin(vec2.Vec2(event.x, event.y))

    def body_drag_motion(self, event) -> None:
        self.search_body()
        if self.current_body is None:
            return
        new_position = vec2.Vec2(event.x, event.y)
        new_velocity = vec2.Vec2(0, 0)

        self.current_body.position = new_position
        self.current_body.velocity = new_velocity

        time_ = time.perf_counter_ns()

        self.mouse_positions.add_data_point(time_, new_position)

    def body_drag_release(self, _) -> None:
        new_velocity = physics.calculate_velocity(self.mouse_positions)
        if self.current_body is None:
            return
        self.current_body.velocity = new_velocity
        self.canvas.itemconfigure(self.pressed_body_id, dash=())


class Toolbar(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.simulation_canvas = parent.simulation_canvas
        self.parent.play_pause_text = tk.StringVar()

        self.add_square_button = ttk.Button(
            self,
            text="Add polygon",
            command=self.simulation_canvas.body_renderer.create_polygon,
        )

        self.gravity_scale = ttk.Scale(
            self,
            command=self.simulation_canvas.simulation_controller.set_gravity,
            from_=0,
            to=20,
            value=9.89,
            orient=tk.HORIZONTAL,
        )

        self.speed_factor_scale = ttk.Scale(
            self,
            command=self.set_speed_factor,
            from_=0.1,
            to=10.0,
            value=SPEED_FACTOR,
            orient=tk.HORIZONTAL,
        )

        self.parent.play_pause_text.set("Play")
        self.play_pause_button = ttk.Button(
            self,
            text="Start",
            textvariable=self.parent.play_pause_text,
            command=self.simulation_canvas.interaction_manager.play_pause,
        )

        self.play_pause_button.grid(column=0, row=1)
        self.add_square_button.grid(column=1, row=1)
        self.gravity_scale.grid(column=2, row=1)
        self.speed_factor_scale.grid(column=3, row=1)

        self.gravity_label = ttk.Label(self, text="Gravity")
        self.gravity_label.grid(column=2, row=0)
        self.speed_factor_label = ttk.Label(self, text="Speed Factor")
        self.speed_factor_label.grid(column=3, row=0)

        self.gravity_value_label = ttk.Label(self, text=str(self.gravity_scale.get()))
        self.gravity_value_label.grid(column=2, row=2)
        self.speed_factor_value_label = ttk.Label(self, text=str(self.speed_factor_scale.get()))
        self.speed_factor_value_label.grid(column=3, row=2)

        self.gravity_scale.config(command=self.update_gravity_value)
        self.speed_factor_scale.config(command=self.update_speed_factor_value)

    def set_speed_factor(self, value: str) -> None:
        self.simulation_canvas.simulation_controller.set_speed_factor(value)

    def update_gravity_value(self, value: str) -> None:
        self.gravity_value_label.config(text=str(value))

    def update_speed_factor_value(self, value: str) -> None:
        self.speed_factor_value_label.config(text=str(value))


class LessonFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent
        super().__init__(self.parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(sticky="nsew")
        self.parser = MarkdownParser(self.content_frame)

    def display_lesson(self, markdown_text: str) -> None:
        self.parser.parse(markdown_text)
        if self.parser.bodies is None:
            return
        for body in self.parser.bodies:
            for _, properties in body.items():
                self.parent.simulation_canvas.body_renderer.create_polygon(**properties)


class LessonManager:
    def __init__(self, parent: tk.Widget, lesson_frame: LessonFrame, simulation_canvas: SimulationCanvas) -> None:
        self.parent = parent
        self.lesson_frame = lesson_frame
        self.simulation_canvas = simulation_canvas
        self.lesson_selector = ttk.Combobox(parent, state="readonly")

        self.lesson_files = [f for f in os.listdir(LESSONS_PATH) if f.endswith(".md")]
        self.lesson_selector["values"] = self.lesson_files
        self.lesson_selector.grid(row=1, column=0, pady=10)
        self.lesson_selector.bind("<<ComboboxSelected>>", self.switch_lesson)
        if self.lesson_files:
            self.lesson_selector.current(0)

    def load_lesson(self, lesson_file: str) -> None:
        lesson_path = os.path.join(LESSONS_PATH, lesson_file)
        if os.path.exists(lesson_path):
            with open(lesson_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()
            self.lesson_frame.display_lesson(markdown_text)

    def switch_lesson(self, _) -> None:
        selected_lesson = self.lesson_selector.get()
        self.load_lesson(selected_lesson)

