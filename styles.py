import tkinter as tk
from tkinter import ttk

DARK_BACKGROUND = "#222222"
DARK_POLYGON_FILL = "#444444"
DARK_POLYGON_OUTLINE = "#ffffff"

LIGHT_BACKGROUND = "#ffffff"
LIGHT_POLYGON_FILL = "#c0c0c0"
LIGHT_POLYGON_OUTLINE = "#000000"

DARK_BUTTON_BG = "#333333"
DARK_BUTTON_FG = "#ffffff"

LIGHT_BUTTON_BG = "#f0f0f0"
LIGHT_BUTTON_FG = "#000000"

def apply_dark_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    
    style.configure("TButton",
                    relief="flat",
                    background=DARK_BUTTON_BG,
                    foreground=DARK_BUTTON_FG,
                    font=("Arial", 10))
    style.configure("TLabel",
                    background=DARK_BACKGROUND,
                    foreground=DARK_BUTTON_FG,
                    font=("Arial", 10))
    style.configure("TScale",
                    background=DARK_BACKGROUND,
                    troughcolor="#555555",
                    sliderlength=15)
    style.configure("TFrame",
                    background=DARK_BACKGROUND)
    style.configure("TScrollbar",
                    background=DARK_BACKGROUND,
                    troughcolor="#555555",
                    arrowcolor=DARK_BUTTON_FG)
    style.configure("TLabelframe",
                    background=DARK_BACKGROUND,
                    foreground=DARK_BUTTON_FG)
    style.configure("TCheckbutton",
                    background=DARK_BACKGROUND,
                    foreground=DARK_BUTTON_FG)
    style.configure("TRadiobutton",
                    background=DARK_BACKGROUND,
                    foreground=DARK_BUTTON_FG)

    root.simulation_canvas.config(bg=DARK_BACKGROUND)

    root.simulation_canvas.polygon_fill = DARK_POLYGON_FILL
    root.simulation_canvas.polygon_outline = DARK_POLYGON_OUTLINE

def apply_light_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    
    style.configure("TButton",
                    relief="flat",
                    background=LIGHT_BUTTON_BG,
                    foreground=LIGHT_BUTTON_FG,
                    font=("Arial", 10))
    style.configure("TLabel",
                    background=LIGHT_BACKGROUND,
                    foreground=LIGHT_BUTTON_FG,
                    font=("Arial", 10))
    style.configure("TScale",
                    background=LIGHT_BACKGROUND,
                    troughcolor="#d3d3d3",
                    sliderlength=15)
    style.configure("TFrame",
                    background=LIGHT_BACKGROUND)
    style.configure("TScrollbar",
                    background=LIGHT_BACKGROUND,
                    troughcolor="#d3d3d3",
                    arrowcolor=LIGHT_BUTTON_FG)
    style.configure("TLabelframe",
                    background=LIGHT_BACKGROUND,
                    foreground=LIGHT_BUTTON_FG)
    style.configure("TCheckbutton",
                    background=LIGHT_BACKGROUND,
                    foreground=LIGHT_BUTTON_FG)
    style.configure("TRadiobutton",
                    background=LIGHT_BACKGROUND,
                    foreground=LIGHT_BUTTON_FG)

    root.simulation_canvas.config(bg=LIGHT_BACKGROUND)

    root.simulation_canvas.polygon_fill = LIGHT_POLYGON_FILL
    root.simulation_canvas.polygon_outline = LIGHT_POLYGON_OUTLINE

