import tkinter as tk
from peewee import *
import datetime

class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.columnconfigure(self, index=0, weight=1)
        tk.Frame.columnconfigure(self, index=1, weight=1)
        tk.Frame.columnconfigure(self, index=2, weight=1)
        tk.Frame.rowconfigure(self, index=0, weight=0)
        tk.Frame.rowconfigure(self, index=1, weight=1)
        tk.Frame.rowconfigure(self, index=2, weight=1)

        color = "#2b99b3"
        background = "#42d4f5"
        tk.Frame.config(self, background=background)

        self.inventoryTracker = tk.PhotoImage(file='images/InventoryTracker.png')
        self.addInvImg = tk.PhotoImage(file='images/addInventory.png')
        self.viewInvImg = tk.PhotoImage(file='images/viewInventory.png')
        self.addCost = tk.PhotoImage(file='images/addCost.png')
        self.viewCost = tk.PhotoImage(file='images/viewCosts.png')

        label = tk.Label(self, image=self.inventoryTracker, borderwidth=0, bg=background)
        addInvButton = tk.Button(self, image=self.addInvImg, bg=background, borderwidth=0, command=lambda: controller.showFrame("addInventory"))
        viewInvButton = tk.Button(self, image=self.viewInvImg, bg=background, command=lambda: controller.showFrame("viewInventory"))
        addCostButton = tk.Button(self, image=self.addCost, bg=background, command=lambda: controller.showFrame("addCost"))
        viewCostButton = tk.Button(self, image=self.viewCost, bg=background, command=lambda: controller.showFrame("viewCost"))

        label.grid(row=0, column=1, padx=10, pady=10)
        addInvButton.grid(row=1, column=0, padx=10, pady=10)
        viewInvButton.grid(row=2, column=0, padx=10, pady=10)
        addCostButton.grid(row=1, column=2, pady=10, padx=10)
        viewCostButton.grid(row=2, column=2, pady=10, padx=10)