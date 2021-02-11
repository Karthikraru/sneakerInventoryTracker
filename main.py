import tkinter as tk
from peewee import *
import datetime
from startPage import startPage
from addInventory import addInventory
from viewInventory import viewInventory
from databases import init


class Tracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in {startPage, addInventory, viewInventory}:
            pageName = F.__name__
            frame = F(container, self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("startPage")

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()



if __name__ == "__main__":
    init()
    app = Tracker()
    app.geometry("1100x735")
    app.title("Inventory Tracker")
    app.mainloop()
