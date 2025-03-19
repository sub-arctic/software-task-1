import time

from datapoint import DataPointList
from rigidbody import RigidBody
import physics
import vec2


class InteractionManager:
    """Handles all user-based interaction with bodies on the canvas.

    Attributes:
        canvas: A tkinter canvas element, which is where the handlers
            will be bound to.
        current_body: Keeps track of the currently pressed body for
            dragging and related updates.
        last_body: Keeps track of the last pressed body for highlighting
            purposes.
        mouse_positions: Stores cursor position data paired with time for
            velocity calculations, used to update the velocity of the dragged
            object on release.
        simulation_controller: Parent object used to reference all RigidBodies
            and call related functions for updating.

    """
    def __init__(self, canvas, simulation_controller) -> None:
        """Initializes the instance given parent elements"""
        self.canvas = canvas
        self.current_body = None
        self.last_body = None
        self.mouse_positions = DataPointList(2)
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

    def search_body(self) -> RigidBody | None:
        self.pressed_body_id = self.canvas.find_withtag("current")[0]
        self.current_body = self.simulation_controller.physics_engine.get_body(
            self.pressed_body_id
        )
        return self.current_body

    def body_press(self, _) -> None:
        self.search_body()
        if self.current_body is not None:
            if self.current_body == self.last_body:
                self.canvas.itemconfigure(self.pressed_body_id, fill="red")
                self.last_body = None
            else:
                if self.last_body is not None:
                    self.canvas.itemconfigure(self.last_body, fill=self.canvas.polygon_fill)
                self.canvas.itemconfigure(self.pressed_body_id, fill="red")
                self.last_body = self.pressed_body_id

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
