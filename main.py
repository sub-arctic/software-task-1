import trace
import tkinter as tk
from tkinter import ttk

tracer = trace.Trace(
    count=False,
    trace=True
)

id = 0
class Application(ttk.Frame):
    def __init__(self, **kwargs):
        super().__init__()
        ttk.Frame(self, **kwargs)
        self.grid()
    
    def createButton(self, **kwargs):
        id = self.button = tk.Button(self, **kwargs)
        self.button.grid()
        return id

    def createCanvas(self, **kwargs):
        id = self.canvas = tk.Canvas(self, **kwargs)
        self.canvas.grid()
        return id
    
    def drawLine(self, points, **kwargs):
        id = self.canvas.create_line(points, **kwargs) 
        return id

    def createText(self, x, y, **kwargs):
        id = self.canvas.create_text(x, y, **kwargs)
        return id

    def createScale(self, x, y, **kwargs):
        id = self.scale = ttk.Scale(self, **kwargs)
        self.scale.place(x=x,y=y,anchor=tk.CENTER)
        return id

    def updateText(self, *args):
        global textId
        global id
        self.canvas.delete(id)
        self.canvas.itemconfigure(textId, text=args)
        id = self.drawLine(createLineFromScale(), width=2)

def createLineFromScale():
    global scaleVertical
    global scaleHorizontal
    valueX = scaleHorizontal.get()
    valueY = scaleVertical.get()
    line = [width/2,height/2,width/2+100+valueX*2,height/2+100+valueY*2]
    return line
width = 1000
height = width


app = Application()
app.createCanvas(bg="#ffffff", width=width, height=height)
textId=app.createText(100, 150)
scaleVertical = app.createScale(width/2, 200, orient=tk.VERTICAL, command=app.updateText, from_=-100, to_=100)
scaleHorizontal = app.createScale(width/2, 100, command=app.updateText, from_=-100, to_=100)


app.mainloop()

