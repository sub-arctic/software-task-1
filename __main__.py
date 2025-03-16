if __name__ == "__main__":
    import tkinter as tk
    from application import Application
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    app = Application(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
else:
    raise ImportError("Run this file directly, don't import it!")
