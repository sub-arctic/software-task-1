import tkinter as tk
from simulation_controller import SimulationController
from renderer import BodyRenderer
from interaction_manager import InteractionManager


class SimulationCanvas(tk.Canvas):
    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent
        super().__init__(self.parent)
        self.width = 800
        self.height = 600
        self.config(width=self.width, height=self.height)
        self.simulation_controller = SimulationController(self)
        self.body_renderer = BodyRenderer(self, self.simulation_controller)
        self.interaction_manager = InteractionManager(self, self.simulation_controller)
        self.interaction_manager.setup_handlers()
        self.grid(row=0, column=1, sticky="nsew")

    def update_dimensions(self) -> None:
        self.width = self.winfo_width()
        self.height = self.winfo_height()

