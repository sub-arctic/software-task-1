import re
import tkinter as tk
from tkinter import ttk
from latex import render_latex

type Properties = dict[str, object]
type Body = dict[str, Properties]
type Bodies = list[dict[str, Properties]]

class MarkdownParser:
    def __init__(self, parent_frame: ttk.Frame) -> None:
        self.parent_frame = parent_frame
        self.bodies: Bodies = []

    def parse(self, md_text: str) -> None:
        self.bodies.clear()
        content: str = md_text

        if md_text.startswith("---"):
            metadata_lines, content = self.extract_metadata(md_text)
            self.bodies = self.parse_metadata(metadata_lines)

        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        for line in content.split("\n"):
            widget = self.create_widget(line)
            if widget:
                widget.pack(anchor="w", padx=10, pady=2)

    def extract_metadata(self, md_text: str) -> tuple[list[str], str]:
        lines: list[str] = md_text.split("\n")
        metadata_lines: list[str] = []
        content_start_index: int = 0

        if lines[0] == "---":
            for i in range(1, len(lines)):
                if lines[i] == "---":
                    content_start_index = i + 1
                    break
                metadata_lines.append(lines[i])

        content: str = "\n".join(lines[content_start_index:])
        return metadata_lines, content

    def parse_metadata(self, metadata_lines: list[str]) -> Bodies:
        bodies: Bodies = []

        for line in metadata_lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ": [" in line:
                key, values = line.split(": [", 1)
                key = key.strip()
                values = values.rstrip("]")

                properties: Properties = self.parse_inline_properties(values)
                bodies.append({key: properties})

        return bodies

    def parse_inline_properties(self, properties_str: str) -> Properties:
        properties: Properties = {}
        pairs: list[str] = properties_str.split(",")

        for pair in pairs:
            if ": " in pair:
                key, value = pair.split(": ", 1)
                properties[key.strip()] = self.cast_value(value.strip())

        return properties

    def cast_value(self, value: str) -> object:
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def create_widget(self, line: str) -> ttk.Widget:
        if line.startswith("# "):
            return ttk.Label(self.parent_frame, text=line[2:], font=("Arial", 14, "bold"))
        elif line.startswith("## "):
            return ttk.Label(self.parent_frame, text=line[3:], font=("Arial", 12, "bold"))
        elif line.startswith("- "):
            return ttk.Label(self.parent_frame, text="• " + line[2:], font=("Arial", 10))
        elif "**" in line:
            return ttk.Label(self.parent_frame, text=re.sub(r"\*\*(.*?)\*\*", r"\1", line), font=("Arial", 10, "bold"))
        elif "*" in line:
            return ttk.Label(self.parent_frame, text=re.sub(r"\*(.*?)\*", r"\1", line), font=("Arial", 10, "italic"))
        elif "$" in line:
            latex_expr: list[str] = re.findall(r"\$(.*?)\$", line)
            if latex_expr:
                return self.create_latex_widget(latex_expr[0])
        return ttk.Label(self.parent_frame, text=line, font=("Arial", 10))

    def create_latex_widget(self, latex_expr: str) -> ttk.Widget:
        img_path: str | None = render_latex(latex_expr)
        if img_path:
            img = tk.PhotoImage(file=img_path)
            label = ttk.Label(self.parent_frame, image=img)
            label.image = img
            return label
        return ttk.Label(self.parent_frame, text=f"LaTeX: {latex_expr}", font=("Arial", 10))

