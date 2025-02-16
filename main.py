import random
import math
from application import *
from coordinate import *

def draw_angle(canvas_name, width=1024, height=1024, scale=100):
    """Draw an angle on the given canvas."""
    center = Coordinate(width / 2, height / 2)
    angle = random.randint(20, 70)
    angle_2 = 0

    theta_radians = math.radians(angle)
    opposite = math.tan(theta_radians) * scale

    l1_end = Coordinate(center.x + scale, center.y)
    l2_end = Coordinate(center.x + scale, center.y - opposite)


    for arm in l1_end, l2_end:
        app.draw_canvas_object(
            canvas_name,
            "create_line",
            center.x, center.y,
            arm.x, arm.y,
            **line_properties
        )

        midpoint = center.midpoint(arm)
        app.draw_canvas_object(
            canvas_name,
            "create_text",
            *midpoint,
            text=center.distance(arm),
            fill='white',
            angle=angle
        )

    arc_size = 100
    arc_points = [
        center.x - arc_size / 2,
        center.y - arc_size / 2,
        center.x + arc_size / 2,
        center.y + arc_size / 2
    ]

    app.draw_canvas_object(canvas_name, "create_arc",
                           *arc_points, extent=angle, start=0,
                           outline="white", style=tk.ARC)


line_properties = {
    'fill': "white",
    'arrow': tk.LAST,
    'smooth': True,
    'width': 2
}

if __name__ == "__main__":
    app = Application(title="test", geometry="1024x1024")

    canvas = app.add_widget(
        "Canvas",
        bg="#000000",
        height=1024,
        width=1024
    )

    draw_angle(canvas)
    app.run()
