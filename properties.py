import tkinter as tk
from tkinter import ttk

class PropertiesFrame(ttk.LabelFrame):
    def __init__(self, parent):
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

    def update_properties(self):
        if self.simulation_canvas.interaction_manager.current_body is None:
            return
        state = self.simulation_canvas.interaction_manager.current_body.get_state()
        velocity_x = round(state["velocity"].x)
        velocity_y = round(state["velocity"].y)
        self.velocity.set(f"velocity x: {velocity_x}, y: {velocity_y}")
        self.mass.set(f"mass: {state["mass"]}")
        self.restitution.set(f"restitution: {state["restitution"]}")

