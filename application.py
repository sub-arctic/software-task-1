import tkinter as tk
from tkinter import ttk
from physics import RigidBody, PhysicsEngine, Vector2D
import math

class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.gravity_var = tk.DoubleVar(value=9.81)
        self.physics = PhysicsEngine(gravity=9.81)
        self.canvas_width = 512
        self.canvas_height = 512
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.grid(column=0, row=0, padx=24, pady=24, sticky='NSEW')

        # Debug checkbox to toggle drawing of velocity and force vectors
        self.show_debug = tk.BooleanVar(value=False)
        self.checkbox = ttk.Checkbutton(self, text="Show Debug Info", variable=self.show_debug)
        self.checkbox.grid(column=0, row=4, pady=5)

        self.label = ttk.Label(self, textvariable=self.gravity_var)
        self.label.grid(column=0, row=1)
        self.slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            value=9.81,
            orient=tk.HORIZONTAL,
            length=self.canvas_width,
            variable=self.gravity_var,
            command=self.update_gravity
        )
        self.slider.grid(column=0, row=2)
        self.play_button = ttk.Button(self, text='Play', command=self.start_simulation)
        self.play_button.grid(column=0, row=3)

        # Store the canvas IDs for the bodies and the debug info separately.
        self.object_canvas_ids = {}
        self.debug_canvas_ids = {}   # keyed by body id; each value is a list of canvas items (lines, texts)
        
        self.create_objects()
        self.draw_bounds()
        self.grid(padx=5, pady=10, sticky=tk.NSEW)
        self.running = False

    def update_gravity(self, val):
        self.physics.gravity = float(val)

    def create_objects(self):
        body1 = RigidBody(
            mass=2,
            bbox=(50, 30),
            position=Vector2D(100, 50),
            velocity=Vector2D(30, 0),
            restitution=0.7
        )
        body2 = RigidBody(
            mass=1,
            bbox=(40, 40),
            position=Vector2D(300, 100),
            velocity=Vector2D(-20, 10),
            restitution=0.7
        )
        body3 = RigidBody(
            mass=50,
            bbox=(100, 100),
            position=Vector2D(200, 300),
            velocity=Vector2D(0, -15),
            restitution=0.6
        )
        self.physics.add_rigid_body(body1)
        self.physics.add_rigid_body(body2)
        self.physics.add_rigid_body(body3)
        for item in self.physics.rigid_bodies:
            body = item["body"]
            canvas_id = self.draw_body(body)
            self.object_canvas_ids[item["id"]] = canvas_id

    def draw_bounds(self):
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, outline="red")

    def draw_body(self, body):
        corners = body.get_corners()
        points = []
        for corner in corners:
            points.extend([corner.x, corner.y])
        return self.canvas.create_polygon(points, outline="white", fill="")

    def update_canvas(self):
        # update moving bodies
        for item in self.physics.rigid_bodies:
            body = item["body"]
            body_id = item["id"]
            canvas_id = self.object_canvas_ids.get(body_id)
            if canvas_id is not None:
                corners = body.get_corners()
                points = []
                for corner in corners:
                    points.extend([corner.x, corner.y])
                self.canvas.coords(canvas_id, *points)

            # Remove previous debug drawings for this body (if any)
            if body_id in self.debug_canvas_ids:
                for dbg_id in self.debug_canvas_ids[body_id]:
                    self.canvas.delete(dbg_id)
                self.debug_canvas_ids[body_id] = []

            if self.show_debug.get():
                self.debug_canvas_ids.setdefault(body_id, [])
                # Calculate center for text label and base of the arrows.
                center = body.position

                # Velocity: decompose velocity into components.
                vx = body.velocity.x
                vy = body.velocity.y
                # Scaling factors to visualize arrows appropriately.
                vel_scale = 1
                force_scale = 0.1

                # Draw velocity x-component arrow (horizontal): red arrow.
                end_x = center.x + vx * vel_scale
                end_y = center.y
                line_vx = self.canvas.create_line(center.x, center.y, end_x, end_y,
                                                   fill="red", arrow=tk.LAST)
                self.debug_canvas_ids[body_id].append(line_vx)

                # Draw velocity y-component arrow (vertical): green arrow.
                end_x_y = center.x
                end_y_y = center.y + vy * vel_scale
                line_vy = self.canvas.create_line(center.x, center.y, end_x_y, end_y_y,
                                                   fill="green", arrow=tk.LAST)
                self.debug_canvas_ids[body_id].append(line_vy)

                # Calculate the magnitude and angle of the applied force (if any).
                force = body.force  # after update, normally force resets to 0
                force_magnitude = force.magnitude()
                # get angle in degrees for readability
                force_angle = math.degrees(math.atan2(force.y, force.x)) if force_magnitude != 0 else 0

                # Draw force arrow (blue) from the center (scaled)
                force_end_x = center.x + force.x * force_scale
                force_end_y = center.y + force.y * force_scale
                line_force = self.canvas.create_line(center.x, center.y, force_end_x, force_end_y,
                                                      fill="blue", arrow=tk.LAST)
                self.debug_canvas_ids[body_id].append(line_force)
                
                # Optionally, also show the velocity components.
                vel_text = f"Vx: {vx:.1f}\nVy: {vy:.1f}"
                text_vel_id = self.canvas.create_text(center.x, center.y + 20, text=vel_text,
                                                      fill="orange", font=("Arial", 10, "bold"))
                self.debug_canvas_ids[body_id].append(text_vel_id)

    def enforce_bounds(self):
        # Ensure bodies stay within canvas limits, applying collision with the canvas boundaries.
        for item in self.physics.rigid_bodies:
            body = item["body"]
            w, h = body.bbox
            radius = math.sqrt((w/2)**2 + (h/2)**2)
            restitution = body.restitution
            if body.position.x - radius < 0:
                body.position.x = radius
                if body.velocity.x < 0:
                    body.velocity.x = -body.velocity.x * restitution
            if body.position.x + radius > self.canvas_width:
                body.position.x = self.canvas_width - radius
                if body.velocity.x > 0:
                    body.velocity.x = -body.velocity.x * restitution
            if body.position.y - radius < 0:
                body.position.y = radius
                if body.velocity.y < 0:
                    body.velocity.y = -body.velocity.y * restitution
            if body.position.y + radius > self.canvas_height:
                body.position.y = self.canvas_height - radius
                if body.velocity.y > 0:
                    body.velocity.y = -body.velocity.y * restitution

    def simulation_step(self):
        dt = 0.016
        self.physics.update(dt)
        self.enforce_bounds()
        self.update_canvas()
        if self.running:
            self.after(16, self.simulation_step)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.simulation_step()
