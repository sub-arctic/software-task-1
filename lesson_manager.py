import os
import tkinter as tk
from tkinter import ttk
import simulation
from markdown import MarkdownParser

LESSONS_PATH = "lessons"

class LessonFrame(ttk.Frame):
    """A frame that displays lessons in a Markdown format with scrolling support.

    This class is responsible for rendering lesson content using a Markdown parser
    and displaying it within a Tkinter frame with scrollability.

    Args:
        parent: The parent application which is referenced for body creation.
    """

    def __init__(self, parent) -> None:
        self.parent = parent
        super().__init__(self.parent)
        
        self.grid(row=0, column=0, sticky="nsew")
        
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self)
        self.yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.xscrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda _: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.yscrollbar.grid(row=0, column=1, sticky="ns")
        self.xscrollbar.grid(row=1, column=0, sticky="ew")
        
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        self.parser = MarkdownParser(self.scrollable_frame)

    def display_lesson(self, markdown_text: str) -> None:
        """Displays the lesson content parsed from the provided Markdown text.

        This method parses the given Markdown text and renders the resulting bodies
        onto the simulation canvas.

        Args:
            markdown_text: The Markdown text to be parsed and displayed.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.parser.parse(markdown_text)
        if self.parser.bodies is None:
            return
        for body in self.parser.bodies:
            for _, properties in body.items():
                self.parent.simulation_canvas.body_renderer.create_polygon(**properties)


class LessonManager:
    """Manages the loading and switching of lessons in the application.

    This class handles the selection of lesson files and loads the corresponding
    Markdown content into the LessonFrame for display.

    Args:
        parent: The parent widget for the lesson manager.
        lesson_frame: The frame responsible for displaying lesson content.
        simulation_canvas: The canvas used for rendering simulations.
    """

    def __init__(
        self,
        parent,
        lesson_frame: LessonFrame,
        simulation_canvas: simulation.Canvas
    ) -> None:
        self.parent = parent
        self.lesson_frame = lesson_frame
        self.simulation_canvas = simulation_canvas
        self.lesson_selector = ttk.Combobox(parent, state="readonly")

        self.lesson_files = [f for f in os.listdir(LESSONS_PATH) if f.endswith(".md")]
        self.lesson_selector["values"] = self.lesson_files
        self.lesson_selector.grid(row=1, column=0, pady=10)
        self.lesson_selector.bind("<<ComboboxSelected>>", self.switch_lesson)
        if self.lesson_files:
            self.lesson_selector.current(0)

    def load_lesson(self, lesson_file: str) -> None:
        """Loads a lesson from the specified Markdown file and displays it.

        This method reads the content of the specified lesson file and passes
        the Markdown text to the LessonFrame for rendering.

        Args:
            lesson_file: The name of the lesson file to load.
        """
        lesson_path = os.path.join(LESSONS_PATH, lesson_file)
        if os.path.exists(lesson_path):
            with open(lesson_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()
            self.lesson_frame.display_lesson(markdown_text)

    def switch_lesson(self, _) -> None:
        """Handles the event of switching lessons in the lesson selector.

        This method resets the simulation controller and loads the selected lesson
        from the lesson selector.

        Args:
            _: The event object (not used).
        """
        selected_lesson = self.lesson_selector.get()
        self.simulation_canvas.simulation_controller.reset()
        self.load_lesson(selected_lesson)

