import tkinter as tk
from tkinter import ttk

class PropertiesFrame(ttk.LabelFrame):
    """A frame that displays properties of the currently selected body in the simulation.

    This frame shows the velocity, mass, and restitution of the selected body,
    updating the displayed values whenever the properties change.

    Attributes:
        simulation_canvas: The canvas used for rendering the simulation.
        velocity: A StringVar that holds the velocity of the selected body.
        mass: A StringVar that holds the mass of the selected body.
        restitution: A StringVar that holds the restitution of the selected body.
        velocity_text: A label that displays the velocity of the selected body.
        mass_text: A label that displays the mass of the selected body.
        restitution_text: A label that displays the restitution of the selected body.
    """

    def __init__(self, parent) -> None:
        super().__init__(
            parent, text="Properties", borderwidth=3, relief=tk.RIDGE, padding=10
        )
        self.simulation_canvas = parent.simulation_canvas
        self.velocity = tk.StringVar()
        self.velocity_text = ttk.Label(self, textvariable=self.velocity)
        self.mass = tk.StringVar()
        self.mass_text = ttk.Label(self, textvariable=self.mass)
        self.restitution = tk.StringVar()
        self.restitution_text = ttk.Label(self, textvariable=self.restitution)

        self.polygon_sides_label = ttk.Label(self, text="Polygon Vertices")
        self.polygon_size_label = ttk.Label(self, text="Polygon Size")
        self.mass_label = ttk.Label(self, text="Polygon Mass")

        self.rounding = 2

        self.polygon_sides_scale = ttk.Scale(
            self,
            from_=3,
            to=25,
            value=4,
            orient=tk.HORIZONTAL,
            variable=self.simulation_canvas.body_renderer.default_polygon_sides
        )
        self.polygon_size_scale = ttk.Scale(
            self,
            from_=10,
            to=200,
            value=100,
            orient=tk.HORIZONTAL,
            variable=self.simulation_canvas.body_renderer.default_polygon_size
        )
        self.mass_scale = ttk.Scale(
            self,
            from_=1,
            to=30,
            value=5,
            orient=tk.HORIZONTAL,
            variable=self.simulation_canvas.body_renderer.default_polygon_mass
        )

        self.polygon_sides_value_label = ttk.Label(self, text=str(round(self.polygon_sides_scale.get(), self.rounding)))
        self.polygon_size_value_label = ttk.Label(self, text=str(round(self.polygon_size_scale.get(), self.rounding)))
        self.mass_value_label = ttk.Label(self, text=str(round(self.mass_scale.get(), self.rounding)))

        self.velocity_text.grid(column=0, row=0, sticky=tk.W)
        self.mass_text.grid(column=0, row=1, sticky=tk.W)
        self.restitution_text.grid(column=0, row=2, sticky=tk.W)

        self.polygon_sides_label.grid(column=0, row=3, sticky=tk.W)
        self.polygon_size_label.grid(column=0, row=5, sticky=tk.W)
        self.mass_label.grid(column=0, row=7, sticky=tk.W)

        self.polygon_sides_scale.grid(column=0, row=4, sticky=tk.W)
        self.polygon_size_scale.grid(column=0, row=6, sticky=tk.W)
        self.mass_scale.grid(column=0, row=8, sticky=tk.W)

        self.polygon_sides_value_label.grid(column=1, row=4, sticky=tk.W)
        self.polygon_size_value_label.grid(column=1, row=6, sticky=tk.W)
        self.mass_value_label.grid(column=1, row=8, sticky=tk.W)

        self.polygon_sides_scale.config(command=self.update_polygon_sides_value)
        self.polygon_size_scale.config(command=self.update_polygon_size_value)
        self.mass_scale.config(command=self.update_mass_value)


    def update_properties(self) -> None:
        """Updates the displayed properties based on the currently selected body."""
        if self.simulation_canvas.interaction_manager.current_body is None:
            return
        state = self.simulation_canvas.interaction_manager.current_body.get_state()
        velocity_x = round(state["velocity"].x)
        velocity_y = round(state["velocity"].y)
        self.velocity.set(f"x: {velocity_x}, y: {velocity_y}")
        self.mass.set(f"mass: {round(state['mass'], 2)}")
        self.restitution.set(f"restitution: {state['restitution']}")

    def update_polygon_sides_value(self, value: str) -> None:
        """Updates the displayed polygon vertices value."""
        self.polygon_sides_value_label.config(text=str(round(float(value), self.rounding)))
        self.simulation_canvas.simulation_controller.modify_current_body()

    def update_polygon_size_value(self, value: str) -> None:
        """Updates the displayed polygon size value."""
        self.polygon_size_value_label.config(text=str(round(float(value), self.rounding)))
        self.simulation_canvas.simulation_controller.modify_current_body()

    def update_mass_value(self, value: str) -> None:
        """Updates the displayed mass value."""
        self.mass_value_label.config(text=str(round(float(value), self.rounding)))
        self.simulation_canvas.simulation_controller.modify_current_body()

