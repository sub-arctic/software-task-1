from typing import Any, Optional

import physics
from custom_types import Scalar
from vec2 import Vec2, Vec2List


class RigidBody:
    """A class representing a rigid body in a physics simulation.

    A rigidbody is a two dimensional shape that has rigid physics;
    it's edges are 'strong' and cannot break. This is MUCH simpler
    to work with than soft body objects.

    Restitution is the elasticity coefficient. 0 is completely inelastic,
    and 1 is perfectly elastic. It determines the collision response between
    two RigidBodies.

    Attributes:
        vertices: The vertices of the body.
        position: The current position of the body.
        velocity: The current velocity of the body.
        angle: The current rotation angle of the body in radians.
        mass: The mass of the body.
        restitution: The restitution coefficient of the body.
        moment_of_inertia: The moment of inertia of the body.
        angular_velocity: The current angular velocity of the body.
        force: The accumulated force applied to the body.
        torque: The accumulated torque applied to the body.
        pinned: Indicates whether the body is pinned in place.
    """

    def __init__(
        self,
        vertices: Vec2List,
        position: Vec2,
        velocity: Vec2,
        angle: Scalar = 0,
        mass: Scalar = 5,
        restitution: Scalar = 0.5,
    ):
        """Initializes a RigidBody with the specified parameters.

        Args:
            vertices: The vertices of the body.
            position: The initial position of the body.
            velocity: The initial velocity of the body.
            angle: The initial rotation angle of the body in degrees.
                Defaults to 0.
            mass: The mass of the body. Defaults to 5.
            restitution: The restitution coefficient of the body.
                Defaults to 0.5.
        """
        self._vertices: Vec2List = vertices
        self._position: Vec2 = position
        self._velocity: Vec2 = velocity
        self._angle: Scalar = angle
        self._mass: Scalar = mass
        self._restitution: Scalar = restitution
        self.moment_of_inertia: Scalar = physics.compute_polygon_inertia(
            self.vertices, mass
        )
        self.angular_velocity: Scalar = 0
        self.force = Vec2()
        self.torque = 0
        self.pinned = False

    @property
    def velocity(self) -> Vec2:
        """Gets the current velocity of the body.

        Returns:
            The current velocity of the body.
        """
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity: Vec2):
        """Sets the current velocity of the body.

        Args:
            new_velocity: The new velocity to set.
        """
        self._velocity = new_velocity

    @property
    def angle(self) -> Scalar:
        """Gets the current rotation angle of the body.

        Returns:
            The current rotation angle in degrees.
        """
        return self._angle

    @angle.setter
    def angle(self, new_angle: Scalar):
        """Sets the current rotation angle of the body.

        Args:
            new_angle: The new angle to set in degrees.
        """
        self._angle = new_angle

    @property
    def mass(self) -> Scalar:
        """Gets the mass of the body.

        Returns:
            The mass of the body.
        """
        return self._mass

    @mass.setter
    def mass(self, new_mass: Scalar):
        """Sets the mass of the body.

        Args:
            new_mass: The new mass to set.
        """
        self._mass = new_mass

    @property
    def restitution(self) -> Scalar:
        """Gets the restitution coefficient of the body.

        Returns:
            The restitution coefficient.
        """
        return self._restitution

    @restitution.setter
    def restitution(self, new_restitution: Scalar):
        """Sets the restitution coefficient of the body.

        Args:
            new_restitution: The new restitution coefficient to set.

        Raises:
            ValueError: If the new restitution is not between 0 and 1.
        """
        if new_restitution < 0 or new_restitution > 1:
            raise ValueError("Restitution must be between 0 and 1")
        self._restitution = new_restitution

    @property
    def position(self) -> Vec2:
        """Gets the current position of the body.

        Returns:
            The current position of the body.
        """
        return self._position

    @position.setter
    def position(self, new_position: Vec2):
        """Sets the current position of the body.

        Args:
            new_position: The new position to set
        """
        self._position = new_position

    @property
    def vertices(self) -> Vec2List:
        """Gets the vertices of the body.

        Returns:
            The vertices of the body.
        """
        return self._vertices

    def get_vertices(self) -> Vec2List:
        """Calculates and returns the rotated vertices of the body based on
        its current angle and position.

        Returns:
            A Vec2List containing the transformed vertices of the body.
        """
        transformed_vertices = []
        for vertex in self.vertices:
            rotated_vertex = vertex.rotated(self.angle)
            translated_vertex = rotated_vertex + self.position
            transformed_vertices.append(translated_vertex)

        return Vec2List(transformed_vertices)

    def apply_force(self, force: Vec2, point: Optional[Vec2] = None) -> None:
        """Applies a force to the body at a specified point.

        Args:
            force: The force to apply to the body.
            point: The point of application of the force.
                If provided, torque will be calculated.
        """
        self.force = self.force + force
        if point is not None:
            r = point - self.position
            self.torque += r.cross(force)

    def pin(self, position: Optional[Vec2] = None) -> None:
        """Pins the body in place, preventing it from moving.

        Args:
            position: The position to pin the body to.
                If provided, updates the body's position.
        """
        if self.pinned:
            self.unpin()
            return

        if position is not None:
            self.position = position
        self.velocity = Vec2()
        self.angular_velocity = 0
        self.restitution = 0.9
        self.pinned = True

    def unpin(self) -> None:
        """Unpins the body, allowing it to move freely again."""
        self.pinned = False

    def update(self, delta_time: Scalar, gravity: Scalar = 9.8) -> None:
        """Updates the state of the body based on the elapsed time and gravity.

        Args:
            delta_time: The time step for the update.
            gravity: The gravitational acceleration to apply.
                Defaults to 9.8 m/s².
        """
        if self.pinned:
            return
        self.apply_force(Vec2(0, self.mass * gravity))

        acceleration = self.force / self.mass
        self.velocity = self.velocity + acceleration * delta_time
        self.position = self.position + self.velocity * delta_time

        angular_acc = self.torque / self.moment_of_inertia
        self.angular_velocity += angular_acc * delta_time
        self.angle += self.angular_velocity * delta_time

        self.force = Vec2()

    def get_state(self) -> dict[str, Any]:
        """Gets the current state of the body as a dictionary.

        Returns:
            A dictionary containing the position, velocity,
                angle, mass, and restitution of the body.
        """
        return {
            "position": self.position,
            "velocity": self.velocity,
            "angle": self.angle,
            "mass": self.mass,
            "restitution": self.restitution,
        }
