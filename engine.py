from itertools import combinations

import drawing
from bodies import Bodies
from collision import handle_collision
from custom_types import Scalar
from rigidbody import RigidBody
from vec2 import Vec2


class Engine:
    """A class to manage the physics engine, including bodies and gravity.

    Attributes:
        bodies: The collection of rigid bodies in the engine, which is an
            abstract class with id: body pairs.
        gravity: The gravitational acceleration affecting the bodies.
        canvas: The canvas on which the bodies are drawn (optional).
    """

    def __init__(self, gravity: Scalar = 9.81, canvas=None) -> None:
        """Initializes the Engine with a specified gravity and optional canvas.

        Args:
            gravity (Scalar): The gravitational acceleration. Defaults to 9.81.
            canvas: The canvas for rendering (optional).
        """
        self._bodies = Bodies()
        self._gravity: Scalar = gravity
        self.canvas = canvas

    @property
    def bodies(self) -> Bodies:
        """Gets the collection of bodies in the engine.

        Returns:
            The collection of rigid bodies.
        """
        return self._bodies

    @property
    def gravity(self) -> Scalar:
        """Gets the gravitational acceleration.

        Returns:
            The current gravitational acceleration.
        """
        return self._gravity

    @gravity.setter
    def gravity(self, new_gravity: Scalar) -> None:
        """Sets the gravitational acceleration.

        Args:
            new_gravity: The new gravitational acceleration.
        """
        self._gravity = new_gravity

    def __getitem__(self, id: int) -> RigidBody:
        """Gets a body by its ID.

        Args:
            id: The ID of the body to retrieve.

        Returns:
            The RigidBody object associated with the given ID.
        """
        return self.bodies[id]

    def get_body(self, id: int) -> RigidBody | None:
        """Returns a body given its ID.

        Args:
            id: The ID of the body to retrieve.

        Returns:
            The RigidBody object if found, otherwise None.
        """
        return self.bodies.get(id)

    def reset(self) -> None:
        """Clears all bodies from the engine."""
        self._bodies = Bodies()

    def create_bounds(self, dimensions: Vec2) -> list:
        """Creates a rectangular boundary as rigid bodies given dimensions.

        Args:
            dimensions: The x-y dimensions of the canvas.

        Returns:
            A list of four walls represented as RigidBody objects.
        """
        walls = [
            (dimensions.x, 1, 0, 0),
            (dimensions.x, 1, 0, dimensions.y),
            (1, dimensions.y, 0, 0),
            (1, dimensions.y, dimensions.x, 0),
        ]

        return [
            RigidBody(
                drawing.draw_rectangle(width, height),
                Vec2(x, y),
                Vec2(),
                mass=100,
                restitution=0.9,
            )
            for width, height, x, y in walls
        ]

    def update(self, delta_time: Scalar, dimensions: Vec2) -> None:
        """Updates the state of the engine, iterating through all bodies
            and resolving collisions.

        Bodies are iterated over in pairs using itertools. This could
        be done with two deep nested for loop, but itertools' solution
        is more elegant and performant.

        Args:
            delta_time: The time step to update over.
            dimensions: The x-y dimensions of the canvas.
        """
        walls = self.create_bounds(dimensions)
        for _, body in self.bodies:
            body.update(delta_time, gravity=self.gravity)
            for wall in walls:
                handle_collision(body, wall)
        # See docstring.
        for body_a, body_b in combinations(self.bodies, 2):
            body_a = body_a[1]
            body_b = body_b[1]
            handle_collision(body_a, body_b)
