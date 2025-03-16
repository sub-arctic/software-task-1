import os
import tkinter as tk
from tkinter import ttk
from markdown import MarkdownParser
from simulation_canvas import SimulationCanvas

LESSONS_PATH = "lessons"


class LessonFrame(ttk.Frame):
    def __init__(self, parent) -> None:
        self.parent = parent
        super().__init__(self.parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(sticky="nsew")
        self.parser = MarkdownParser(self.content_frame)

    def display_lesson(self, markdown_text: str) -> None:
        self.parser.parse(markdown_text)
        if self.parser.bodies is None:
            return
        for body in self.parser.bodies:
            for _, properties in body.items():
                self.parent.simulation_canvas.body_renderer.create_polygon(**properties)


    def load_lesson(self, lesson_filename: str) -> None:
        lesson_file_path = os.path.join(LESSONS_PATH, lesson_filename)
        if os.path.exists(lesson_file_path):
            with open(lesson_file_path, "r") as file:
                lesson_text = file.read()
            self.display_lesson(lesson_text)
        else:
            print(f"Lesson {lesson_filename} not found!")

class LessonManager:
    def __init__(self, parent: tk.Widget, lesson_frame: LessonFrame, simulation_canvas: SimulationCanvas) -> None:
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
        lesson_path = os.path.join(LESSONS_PATH, lesson_file)
        if os.path.exists(lesson_path):
            with open(lesson_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()
            self.lesson_frame.display_lesson(markdown_text)

    def switch_lesson(self, _) -> None:
        selected_lesson = self.lesson_selector.get()
        self.simulation_canvas.simulation_controller.reset()
        self.load_lesson(selected_lesson)
