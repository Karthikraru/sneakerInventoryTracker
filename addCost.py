import tkinter as tk
from peewee import *
import datetime
from databases import Cost

class addCost(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.columnconfigure(self, index=0, weight=1)
        tk.Frame.columnconfigure(self, index=1, weight=1)
        tk.Frame.columnconfigure(self, index=2, weight=1)
        tk.Frame.rowconfigure(self, index=0, weight=0)


        self.errorLog = tk.StringVar()
        self.errorLog.trace('w', self.buildErrorLog)

        self.color = "#2b99b3"
        self.background = "#42d4f5"

        tk.Frame.config(self, background=self.background)

        self.add = tk.PhotoImage(file='images/add.png')
        self.inventoryTracker = tk.PhotoImage(file='images/InventoryTracker.png')

        startPageButton = tk.Button(self, image=self.inventoryTracker, fg="#2b99b3",command=lambda: controller.showFrame("startPage"))
        startPageButton.grid(row=0, column=1, padx=10, pady=10)

        addButton = tk.Button(self, image=self.add, fg='#2b99b3', command=self.addToDatabase)
        addButton.grid(row=0, column=0, pady=10, padx=10)

        self.buildPage()
        self.buildErrorLog()

    def buildPage(self):
        self.costwhat = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.costcost = tk.Entry(self, width=50, background=self.color,fg='white',  borderwidth=0)
        self.costPurchaseDay = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.costPurchaseMonth = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.costPurchaseYear = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        what = tk.Label(self, bg=self.color, fg='white', text="What: ")
        cost = tk.Label(self, bg=self.color, fg='white', text="Cost: ")
        purchaseDay = tk.Label(self, bg=self.color, fg='white', text="Purchase Day: ")
        purchaseMonth = tk.Label(self, bg=self.color, fg='white', text="Purchase Month: ")
        purchaseYear = tk.Label(self, bg=self.color, fg='white', text="Purchase Year: ")
        errorLog = tk.Label(self, bg=self.color, fg='white', text="Error Log: ")

        what.grid(row=1, column=0, sticky='ew', pady=10, padx=10)
        cost.grid(row=2, column=0, sticky='ew', pady=10, padx=10)
        purchaseDay.grid(row=3, column=0, sticky='ew', pady=10, padx=10)
        purchaseMonth.grid(row=4, column=0, sticky='ew', pady=10, padx=10)
        purchaseYear.grid(row=5, column=0, sticky='ew', pady=10, padx=10)
        errorLog.grid(row=2, column=2, pady=10, padx=10)
        self.costwhat.grid(row=1, column=1, pady=10, padx=10)
        self.costcost.grid(row=2, column=1, pady=10, padx=10)
        self.costPurchaseDay.grid(row=3, column=1, pady=10, padx=10)
        self.costPurchaseMonth.grid(row=4, column=1, pady=10, padx=10)
        self.costPurchaseYear.grid(row=5, column=1, pady=10, padx=10)

    def addToDatabase(self):
        self.errorLog.set("")
        what = self.costwhat.get()
        cost = self.costcost.get()
        day = self.costPurchaseDay.get()
        month = self.costPurchaseMonth.get()
        year = self.costPurchaseYear.get()

        safe = True

        if what == "":
            safe = False
            self.errorLog.set("Product Name Blank\n")
        try:
            cost = float(cost)
        except ValueError:
            safe = False
            self.errorLog.set('{}Purchase Cost Invalid\n'.format(self.errorLog.get()))

        if month != "":
            try:
                month = int(month)
            except ValueError:
                safe = False
                self.errorLog.set('{}Purchase Month Invalid\n'.format(self.errorLog.get()))

            try:
                day = int(day)
            except ValueError:
                safe = False
                self.errorLog.set('{}Purchase Day Invalid\n'.format(self.errorLog.get()))

            try:
                year = int(year)
            except ValueError:
                safe = False
                self.errorLog.set('{}Purchase Year Invalid\n'.format(self.errorLog.get()))

        else:
            self.errorLog.set("{}Purchase Date Blank\n".format(self.errorLog.get()))

        if safe:
            date = datetime.datetime(year, month, day)
            Cost.create(what=what, cost=cost, purchaseDate=date)
            self.errorLog.set("Added")

    def buildErrorLog(self, *args):
        log = tk.Label(self, background=self.color, fg='white', text=self.errorLog.get(), font=30)
        log.grid(row=1, column=3, rowspan=4, sticky='nsew', padx=10, pady=10)