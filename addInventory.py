import tkinter as tk
from peewee import *
import datetime
from databases import Entry

class addInventory(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.columnconfigure(self, index=0, weight=0)
        tk.Frame.columnconfigure(self, index=1, weight=0)
        tk.Frame.columnconfigure(self, index=2, weight=0)
        tk.Frame.rowconfigure(self, index=0, weight=0)
        tk.Frame.rowconfigure(self, index=1, weight=0)

        self.errorLog = tk.StringVar()
        self.errorLog.trace('w', self.buildErrorLog)

        self.color = "#2b99b3"
        self.background = "#42d4f5"

        tk.Frame.config(self, background=self.background)

        self.add = tk.PhotoImage(file='images/add.png')
        self.inventoryTracker = tk.PhotoImage(file='images/InventoryTracker.png')

        startPageButton = tk.Button(self, image=self.inventoryTracker, fg="#2b99b3", command=lambda: controller.showFrame("startPage"))
        startPageButton.grid(row=0, column=1, padx=10, pady=10)

        addButton = tk.Button(self, image=self.add, fg='#2b99b3', command=self.addToDatabase)
        addButton.grid(row=0, column=0, pady=10, padx=10)

        self.buildPage()
        self.buildErrorLog()

    def buildPage(self):
        name = tk.Label(self, bg=self.color, fg='white', text='Shoe Name: ')
        size = tk.Label(self, bg=self.color, fg='white', text='Shoe Size: ')
        pinfo = tk.Label(self, bg=self.color, fg='white', text='Purchasing Info')
        pcost = tk.Label(self, bg=self.color, fg='white', text='Purchase Cost: ')
        pday = tk.Label(self, bg=self.color, fg='white', text='Purchase Day: ')
        pmonth = tk.Label(self, bg=self.color, fg='white', text='Purchase Month: ')
        pyear = tk.Label(self, bg=self.color, fg='white', text='Purchase Year: ')
        sinfo = tk.Label(self, bg=self.color, fg='white', text='Sold Info (Leave blank if not sold yet)')
        sprice = tk.Label(self, bg=self.color, fg='white', text='Sold Price: ')
        sday = tk.Label(self, bg=self.color, fg='white', text='Sold Day: ')
        smonth = tk.Label(self, bg=self.color, fg='white', text='Sold Month: ')
        syear = tk.Label(self, bg=self.color, fg='white', text='Sold Year: ')
        sLocation = tk.Label(self, bg=self.color, fg='white', text='Sold Location: ')
        errorLog = tk.Label(self, bg=self.color, fg='white', text='Error Log: ')

        self.name = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.size = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.pcost = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.pday = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.pmonth = tk.Entry(self, width=50, background=self.color,fg='white',  borderwidth=0)
        self.pyear = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.sprice = tk.Entry(self, width=50, background=self.color,fg='white',  borderwidth=0)
        self.sday = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.smonth = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.syear = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)
        self.sLocation = tk.Entry(self, width=50, background=self.color, fg='white', borderwidth=0)

        name.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
        size.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)
        pinfo.grid(row=3, column=0, sticky='nsew', pady=10, padx=10, columnspan=2)
        pcost.grid(row=4, column=0, sticky='nsew', pady=10, padx=10)
        pday.grid(row=5, column=0, sticky='nsew', pady=10, padx=10)
        pmonth.grid(row=6, column=0, sticky='nsew', pady=10, padx=10)
        pyear.grid(row=7, column=0, sticky='nsew', pady=10, padx=10)
        sinfo.grid(row=8, column=0, sticky='nsew', pady=10, padx=10, columnspan=2)
        sprice.grid(row=9, column=0, sticky='nsew', pady=10, padx=10)
        sday.grid(row=10, column=0, sticky='nsew', pady=10, padx=10)
        smonth.grid(row=11, column=0, sticky='nsew', pady=10, padx=10)
        syear.grid(row=12, column=0, sticky='nsew', pady=10, padx=10)
        sLocation.grid(row=13, column=0, sticky='nsew', pady=10, padx=10)
        errorLog.grid(row=4, column=2, sticky='nsew', pady=10, padx=10)

        self.name.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
        self.size.grid(row=2, column=1, sticky='nsew', pady=10, padx=10)
        self.pcost.grid(row=4, column=1, sticky='nsew', pady=10, padx=10)
        self.pday.grid(row=5, column=1, sticky='nsew', pady=10, padx=10)
        self.pmonth.grid(row=6, column=1, sticky='nsew', pady=10, padx=10)
        self.pyear.grid(row=7, column=1, sticky='nsew', pady=10, padx=10)
        self.sprice.grid(row=9, column=1, sticky='nsew', pady=10, padx=10)
        self.sday.grid(row=10, column=1, sticky='nsew', pady=10, padx=10)
        self.smonth.grid(row=11, column=1, sticky='nsew', pady=10, padx=10)
        self.syear.grid(row=12, column=1, sticky='nsew', pady=10, padx=10)
        self.sLocation.grid(row=13, column=1, sticky='nsew', pady=10, padx=10)

    def buildErrorLog(self, *args):
        log = tk.Label(self, background=self.color, fg='white', text=self.errorLog.get(), font=30)
        log.grid(row=3, column=3, rowspan=4,sticky='nsew', padx=10, pady=10)

    def addToDatabase(self):
        self.errorLog.set("")
        name = self.name.get()
        size = self.size.get()
        pcost = self.pcost.get()
        pday = self.pday.get()
        pmonth = self.pmonth.get()
        pyear = self.pyear.get()
        sprice = self.sprice.get()
        sday = self.sday.get()
        smonth = self.smonth.get()
        syear = self.syear.get()
        sLocation = self.sLocation.get()

        safe = True
        try:
            size = float(size)
        except ValueError:
            safe = False
            self.errorLog.set('Size Invalid\n')

        try:
            pcost = float(pcost)
        except ValueError:
            safe = False
            self.errorLog.set('{}Purchase Cost Invalid\n'.format(self.errorLog.get()))

        try:
            pmonth = int(pmonth)
        except ValueError:
            safe = False
            self.errorLog.set('{}Purchase Month Invalid\n'.format(self.errorLog.get()))

        try:
            pday = int(pday)
        except ValueError:
            safe = False
            self.errorLog.set('{}Purchase Day Invalid\n'.format(self.errorLog.get()))

        try:
            pyear = int(pyear)
        except ValueError:
            safe = False
            self.errorLog.set('{}Purchase Year Invalid\n'.format(self.errorLog.get()))
        if sprice != "":
            try:
                scost = float(sprice)
            except ValueError:
                safe = False
                self.errorLog.set('{}Sold Cost Invalid\n'.format(self.errorLog.get()))
        else:
            scost = 0

        if smonth != "":
            try:
                smonth = int(smonth)
            except ValueError:
                safe = False
                self.errorLog.set('{}Sold Month Invalid\n'.format(self.errorLog.get()))

            try:
                sday = int(sday)
            except ValueError:
                safe = False
                self.errorLog.set('{}Sold Day Invalid\n'.format(self.errorLog.get()))

            try:
                syear = int(syear)
            except ValueError:
                safe = False
                self.errorLog.set('{}Sold Year Invalid\n'.format(self.errorLog.get()))
        else:
            smonth = 1
            sday = 1
            syear = 2000

        if safe:
            pdate = datetime.datetime(pyear, pmonth, pday)
            sdate = datetime.datetime(syear, smonth, sday)
            Entry.create(name=name, size=size, purchaseCost=pcost, purchaseDate=pdate, soldCost=scost, soldDate=sdate,
                         soldLocation=sLocation)
            self.errorLog.set("Added")