import drawing
from typing import Optional
import rigidbody
import vec2

class BodyRenderer:
    def __init__(self, canvas: "SimulationCanvas", simulation_controller: "SimulationController") -> None:
        self.canvas = canvas
        self.simulation_controller = simulation_controller

    def create_polygon(self, position: Optional[vec2.Vec2] = None, velocity: Optional[vec2.Vec2] = None,
                       sides: int = 4, side_length: int = 100, angle: float = 0, mass: float = 5, restitution: float = 0.5) -> None:
        vertices = drawing.draw_polygon(side_length, sides)

        velocity = velocity if velocity is not None else vec2.Vec2()

        if position == "center" or position is None:
            self.canvas.update_dimensions()
            cwidth = self.canvas.width
            cheight = self.canvas.height
            if cwidth < 10 and cheight < 10:
                position = vec2.Vec2(200, 200)
            else:
                position = vec2.Vec2(cwidth / 2, cheight / 2)
        elif position == "bottom":
            self.canvas.update_dimensions()
            cwidth = self.canvas.width
            cheight = self.canvas.height
            if cwidth < 10 and cheight < 10:
                position = vec2.Vec2(200, 400)
            else:
                position = vec2.Vec2(cwidth / 2, cheight)


        body = rigidbody.RigidBody(
            vertices, position, velocity, angle, mass, restitution
        )
        canvas_id = self.draw_polygon(*body.get_vertices().unpack(), outline="white")
        self.simulation_controller.physics_engine.bodies.add(body, canvas_id)

    def draw_polygon(self, vertices: list[float], *args, **kwargs) -> int:
        tags = "body"
        return self.canvas.create_polygon(vertices, tags=tags, *args, **kwargs)

