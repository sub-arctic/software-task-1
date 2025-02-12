import tkinter as tk
from tkinter import ttk
class Application(ttk.Frame):
    """Main application class for the Tkinter GUI."""

    def __init__(self, title="root", geometry="512x512", **kwargs):
        """Initialize the application window."""
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)

        self.frame = tk.Frame(self.root, **kwargs)
        self.frame.grid(row=0, column=0, sticky="NESW")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def run(self):
        """Run the main loop of the application."""
        self.root.mainloop()

    def do_exit(self):
        """Exit the application."""
        self.root.destroy()

    def add_widget(self, widget_name, grid_options=None, **kwargs):
        """Add a widget to the application frame."""
        if grid_options is None:
            grid_options = {"column": 0, "columnspan": 1, "row": 0}

        widget_class = getattr(ttk, widget_name, None)

        if widget_class is None:
            widget_class = getattr(tk, widget_name, None)
            if widget_class is None:
                print(f"Widget '{widget_name}' not found.")
                return None

        widget = widget_class(self.frame, **kwargs)

        if widget is not None:
            widget.grid(**grid_options)
        return widget

    def draw_canvas_object(self, canvas_name, object_name, *args, **kwargs):
        """Draw an object on the canvas."""
        obj_id = getattr(canvas_name, object_name)(*args, **kwargs)
        return obj_id

