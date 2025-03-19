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

    Args:
        parent: The parent widget to which this frame will be attached.
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

        for text in {self.restitution_text, self.velocity_text, self.mass_text}:
            text.grid()

    def update_properties(self) -> None:
        """Updates the displayed properties based on the currently selected body.

        This method retrieves the state of the currently selected body and updates
        the velocity, mass, and restitution displayed in the frame. If no body is
        selected, the method does nothing.
        """
        if self.simulation_canvas.interaction_manager.current_body is None:
            return
        state = self.simulation_canvas.interaction_manager.current_body.get_state()
        velocity_x = round(state["velocity"].x)
        velocity_y = round(state["velocity"].y)
        self.velocity.set(f"x: {velocity_x}, y: {velocity_y}")
        self.mass.set(f"mass: {state['mass']}")
        self.restitution.set(f"restitution: {state['restitution']}")

