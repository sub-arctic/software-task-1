import tkinter as tk
from tkinter import ttk
import simulation
from toolbar import Toolbar
from lesson_manager import LessonManager, LessonFrame
from properties import PropertiesFrame
from styles import apply_dark_theme, apply_light_theme

LESSONS_PATH = "lessons"

class Application(ttk.Frame):
    """The main application frame.

    Attributes:
        lesson_frame: A tkinter frame containing lesson information.
        simulation_canvas: A tkinter canvas for drawing rigidbodies
            and handling the physics simulation.
        properties_frame: A tkinter label frame containing selected
            shape properties.
        lesson_manager: An object handling parsing and rendering of
            markdown lessons.
        dark_theme: A boolean flag that sets the application theme.
    """
    def __init__(self, parent: tk.Tk) -> None:
        """Initialises the tkinter frame on the parent.

        Args:
            parent: The tkinter root window.
        """
        super().__init__(parent)
        self.setup_grid()


        self.lesson_frame = LessonFrame(self)
        self.simulation_canvas = simulation.Canvas(self)

        self.dark_theme = False
        apply_light_theme(self)

        self.toolbar = Toolbar(self)
        self.toolbar.grid(row=1, column=1, sticky="nsew")

        self.properties_frame = PropertiesFrame(self)
        self.properties_frame.grid(row=0, column=3, sticky="nsew")

        self.lesson_manager = LessonManager(
            self, self.lesson_frame, self.simulation_canvas
        )
        self.lesson_manager.load_lesson("intro.md")


    def setup_grid(self) -> None:
        """Setup grid alignment.

        Initializes the grid for the current frame, displaying it
        on the root, and allows it to expand in all directions.
        Uses column and rowconfigure to allow the second column
        to be resizable, which is where the canvas is stored.
        """
        self.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
    
    def toggle_theme(self):
        if self.dark_theme:
            apply_light_theme(self)
        else:
            apply_dark_theme(self)
        self.dark_theme = not self.dark_theme
