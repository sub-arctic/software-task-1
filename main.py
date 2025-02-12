import random
import math
from application import *
from coordinate import *



def draw_angle(canvas_name, width=1024, height=1024, scale=100):
    """Draw an angle on the given canvas."""
    center = Coordinate(width / 2, height / 2)
    angle = random.randint(20, 70)
    theta_radians = math.radians(angle)
    opposite = math.tan(theta_radians) * scale

    l1_end = Coordinate(center.x + scale, center.y)
    l2_end = Coordinate(center.x + scale, center.y - opposite)

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

    ## Bad implementation, but looks cool :)
    # for line in "l1", "l2":
    #     arm_points = [
    #         center.x, center.y,
    #         locals()[line+"_end"].x, locals()[line+"_end"].y
    #     ] # this is bad practice, but $line range is known
    #     locals()["arm_"+line] = app.draw_canvas_object(
    #        canvas,
    #        "create_line",
    #        arm_points,
    #        **line_properties
    #     )
    # Less concise but probably more perfomant
    arm_1 = app.draw_canvas_object(
        canvas_name,
        "create_line",
        center.x, center.y,
        l1_end.x, l1_end.y,
        **line_properties
    )

    arm_2 = app.draw_canvas_object(
        canvas_name,
        "create_line",
        center.x, center.y,
        l2_end.x, l2_end.y,
        **line_properties
    )

    offset = 20
    p1 = Coordinate(center.x-offset, center.y)
    p2 = Coordinate(l2_end.x-offset, l2_end.y)

    midpoint = p1.midpoint(p2)

    
    app.draw_canvas_object(
        canvas_name,
        "create_text",
        *midpoint,
        text=center.distance(l2_end),
        fill='white',
        angle=angle
    )
    midpoint = center.midpoint(l1_end)
    midpoint.y += offset

    app.draw_canvas_object(
        canvas_name,
        "create_text",
        *midpoint,
        text=center.distance(l1_end),
        fill='white',
        angle=0
    )

    return arm_1, arm_2

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
