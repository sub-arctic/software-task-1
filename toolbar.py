import tkinter as tk
from tkinter import ttk

class Toolbar(ttk.Frame):
    """A toolbar for controlling the simulation.

    This class provides buttons and sliders to interact with the simulation,
    including adding polygons, adjusting gravity, and controlling the speed factor.

    Attributes:
        parent: The parent widget of this toolbar.
        simulation_canvas: The canvas on which the simulation is rendered.
        play_pause_button: A button to start or pause the simulation.
        add_square_button: A button to add a polygon to the simulation.
        gravity_scale: A scale widget to adjust the gravity in the simulation.
        speed_factor_scale: A scale widget to adjust the speed factor of the simulation.
        gravity_label: A label displaying the text "Gravity".
        speed_factor_label: A label displaying the text "Speed Factor".
        gravity_value_label: A label displaying the current gravity value.
        speed_factor_value_label: A label displaying the current speed factor value.

    Args:
        parent: The parent widget to which this toolbar will be attached.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.simulation_canvas = parent.simulation_canvas
        self.parent.play_pause_text = tk.StringVar()

        self.add_polygon_button = ttk.Button(
            self,
            text="Add polygon",
            command=self.simulation_canvas.body_renderer.create_polygon,
        )

        self.gravity_scale = ttk.Scale(
            self,
            command=self.simulation_canvas.simulation_controller.set_gravity,
            from_=0,
            to=20,
            value=9.89,
            orient=tk.HORIZONTAL,
        )

        self.speed_factor_scale = ttk.Scale(
            self,
            command=self.set_speed_factor,
            from_=0.1,
            to=10.0,
            value=3.0,
            orient=tk.HORIZONTAL,
        )

        self.parent.play_pause_text.set("Play")
        self.play_pause_button = ttk.Button(
            self,
            text="Start",
            textvariable=self.parent.play_pause_text,
            command=self.simulation_canvas.interaction_manager.play_pause,
        )
        self.clear_button = ttk.Button(
            self,
            text="Clear",
            command=self.simulation_canvas.simulation_controller.reset,
        )

        self.play_pause_button.grid(column=0, row=1)
        self.add_polygon_button.grid(column=1, row=1)
        self.gravity_scale.grid(column=2, row=1)
        self.speed_factor_scale.grid(column=3, row=1)

        self.gravity_label = ttk.Label(self, text="Gravity")
        self.gravity_label.grid(column=2, row=0)
        self.speed_factor_label = ttk.Label(self, text="Speed Factor")
        self.speed_factor_label.grid(column=3, row=0)

        self.gravity_value_label = ttk.Label(self, text=str(self.gravity_scale.get()))
        self.gravity_value_label.grid(column=2, row=2)
        self.speed_factor_value_label = ttk.Label(self, text=str(self.speed_factor_scale.get()))
        self.speed_factor_value_label.grid(column=3, row=2)

        self.gravity_scale.config(command=self.update_gravity_value)
        self.speed_factor_scale.config(command=self.update_speed_factor_value)

        self.clear_button.grid(column=4, row=1)

        self.theme_toggle_var = tk.BooleanVar(value=False)
        self.theme_toggle_check = ttk.Checkbutton(
            self,
            text="Dark Theme",
            variable=self.theme_toggle_var,
            command=self.parent.toggle_theme,
        )
        self.theme_toggle_check.grid(column=5, row=1)

    def set_speed_factor(self, value: str) -> None:
        """Sets the speed factor for the simulation."""
        self.simulation_canvas.simulation_controller.set_speed_factor(value)

    def update_gravity_value(self, value: str) -> None:
        """Updates the gravity value in the simulation and the display label."""
        self.simulation_canvas.simulation_controller.set_gravity(value)
        self.gravity_value_label.config(text=str(round(float(value), 2)))

    def update_speed_factor_value(self, value: str) -> None:
        """Updates the displayed speed factor value."""
        self.speed_factor_value_label.config(text=str(value))

