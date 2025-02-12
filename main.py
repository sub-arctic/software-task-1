import tkinter as tk
from tkinter import ttk

class Application(ttk.Frame):
    def __init__(self, title="root", geometry="512x512", **kwargs):
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
        self.root.mainloop()

    def doExit(self):
        self.root.destroy()

    def addWidget(self, widget_name, **kwargs):
        widget_class = getattr(tk, widget_name, None)
        if widget_class is None:
            print(f"Widget '{widget_name}' not found.")
            return None
        widget = widget_class(self.frame, **kwargs)
        if widget is not None:
            widget.grid(**{k: v for k, v in kwargs.items() if k in ['row', 'column', 'sticky', 'padx', 'pady']})
        return widget

if __name__ == "__main__":
    app = Application(title="test", geometry="1024x1024")
    mainMessage = app.addWidget(
        "Message", 
        text="Welcome to this application", 
        width=512, 
        justify=tk.CENTER
    )
    exitBtn = app.addWidget("Button", text="exit", command=app.doExit)
    app.run()
