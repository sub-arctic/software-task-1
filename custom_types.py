from typing import Optional

from vec2 import Vec2, Vec2List

# Analogous to "Real"
type Scalar = int | float


class CollisionResult:
    """Stores the result of a collision check between two RigidBodies
    
    Attributes:
        collided: A boolean value that simply determines if the two bodies
            are in collision.
        Penetration: The depth of contact between two bodies; the minimum
            distance needed to resolve the collision.
        normal: The axis on which the penetration occurs.
        contacts: A list of vectors which are common between both bodies;
            points of contact. Typically limited to two with the current
            collision algorithm.
    """
    def __init__(
        self,
        collided: bool,
        penetration: Optional[Scalar] = 0,
        normal: Optional[Vec2] = None,
        contacts: Optional[Vec2List] = None,
    ):
        """Initializes the instance based on the result of a collision.

        Args:
            collided: Determine if this instance is in collision.
            Penetration: The depth of contact between two bodies; the minimum
                distance needed to resolve the collision.
            normal: The axis on which the penetration occurs.
            contacts: A list of vectors which are common between both bodies;
                points of contact. Typically limited to two with the current
                collision algorithm.
        """
        self.collided = collided
        self.penetration = penetration
        self.normal = normal
        self.contacts = contacts
