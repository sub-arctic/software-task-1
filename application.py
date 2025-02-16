import tkinter as tk
from tkinter import ttk
from physics import *

class MainFrame(ttk.Frame):
    lastId = 0
    def __init__(self, container):
        super().__init__(container)

        gravity = tk.DoubleVar()
        self.physics = Physics(gravity=9.811)

        self.canvas = tk.Canvas(self, width=512, height=512, bg='black')
        self.canvas.grid(column=0, row=0, padx=24, pady=24, sticky='N')

        self.label = ttk.Label(self, textvariable=gravity)
        self.label.grid(column=0, row=1)

        self.slider = ttk.Scale(
            self,
            command=self.physics.update_gravity,
            from_=0, to=100,
            value=9.8,
            orient=tk.HORIZONTAL,
            length=512,
            variable=gravity
            )
        self.slider.grid(column=0, row=2)

        self.play_button = ttk.Button(self, text='Play', command=self.get_physics_object_states)
        self.play_button.grid(column=0, row=3)

        square_x = 100
        square_y = 100
        self.squareId = self.draw_square(100, 100, 100)
        square = PhysicsObject(100, self.canvas.bbox(self.squareId), (0, 0), (square_x, square_y))
        self.physics.add_object(square)

        # self.canvas.bind('<B1-Motion>', self.drag_object)

        self.grid(padx=5, pady=10, sticky=tk.NSEW)

    def get_physics_object_states(self):
        self.physics.update(time=0.1)
        self.canvas.move(self.squareId, *self.physics.get_position(self.squareId))

    def draw_square(self, x, y, size):
        id = self.canvas.create_rectangle(x, y, x+size, y+size, outline="white")
        return id

    def is_within_bbox(self, event_x, event_y, x1, y1, x2, y2, tolerance=10):
        x1_t = x1 - tolerance
        y1_t = y1 - tolerance
        x2_t = x2 + tolerance
        y2_t = y2 + tolerance
        return x1_t <= event_x <= x2_t and y1_t <= event_y <= y2_t

class App(tk.Tk):
    def __init__(self, title="root", geometry="1024x1024"):
        super().__init__()

        self.title(title)
        self.geometry(geometry)
        self.resizable(True, True)
