import tkinter as tk
from peewee import *
import datetime
from databases import Cost
from tkinter import ttk

class viewCost(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.color = "#2b99b3"
        self.background = "#42d4f5"

        mainFrame = tk.Frame(self, parent)
        mainFrame.pack(fill="both", expand=1)
        canvas = tk.Canvas(mainFrame)
        canvas.pack(side="left", fill="both", expand=1)
        scrollBar = ttk.Scrollbar(mainFrame, orient='vertical', command=canvas.yview)
        scrollBar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollBar.set, background=self.background)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.frame = tk.Frame(canvas)
        self.frame.config(background=self.background)
        canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.configFrame()
        self.initStringVar()

        self.inventoryTracker = tk.PhotoImage(file='images/InventoryTracker.png')
        self.refresh = tk.PhotoImage(file='images/Refresh.png')
        self.delete = tk.PhotoImage(file='images/delete.png')

        label = tk.Button(self.frame, image=self.inventoryTracker, fg="#2b99b3", command=lambda: controller.showFrame("startPage"))
        refreshButton = tk.Button(self.frame, image=self.refresh, bg="#2b99b3", command=self.fillCosts)
        deleteButton = tk.Button(self.frame, image=self.delete, command=self.deletePage)

        label.grid(row=0,column=0,columnspan=2,sticky='nsew', pady=10, padx=10)
        refreshButton.grid(row=2, column=4, pady=10, padx=10)
        deleteButton.grid(row=4, column=4, pady=10, padx=10)

        self.buildPage()
        self.fillCosts()

    def fillCosts(self):
        costs = Cost.select().order_by(Cost.purchaseDate.desc())
        self.what.set("")
        self.cost.set("")
        self.date.set("")
        for cost in costs:
            self.what.set("{}{}\n".format(self.what.get(), cost.what))
            self.cost.set("{}{}\n".format(self.cost.get(), cost.cost))
            self.date.set("{}{}\n".format(self.date.get(), cost.purchaseDate.strftime('%B %d, %Y')))

    def deletePage(self):
        self.deleteErrorLog.set("")
        self.deletePage = tk.Toplevel(background=self.background)
        self.deletePage.title("Delete Costs")
        logo = tk.Label(self.deletePage, image=self.inventoryTracker)
        logo.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)
        error = tk.Label(self.deletePage, bg=self.color, fg='white', text="Error Log: ")
        error.grid(row=2, column=2, sticky='nsew', pady=10, padx=10)
        self.buildErrorLog()
        self.buildDeletePage()

    def buildDeletePage(self):
        self.delWhat = tk.Entry(self.deletePage, fg='white', width=50, background=self.color, borderwidth=0)
        self.delCost = tk.Entry(self.deletePage, fg='white', width=50, background=self.color, borderwidth=0)
        self.delDay = tk.Entry(self.deletePage, fg='white', width=50, background=self.color, borderwidth=0)
        self.delMonth = tk.Entry(self.deletePage, fg='white', width=50, background=self.color, borderwidth=0)
        self.delYear = tk.Entry(self.deletePage, fg='white', width=50, background=self.color, borderwidth=0)
        name = tk.Label(self.deletePage, bg=self.color, fg='white', text="Name of the expense: ")
        size = tk.Label(self.deletePage, bg=self.color, fg='white', text="Cost of the expense: ")
        pday = tk.Label(self.deletePage, bg=self.color, fg='white', text="Purchase Day: ")
        pmonth = tk.Label(self.deletePage, bg=self.color, fg='white', text="Purchase Month: ")
        pyear = tk.Label(self.deletePage, bg=self.color, fg='white', text="Purchase Year: ")
        deleteButton = tk.Button(self.deletePage, image=self.delete, command=self.deleteEntry)

        self.delWhat.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
        self.delCost.grid(row=2, column=1, sticky='nsew', pady=10, padx=10)
        self.delDay.grid(row=3, column=1, sticky='nsew', pady=10, padx=10)
        self.delMonth.grid(row=4, column=1, sticky='nsew', pady=10, padx=10)
        self.delYear.grid(row=5, column=1, sticky='nsew', pady=10, padx=10)
        name.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
        size.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)
        pday.grid(row=3, column=0, sticky='nsew', pady=10, padx=10)
        pmonth.grid(row=4, column=0, sticky='nsew', pady=10, padx=10)
        pyear.grid(row=5, column=0, sticky='nsew', pady=10, padx=10)
        deleteButton.grid(row=0, column=1, padx=10, pady=10)

    def deleteEntry(self):
        what = self.delWhat.get()
        cost = self.delCost.get()
        day = self.delDay.get()
        month = self.delMonth.get()
        year = self.delYear.get()

        self.deleteErrorLog.set("")

        safe = True

        if what == "":
            self.deleteErrorLog.set("Expense Name Invalid\n")
            safe = False
        try:
            cost = float(cost)
        except ValueError:
            self.deleteErrorLog.set("{}Cost Invalid\n".format(self.deleteErrorLog.get()))
            safe = False
        try:
            day = int(day)
        except ValueError:
            self.deleteErrorLog.set("{}Purchase Day Invalid\n".format(self.deleteErrorLog.get()))
            safe = False
        try:
            month = int(month)
        except ValueError:
            self.deleteErrorLog.set("{}Purchase Month Invalid\n".format(self.deleteErrorLog.get()))
            safe = False
        try:
            year = int(year)
        except ValueError:
            self.deleteErrorLog.set("{}Purchase Year Invalid\n".format(self.deleteErrorLog.get()))
            safe = False

        if safe:
            #Add try statement
            date = datetime.datetime(year, month, day)
            for expense in Cost.select():
                if (expense.what == what) and (expense.cost == cost) and (expense.purchaseDate == date):
                    expense.delete_instance()
                    self.deleteErrorLog.set("Deleted")
                    return
            self.deleteErrorLog.set("Cost not found")

    def configFrame(self):
        self.frame.columnconfigure(index=0, weight=1)
        self.frame.columnconfigure(index=1, weight=1)
        self.frame.columnconfigure(index=2, weight=1)
        self.frame.columnconfigure(index=3, weight=1)
        self.frame.columnconfigure(index=4, weight=1)
        self.frame.rowconfigure(index=0, weight=0)
        self.frame.rowconfigure(index=1, weight=0)

    def initStringVar(self):
        self.what = tk.StringVar()
        self.what.trace('w', self.buildWhat)

        self.cost = tk.StringVar()
        self.cost.trace('w', self.buildCost)

        self.date = tk.StringVar()
        self.date.trace('w', self.buildDate)

        self.deleteErrorLog = tk.StringVar()
        self.deleteErrorLog.trace('w', self.buildErrorLog)

    def buildErrorLog(self, *args):
        text = tk.Label(self.deletePage, background=self.color, foreground='white', text=self.deleteErrorLog.get(),font=30)
        text.grid(row=1, column=3, rowspan=3, sticky='nsew', pady=10, padx=10)

    def buildPage(self, *args):
        what = tk.Label(self.frame, bg=self.color, fg='white', text='Expense')
        cost = tk.Label(self.frame, bg=self.color, fg='white', text='Cost')
        date = tk.Label(self.frame, bg=self.color, fg='white', text='Purchase Date')

        what.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
        cost.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
        date.grid(row=1, column=2, sticky='nsew', pady=10, padx=10)

    def buildWhat(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.what.get(), font=30)
        text.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)

    def buildCost(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.cost.get(), font=30)
        text.grid(row=2, column=1, sticky='nsew', pady=10, padx=10)

    def buildDate(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.date.get(), font=30)
        text.grid(row=2, column=2, sticky='nsew', pady=10, padx=10)
