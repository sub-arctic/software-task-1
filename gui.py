import tkinter as tk
from tkinter import ttk

from physics import PhysicsEngine, RigidBody, Vector2D


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.canvas_width = 512
        self.canvas_height = 512
        self.canvas = tk.Canvas(self, width=self.canvas_width,
                                height=self.canvas_height, bg='black')
        self.canvas.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        self.gravity_var = tk.DoubleVar(value=9.81)
        self.physics = PhysicsEngine(gravity=9.81)

        self.play_button = ttk.Button(
            self.control_frame, text="Play", command=self.start_simulation)
        self.play_button.pack(pady=2)
        self.pause_button = ttk.Button(
            self.control_frame, text="Pause", command=self.pause_simulation)
        self.pause_button.pack(pady=2)
        self.new_shape_button = ttk.Button(
            self.control_frame, text="New Rectangle", command=self.create_new_shape)
        self.new_shape_button.pack(pady=2)
        self.new_polygon_button = ttk.Button(
            self.control_frame, text="New Polygon", command=self.create_new_polygon)
        self.new_polygon_button.pack(pady=2)
        self.reset_button = ttk.Button(
            self.control_frame, text="Reset Canvas", command=self.reset_canvas)
        self.reset_button.pack(pady=2)

        ttk.Label(self.control_frame, text="Gravity").pack(pady=2)
        self.gravity_slider = ttk.Scale(self.control_frame, from_=0, to=100,
                                        orient=tk.HORIZONTAL, variable=self.gravity_var,
                                        command=lambda val: self.update_gravity(val))
        self.gravity_slider.pack(pady=2)
        self.gravity_val_label = ttk.Label(
            self.control_frame, text=f"{self.gravity_var.get():.2f}")
        self.gravity_val_label.pack(pady=2)
        self.gravity_var.trace(
            "w", lambda *args: self.gravity_val_label.config(text=f"{self.gravity_var.get():.2f}"))

        ttk.Label(self.control_frame, text="Air Resistance").pack(pady=2)
        self.air_resistance_var = tk.DoubleVar(value=0.1)
        self.air_resistance_slider = ttk.Scale(self.control_frame, from_=0, to=1,
                                               orient=tk.HORIZONTAL, variable=self.air_resistance_var,
                                               command=lambda val: self.update_air_resistance(val))
        self.air_resistance_slider.pack(pady=2)
        self.air_resistance_val_label = ttk.Label(
            self.control_frame, text=f"{self.air_resistance_var.get():.2f}")
        self.air_resistance_val_label.pack(pady=2)
        self.air_resistance_var.trace(
            "w", lambda *args: self.air_resistance_val_label.config(text=f"{self.air_resistance_var.get():.2f}"))

        ttk.Label(self.control_frame, text="Friction Coefficient").pack(pady=2)
        self.friction_var = tk.DoubleVar(value=0.2)
        self.friction_slider = ttk.Scale(self.control_frame, from_=0, to=1,
                                         orient=tk.HORIZONTAL, variable=self.friction_var,
                                         command=lambda val: self.update_friction(val))
        self.friction_slider.pack(pady=2)
        self.friction_val_label = ttk.Label(
            self.control_frame, text=f"{self.friction_var.get():.2f}")
        self.friction_val_label.pack(pady=2)
        self.friction_var.trace(
            "w", lambda *args: self.friction_val_label.config(text=f"{self.friction_var.get():.2f}"))
        self.friction_coefficient = self.friction_var.get()

        self.debug_mode = tk.BooleanVar(value=False)
        self.debug_checkbox = ttk.Checkbutton(
            self.control_frame, text="Debug Mode", variable=self.debug_mode)
        self.debug_checkbox.pack(pady=2)

        self.prop_panel = ttk.LabelFrame(
            self.control_frame, text="Selected Object Properties")
        self.prop_panel.pack(fill="both", expand=True, pady=10)

        self.selected_body_id = None
        self.drag_offset = None
        self.object_canvas_ids = {}
        self.create_objects()
        self.draw_bounds()
        self.running = False

        # bind dragging events
        self.canvas.tag_bind("body", "<ButtonPress-1>", self.on_body_press)
        self.canvas.tag_bind("body", "<B1-Motion>", self.on_drag_motion)
        self.canvas.tag_bind("body", "<ButtonRelease-1>", self.on_drag_release)
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)

    def update_gravity(self, val):
        self.physics.gravity = float(val)

    def update_air_resistance(self, val):
        new_drag = float(val)
        for item in self.physics.rigid_bodies:
            item["body"].drag_coefficient = new_drag

    def update_friction(self, val):
        self.friction_coefficient = float(val)

    def create_objects(self):
        # create a few initial bodies
        bodies = [
            RigidBody(mass=2, bbox=(50, 30), position=Vector2D(100, 50),
                      velocity=Vector2D(30, 0), restitution=0.7),
            RigidBody(mass=1, bbox=(40, 40), position=Vector2D(300, 100),
                      velocity=Vector2D(-20, 10), restitution=0.7),
            RigidBody(mass=50, bbox=(100, 100), position=Vector2D(200, 300),
                      velocity=Vector2D(0, -15), restitution=0.6)
        ]
        for body in bodies:
            self.physics.add_rigid_body(body)
        for item in self.physics.rigid_bodies:
            body_id = item["id"]
            canvas_id = self.draw_body(item["body"], body_id)
            self.object_canvas_ids[body_id] = canvas_id

    def create_new_shape(self):
        new_body = RigidBody(mass=1, bbox=(50, 50),
                             position=Vector2D(250, 250),
                             velocity=Vector2D(0, 0), restitution=0.5)
        self.physics.add_rigid_body(new_body)
        new_id = self.physics.rigid_bodies[-1]["id"]
        canvas_id = self.draw_body(new_body, new_id)
        self.object_canvas_ids[new_id] = canvas_id

    def create_new_polygon(self):
        triangle = [Vector2D(0, -30), Vector2D(30, 30), Vector2D(-30, 30)]
        new_body = RigidBody(mass=1, vertices=triangle,
                             position=Vector2D(350, 350),
                             velocity=Vector2D(0, 0), restitution=0.5)
        self.physics.add_rigid_body(new_body)
        new_id = self.physics.rigid_bodies[-1]["id"]
        canvas_id = self.draw_body(new_body, new_id)
        self.object_canvas_ids[new_id] = canvas_id

    def reset_canvas(self):
        self.pause_simulation()
        self.canvas.delete("all")
        self.draw_bounds()
        self.physics.rigid_bodies.clear()
        self.object_canvas_ids.clear()
        self.selected_body_id = None
        self.create_objects()

    def draw_bounds(self):
        self.canvas.create_rectangle(0, 0, self.canvas_width,
                                     self.canvas_height, outline="red")

    def draw_body(self, body, body_id):
        corners = body.get_corners()
        # use a list comprehension to flatten the corner coordinates
        points = [coord for corner in corners for coord in (
            corner.x, corner.y)]
        return self.canvas.create_polygon(points, outline="white",
                                          fill="", tags=("body", f"body_{body_id}"))

    def update_canvas(self):
        for item in self.physics.rigid_bodies:
            body = item["body"]
            body_id = item["id"]
            canvas_id = self.object_canvas_ids.get(body_id)
            if canvas_id:
                points = [coord for corner in body.get_corners()
                          for coord in (corner.x, corner.y)]
                self.canvas.coords(canvas_id, *points)
                fill_color = "red" if self.selected_body_id == body_id else ""
                self.canvas.itemconfig(canvas_id, fill=fill_color)
        self.canvas.delete("debug_arrow")
        if self.debug_mode.get():
            for item in self.physics.rigid_bodies:
                body = item["body"]
                pos = body.position
                # velocity arrow (green)
                v_scale = 0.5
                end_v = Vector2D(pos.x + body.velocity.x * v_scale,
                                 pos.y + body.velocity.y * v_scale)
                self.canvas.create_line(pos.x, pos.y, end_v.x, end_v.y,
                                        fill="green", arrow=tk.LAST,
                                        tags="debug_arrow")
                # constant force arrow (blue)
                f_scale = 0.1
                end_f = Vector2D(pos.x + body.constant_force.x * f_scale,
                                 pos.y + body.constant_force.y * f_scale)
                self.canvas.create_line(pos.x, pos.y, end_f.x, end_f.y,
                                        fill="blue", arrow=tk.LAST,
                                        tags="debug_arrow")
                # air resistance arrow (purple)
                a_scale = 50
                air_resistance = body.velocity * (-body.drag_coefficient)
                end_a = Vector2D(pos.x + air_resistance.x * a_scale,
                                 pos.y + air_resistance.y * a_scale)
                self.canvas.create_line(pos.x, pos.y, end_a.x, end_a.y,
                                        fill="purple", arrow=tk.LAST,
                                        tags="debug_arrow")

    def enforce_bounds(self, dt):
        for item in self.physics.rigid_bodies:
            body = item["body"]
            radius = body.get_bounding_radius()
            if body.position.x - radius < 0:
                body.position.x = radius
                if body.velocity.x < 0:
                    body.velocity.x = -body.velocity.x * body.restitution
            if body.position.x + radius > self.canvas_width:
                body.position.x = self.canvas_width - radius
                if body.velocity.x > 0:
                    body.velocity.x = -body.velocity.x * body.restitution
            if body.position.y - radius < 0:
                body.position.y = radius
                if body.velocity.y < 0:
                    body.velocity.y = -body.velocity.y * body.restitution
            if body.position.y + radius > self.canvas_height:
                body.position.y = self.canvas_height - radius
                if body.velocity.y > 0:
                    body.velocity.y = -body.velocity.y * body.restitution
                body.velocity.x *= (1 - self.friction_coefficient * dt)

    def simulation_step(self):
        dt = 0.016
        self.physics.update(dt)
        self.enforce_bounds(dt)
        self.update_canvas()
        if self.running:
            self.after(16, self.simulation_step)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.simulation_step()

    def pause_simulation(self):
        self.running = False

    def on_body_press(self, event):
        clicked_items = self.canvas.find_withtag("current")
        if not clicked_items:
            return
        item = clicked_items[0]
        tags = self.canvas.gettags(item)
        body_id = next(
            (int(tag.split("_")[1]) for tag in tags if tag.startswith("body_")), None)
        if body_id is None:
            return
        self.selected_body_id = body_id
        body = next(
            (d["body"] for d in self.physics.rigid_bodies if d["id"] == body_id), None)
        if not body:
            return
        self.drag_offset = Vector2D(
            event.x - body.position.x, event.y - body.position.y)
        body.velocity = Vector2D(0, 0)
        self.update_property_panel()

    def on_drag_motion(self, event):
        if self.selected_body_id is None or not self.drag_offset:
            return
        new_pos = Vector2D(event.x - self.drag_offset.x,
                           event.y - self.drag_offset.y)
        for d in self.physics.rigid_bodies:
            if d["id"] == self.selected_body_id:
                d["body"].position = new_pos
                d["body"].velocity = Vector2D(0, 0)
                break
        self.update_canvas()

    def on_drag_release(self, event):
        self.drag_offset = None

    def on_canvas_click(self, event):
        if not self.canvas.find_withtag("current"):
            self.selected_body_id = None
            self.update_property_panel()
            self.update_canvas()

    # helper to create sliders
    def create_slider(self, label_text, var, frm, frm_range, command, fmt="{:.2f}"):
        frame = ttk.Frame(frm)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=label_text).pack(side="left")
        slider = ttk.Scale(
            frame, from_=frm_range[0], to=frm_range[1], variable=var, command=command)
        slider.pack(side="left", fill="x", expand=True, padx=5)
        value_label = ttk.Label(frame, text=fmt.format(var.get()))
        value_label.pack(side="right")
        var.trace("w", lambda *args: value_label.config(text=fmt.format(var.get())))
        return slider

    def update_property_panel(self):
        for widget in self.prop_panel.winfo_children():
            widget.destroy()
        if self.selected_body_id is None:
            ttk.Label(self.prop_panel, text="No shape selected").pack()
            return
        body = next((d["body"] for d in self.physics.rigid_bodies if d["id"]
                    == self.selected_body_id), None)
        if not body:
            return

        mass_var = tk.DoubleVar(value=body.mass)
        self.create_slider("Mass", mass_var, self.prop_panel, (0.1, 100),
                           lambda val: self.update_body_mass(body, float(val)))
        if body.bbox is not None:
            width_var = tk.DoubleVar(value=body.bbox[0])
            self.create_slider("Width", width_var, self.prop_panel, (10, 200),
                               lambda val: self.update_body_size(body, float(val), body.bbox[1]))
            height_var = tk.DoubleVar(value=body.bbox[1])
            self.create_slider("Height", height_var, self.prop_panel, (10, 200),
                               lambda val: self.update_body_size(body, body.bbox[0], float(val)))
        else:
            scale_var = tk.DoubleVar(value=body.scale)
            self.create_slider("Scale", scale_var, self.prop_panel, (0.1, 3.0),
                               lambda val: self.update_body_scale(body, float(val)))
        ang_vel_var = tk.DoubleVar(value=body.angular_velocity)
        self.create_slider("Angular Velocity", ang_vel_var, self.prop_panel, (-10, 10),
                           lambda val: self.update_body_angular_velocity(body, float(val)))
        force_x_var = tk.DoubleVar(value=body.constant_force.x)
        self.create_slider("Force X", force_x_var, self.prop_panel, (-1000, 1000),
                           lambda val: self.update_body_force(body, float(val), body.constant_force.y))
        force_y_var = tk.DoubleVar(value=body.constant_force.y)
        self.create_slider("Force Y", force_y_var, self.prop_panel, (-1000, 1000),
                           lambda val: self.update_body_force(body, body.constant_force.x, float(val)))
        del_button = ttk.Button(
            self.prop_panel, text="Delete Shape", command=self.delete_selected_shape)
        del_button.pack(pady=5)

    def update_body_mass(self, body, mass):
        body.mass = mass
        if body.bbox is not None:
            w, h = body.bbox
            body.moment_of_inertia = mass * (w**2 + h**2) / 12
        else:
            body.update_moment_of_inertia()

    def update_body_size(self, body, width, height):
        if body.bbox is not None:
            body.bbox = (width, height)
            hw, hh = width / 2, height / 2
            body.original_vertices = [
                Vector2D(-hw, -hh), Vector2D(hw, -hh), Vector2D(hw, hh), Vector2D(-hw, hh)]
            body.vertices = [v * body.scale for v in body.original_vertices]
            body.moment_of_inertia = body.mass * (width**2 + height**2) / 12

    def update_body_scale(self, body, scale):
        body.scale = scale
        body.vertices = [v * scale for v in body.original_vertices]
        body.update_moment_of_inertia()

    def update_body_angular_velocity(self, body, ang_vel):
        body.angular_velocity = ang_vel

    def update_body_force(self, body, fx, fy):
        body.constant_force = Vector2D(fx, fy)

    def delete_selected_shape(self):
        if self.selected_body_id is None:
            return
        self.physics.rigid_bodies = [
            d for d in self.physics.rigid_bodies if d["id"] != self.selected_body_id]
        if self.selected_body_id in self.object_canvas_ids:
            self.canvas.delete(self.object_canvas_ids[self.selected_body_id])
            del self.object_canvas_ids[self.selected_body_id]
        self.selected_body_id = None
        self.update_property_panel()
        self.update_canvas()


class WelcomeFrame(ttk.Frame):
    """Initial popup dialog. Instantializes tkinter frame and spawns main application"""

    def __init__(self, container):
        super().__init__(container)

        self.control_frame = ttk.Frame(self)
        self.control_frame.pack()
        welcome_text = """
            In this application you will be able to play around with rigid body polygons and simulate physics.
            \n Click "Play" to start the simulation.
            \n Click a shape to adjust parameters.
            \n If you want further instructions, click the "?" button to display more information about an element.
        """
        self.welcome_label = ttk.Label(
            justify=tk.CENTER, text=welcome_text).pack()

        self.ok_button = ttk.Button(
            text="Continue", command=self.callback).pack()

    def callback(self):
        print("called")


class App(tk.Tk):
    def __init__(self, frame, title="Rigid Body Simulator", geometry="1024x768"):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(True, True)
        frame(self).pack(fill="both", expand=True)
