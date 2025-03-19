import math

from custom_types import Scalar
from vec2 import Vec2, Vec2List


def calculate_side_length(n: int, side_length: Scalar) -> Scalar:
    """Calculate the side length of a regular polygon given the number of sides and side length of a square."""

    # Calculate the circumradius (r) using the side length for a square (n=4)
    r = side_length / (2 * math.sin(math.pi / 4))
    
    # Calculate the side length for the polygon with n sides
    return 2 * r * math.sin(math.pi / n)

def draw_polygon(side_length: Scalar, sides: int) -> Vec2List:
    """Creates a polygon defined by vectors given quantity and length of sides

    The polygon is expected to be regular, meaning all sides are of equal length
    and all interior angles are equivalent. The radius of the circumcircle, which
    is a circle that passes through all vertices, grows exponentially given higher
    side counts.

    Args:
        side_length: The length of each equivalent side of the polygon.
        sides: The quantity of sides

    Returns:
        A list of vectors defining the vertices of the polygon.

    """
    # Derives relationship between side length of a regular polygon and the
    # radius of its circumcircle.
    circumcircle_radius: Scalar = side_length / (2 * math.sin(math.pi / sides))
    vertices: Vec2List = Vec2List()

    for i in range(sides):
        xi: Scalar = circumcircle_radius * math.cos((2 * math.pi * i) / sides)
        yi: Scalar = circumcircle_radius * math.sin((2 * math.pi * i) / sides)
        vertices.append(Vec2(xi, yi))

    return vertices


def draw_rectangle(width: Scalar, height: Scalar) -> Vec2List:
    """Creates a rectangle defined by vertices given dimensions.

    Used for bounding boxes.
    
    Args:
        width: The width of the rectangle.
        height: The height of the rectangle.

    Returns:
        A list of vectors defining the vertices of the rectangle.
    """
    vertices = Vec2List()
    vertices.append(Vec2(0, 0))
    vertices.append(Vec2(width, 0))
    vertices.append(Vec2(width, height))
    vertices.append(Vec2(0, height))
    return vertices
