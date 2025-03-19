from typing import Optional
import tkinter as tk
from custom_types import Scalar

import drawing
import rigidbody
from vec2 import Vec2



class BodyRenderer:
    """A class to render bodies in a simulation canvas.

    Attributes:
        canvas: The canvas on which bodies are drawn.
        simulation_controller: The controller managing the simulation.
    """

    def __init__(
        self, canvas, simulation_controller
    ) -> None:
        """Initializes the BodyRenderer with a canvas and a simulation controller.

        Args:
            canvas: The canvas for rendering.
            simulation_controller: The controller for the simulation.
        """
        self.canvas = canvas
        self.simulation_controller = simulation_controller
        self.default_polygon_sides = tk.IntVar()
        self.default_polygon_size = tk.DoubleVar()
        self.default_polygon_mass = tk.DoubleVar()

        self.default_polygon_sides.set(4)
        self.default_polygon_size.set(100)
        self.default_polygon_mass.set(5)

    def create_polygon(
        self,
        position: Optional[Vec2] = None,
        velocity: Optional[Vec2] = None,
        sides: int = 4,
        side_length: Scalar = 100,
        angle: float = 0,
        mass: float = 5,
        restitution: float = 0.5,
    ) -> None:
        """Creates a polygonal rigid body and adds it to the simulation.

        Args:
            position: The initial position of the body. If "center" or None,
                the body is centered on the canvas.
            velocity: The initial velocity of the body. Defaults to a zero vector 
                if None.
            sides: The number of sides of the polygon. Defaults to 4 (a square).
            side_length: The length of each side of the polygon. Defaults to 100.
            angle: The initial rotation angle of the body in radians. Defaults to 0.
            mass: The mass of the body. Defaults to 5.
            restitution: The restitution coefficient for the body. Defaults to 0.5.
        """
        sides = self.default_polygon_sides.get()
        side_length = drawing.calculate_side_length(
            sides, self.default_polygon_size.get()
        )
        mass = self.default_polygon_mass.get()
        vertices = drawing.draw_polygon(side_length, sides)

        velocity = velocity if velocity is not None else Vec2()

        # Bad fix for cwidth and cheight not being set.
        if position == "center" or position is None:
            self.canvas.update_dimensions()
            cwidth = self.canvas.width
            cheight = self.canvas.height
            if cwidth < 10 and cheight < 10:
                position = Vec2(100, 100)
            else:
                position = Vec2(cwidth / 2, cheight / 2)
        elif position == "bottom":
            self.canvas.update_dimensions()
            cwidth = self.canvas.width
            cheight = self.canvas.height
            if cwidth < 10 and cheight < 10:
                position = Vec2(100, 100)
            else:
                position = Vec2(cwidth / 2, cheight)

        body = rigidbody.RigidBody(
            vertices, position, velocity, angle, mass, restitution
        )
        canvas_id = self.draw_polygon(
            *body.get_vertices().unpack(),
            outline=self.canvas.polygon_outline,
            fill=self.canvas.polygon_fill
        )
        self.simulation_controller.physics_engine.bodies.add(body, canvas_id)

    def draw_polygon(self, vertices: list[float], *args, **kwargs) -> int:
        """Draws a polygon on the canvas and returns its ID.

        Args:
            vertices: The list of vertex coordinates for the polygon.
            *args: Additional positional arguments for the drawing function.
            **kwargs: Additional keyword arguments for the drawing function.

        Returns:
            The ID of the drawn polygon on the canvas.
        """
        tags = "body"
        return self.canvas.create_polygon(vertices, tags=tags, *args, **kwargs)
