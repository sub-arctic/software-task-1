import tkinter as tk
root = tk.Tk()
root.geometry("500x500+0+0")
frmMain = tk.Frame(root,bg="blue")

startbutton = tk.Button(frmMain, text="Start",height=1,width=4)
startbutton.grid()

#Configure the row/col of our frame and root window to be resizable and fill all available space
frmMain.grid(row=0, column=0, sticky="NESW")
frmMain.grid_rowconfigure(0, weight=1)
frmMain.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
