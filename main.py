import tkinter as tk
from application import Application

if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = Application(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
