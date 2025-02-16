import tkinter as tk
from application import MainFrame

class App(tk.Tk):
    def __init__(self, title="Rigid Body Simulator", geometry="1024x768"):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(True, True)
        MainFrame(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()

