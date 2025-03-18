import tkinter as tk
from tkinter import ttk
from simulation_canvas import SimulationCanvas
from toolbar import Toolbar
from lesson_manager import LessonManager, LessonFrame
from properties import PropertiesFrame

LESSONS_PATH = "lessons"

class Application(ttk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.setup_grid()

        self.lesson_frame = LessonFrame(self)
        self.simulation_canvas = SimulationCanvas(self)

        self.toolbar = Toolbar(self)
        self.toolbar.grid(row=1, column=1, sticky="nsew")

        self.properties_frame = PropertiesFrame(self)
        self.properties_frame.grid(row=0, column=3, sticky="nsew")

        self.lesson_manager = LessonManager(self, self.lesson_frame, self.simulation_canvas)
        self.lesson_manager.load_lesson("intro.md")

    def setup_grid(self) -> None:
        self.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)


