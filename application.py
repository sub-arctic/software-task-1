import tkinter as tk
from tkinter import ttk
from simulation_canvas import SimulationCanvas
from toolbar import Toolbar
from lesson_manager import LessonManager, LessonFrame

LESSONS_PATH = "lessons"

class Application(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.setup_grid()

        self.lesson_frame = LessonFrame(self)
        self.simulation_canvas = SimulationCanvas(self)

        self.toolbar = Toolbar(self)
        self.toolbar.grid(row=1, column=1, sticky="nsew")

        self.lesson_manager = LessonManager(self, self.lesson_frame, self.simulation_canvas)
        self.lesson_manager.load_lesson("gravity.md")

    def setup_grid(self) -> None:
        self.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)


