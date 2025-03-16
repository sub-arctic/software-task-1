import markdown
import re
import tkinter as tk
from tkinter import ttk
from latex import render_latex

class MarkdownParser:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

    def parse(self, md_text):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()  # Clear previous content

        lines = md_text.split("\n")
        for line in lines:
            widget = self.create_widget(line)
            if widget:
                widget.pack(anchor="w", padx=10, pady=2)

    def create_widget(self, line):
        if line.startswith("# "):  # Heading 1
            return ttk.Label(self.parent_frame, text=line[2:], font=("Arial", 14, "bold"))
        elif line.startswith("## "):  # Heading 2
            return ttk.Label(self.parent_frame, text=line[3:], font=("Arial", 12, "bold"))
        elif line.startswith("- "):  # Bullet points
            return ttk.Label(self.parent_frame, text="• " + line[2:], font=("Arial", 10))
        elif "**" in line:  # Bold
            return ttk.Label(self.parent_frame, text=re.sub(r"\*\*(.*?)\*\*", r"\1", line), font=("Arial", 10, "bold"))
        elif "*" in line:  # Italic
            return ttk.Label(self.parent_frame, text=re.sub(r"\*(.*?)\*", r"\1", line), font=("Arial", 10, "italic"))
        elif "$" in line:  # LaTeX math expression
            latex_expr = re.findall(r"\$(.*?)\$", line)
            if latex_expr:
                return self.create_latex_widget(latex_expr[0])
        else:
            return ttk.Label(self.parent_frame, text=line, font=("Arial", 10))

    def create_latex_widget(self, latex_expr):
        img_path = render_latex(latex_expr)
        if img_path:
            img = tk.PhotoImage(file=img_path)
            label = tk.Label(self.parent_frame, image=img)
            label.image = img
            return label
        return ttk.Label(self.parent_frame, text=f"LaTeX: {latex_expr}", font=("Arial", 10))

