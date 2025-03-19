from __future__ import annotations
import tkinter as tk
import engine
import vec2
from renderer import BodyRenderer
from interaction_manager import InteractionManager

DELTA_TIME = 0.016
SPEED_FACTOR = 3

class Controller:
    """Controls the simulation step and manages the physics engine.

    This class is responsible for updating the physics engine and the canvas
    during each simulation step. It handles the simulation's running state,
    gravity, and speed factor.

    Attributes:
        running: A boolean indicating whether the simulation is currently running.
        dt: The time step for the simulation.
        speed: The speed factor for the simulation.
        canvas: The canvas on which the simulation is rendered.
        physics_engine: The physics engine that handles the simulation logic.
    """

    def __init__(self, canvas) -> None:
        self.running = False
        self.dt = DELTA_TIME
        self.speed = SPEED_FACTOR
        self.canvas = canvas
        self.physics_engine = engine.Engine(canvas=self.canvas)

    def step(self) -> None:
        """Performs a single step in the simulation.

        This method updates the physics engine and the canvas based on the
        current time step and speed factor. If the simulation is running,
        it schedules the next step using the Tkinter after method.
        """
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
        """Resets the simulation to its initial state.

        This method stops the simulation, resets the physics engine, and clears
        the canvas.
        """
        self.dt = DELTA_TIME
        self.running = False
        self.speed = SPEED_FACTOR
        self.physics_engine.reset()
        self.canvas.delete("all")

    def update(self) -> None:
        """Updates the positions of all bodies in the simulation.

        This method retrieves the current positions of the bodies from the
        physics engine and updates their coordinates on the canvas.
        """
        for id, body in self.physics_engine.bodies:
            self.canvas.coords(id, *body.get_vertices().unpack())

    def set_gravity(self, new_gravity: str) -> None:
        """Sets the gravity for the physics engine.

        Args:
            new_gravity: A string representing the new gravity value to be set.
        """
        self.physics_engine.gravity = float(new_gravity)

    def set_speed_factor(self, value: str) -> None:
        """Sets the speed factor for the simulation.

        Args:
            value: A string representing the new speed factor to be set.
        """
        self.speed = float(value)


class Canvas(tk.Canvas):
    """A canvas for rendering the simulation.

    This class extends the Tkinter Canvas to provide additional functionality
    for rendering the simulation, including managing the controller and
    interaction manager.

    Attributes:
        parent: The parent widget of this canvas.
        width: The width of the canvas.
        height: The height of the canvas.
        simulation_controller: The controller that manages the simulation.
        body_renderer: The renderer responsible for drawing bodies on the canvas.
        interaction_manager: The manager that handles user interactions with the canvas.

    Args:
        parent: The parent widget to which this canvas will be attached.
    """

    def __init__(self, parent) -> None:
        self.parent = parent
        super().__init__(self.parent)
        self.width = 800
        self.height = 600
        self.config(width=self.width, height=self.height)
        self.simulation_controller = Controller(self)
        self.body_renderer = BodyRenderer(self, self.simulation_controller)
        self.interaction_manager = InteractionManager(self, self.simulation_controller)
        self.interaction_manager.setup_handlers()
        self.grid(row=0, column=1, sticky="nsew")

    def update_dimensions(self) -> None:
        """Updates the dimensions of the canvas based on its current size.

        This method retrieves the current width and height of the canvas
        and updates the corresponding attributes.
        """
        self.width = self.winfo_width()
        self.height = self.winfo_height()

