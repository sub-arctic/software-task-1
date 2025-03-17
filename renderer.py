from typing import Optional

import drawing
import rigidbody
from simulation_canvas import SimulationCanvas
from simulation_controller import SimulationController
from vec2 import Vec2


class BodyRenderer:
    """A class to render bodies in a simulation canvas.

    Attributes:
        canvas (SimulationCanvas): The canvas on which bodies are drawn.
        simulation_controller (SimulationController): The controller managing the simulation.
    """

    def __init__(
        self, canvas: SimulationCanvas, simulation_controller: SimulationController
    ) -> None:
        """Initializes the BodyRenderer with a canvas and a simulation controller.

        Args:
            canvas (Canvas): The canvas for rendering.
            simulation_controller (Controller): The controller for the simulation.
        """
        self.canvas = canvas
        self.simulation_controller = simulation_controller

    def create_polygon(
        self,
        position: Optional[Vec2] = None,
        velocity: Optional[Vec2] = None,
        sides: int = 4,
        side_length: int = 100,
        angle: float = 0,
        mass: float = 5,
        restitution: float = 0.5,
    ) -> None:
        """Creates a polygonal rigid body and adds it to the simulation.

        Args:
            position (Optional[Vec2]): The initial position of the body. If "center" or None, the body is centered on the canvas.
            velocity (Optional[Vec2]): The initial velocity of the body. Defaults to a zero vector if None.
            sides (int): The number of sides of the polygon. Defaults to 4 (a square).
            side_length (int): The length of each side of the polygon. Defaults to 100.
            angle (float): The initial rotation angle of the body in radians. Defaults to 0.
            mass (float): The mass of the body. Defaults to 5.
            restitution (float): The restitution coefficient for the body. Defaults to 0.5.
        """
        vertices = drawing.draw_polygon(side_length, sides)

        velocity = velocity if velocity is not None else Vec2()

        if position == "center" or position is None:
            self.canvas.update_dimensions()
            cwidth = self.canvas.width
            cheight = self.canvas.height
            if cwidth < 10 and cheight < 10:
                position = Vec2(200, 200)
            else:
                position = Vec2(cwidth / 2, cheight / 2)
        elif position == "bottom":
            self.canvas.update_dimensions()
            cwidth = self.canvas.width
            cheight = self.canvas.height
            if cwidth < 10 and cheight < 10:
                position = Vec2(200, 400)
            else:
                position = Vec2(cwidth / 2, cheight)

        body = rigidbody.RigidBody(
            vertices, position, velocity, angle, mass, restitution
        )
        canvas_id = self.draw_polygon(*body.get_vertices().unpack(), outline="white")
        self.simulation_controller.physics_engine.bodies.add(body, canvas_id)

    def draw_polygon(self, vertices: list[float], *args, **kwargs) -> int:
        """Draws a polygon on the canvas and returns its ID.

        Args:
            vertices (list[float]): The list of vertex coordinates for the polygon.
            *args: Additional positional arguments for the drawing function.
            **kwargs: Additional keyword arguments for the drawing function.

        Returns:
            int: The ID of the drawn polygon on the canvas.
        """
        tags = "body"
        return self.canvas.create_polygon(vertices, tags=tags, *args, **kwargs)
