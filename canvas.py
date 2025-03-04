import tkinter
from typing import Any


class SimulationCanvas(tkinter.Canvas):
    def __init__(self, parent: tkinter.Frame, **kwargs: Any) -> None:
        super().__init__(parent, **kwargs)

        self.parent = parent
