import tkinter as tk
from peewee import *
import datetime
from databases import Entry
from tkinter import ttk

class viewInventory(tk.Frame):
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
        canvas.bind('<Configure>', lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        self.frame = tk.Frame(canvas)
        self.frame.config(background=self.background)
        canvas.create_window((0,0), window=self.frame, anchor='nw')

        self.configFrame()
        self.initStringVar()

        self.inventoryTracker = tk.PhotoImage(file='images/InventoryTracker.png')
        self.refresh = tk.PhotoImage(file='images/Refresh.png')
        self.edit = tk.PhotoImage(file='images/edit.png')
        self.delete = tk.PhotoImage(file='images/delete.png')

        label = tk.Button(self.frame, image=self.inventoryTracker, fg="#2b99b3", command=lambda: controller.showFrame("startPage"))
        refreshButton = tk.Button(self.frame, image=self.refresh, bg="#2b99b3",  command=self.fillInventory)
        editButton = tk.Button(self.frame, image=self.edit, command=self.editPage)
        deleteButton = tk.Button(self.frame, image=self.delete, command=self.deletePage)

        label.grid(row=0,column=0,columnspan=2,sticky='ns', pady=10, padx=10)
        refreshButton.grid(row=0, column=2, pady=10, padx=10)
        editButton.grid(row=0, column=4, pady=10, padx=10)
        deleteButton.grid(row=0, column=5, pady=10, padx=10)

        self.buildPage()
        self.fillInventory()

    def initStringVar(self):
        self.name = tk.StringVar()
        self.name.trace('w', self.buildName)

        self.size = tk.StringVar()
        self.size.trace('w', self.buildSize)

        self.pCost = tk.StringVar()
        self.pCost.trace('w', self.buildPCost)

        self.pDate = tk.StringVar()
        self.pDate.trace('w', self.buildPDate)

        self.sPrice = tk.StringVar()
        self.sPrice.trace('w', self.buildSPrice)

        self.sDate = tk.StringVar()
        self.sDate.trace('w', self.buildSDate)

        self.sLocation = tk.StringVar()
        self.sLocation.trace('w', self.buildSLocation)

        self.profit = tk.StringVar()
        self.profit.trace('w', self.buildProfit)

        self.deleteErrorLog = tk.StringVar()
        self.deleteErrorLog.trace('w', self.buildDeleteErrorLog)

        self.editErrorLog = tk.StringVar()
        self.editErrorLog.trace('w', self.buildEditErrorLog)

    def configFrame(self):
        self.frame.columnconfigure(index=0, weight=0)
        self.frame.columnconfigure(index=1, weight=0)
        self.frame.columnconfigure(index=2, weight=0)
        self.frame.rowconfigure(index=0, weight=0)
        self.frame.rowconfigure(index=1, weight=0)

    def fillInventory(self):
        entries = Entry.select().order_by(Entry.purchaseDate.asc())
        self.name.set("")
        self.size.set("")
        self.pCost.set("")
        self.pDate.set("")
        self.sPrice.set("")
        self.sDate.set("")
        self.sLocation.set("")
        self.profit.set("")
        for entry in entries:
            self.name.set("{}{}\n\n".format(self.name.get(), entry.name))
            self.size.set("{}{}\n\n".format(self.size.get(), entry.size))
            self.pCost.set("{}${}\n\n".format(self.pCost.get(), entry.purchaseCost))
            self.pDate.set("{}{}\n\n".format(self.pDate.get(), entry.purchaseDate.strftime('%B %d, %Y')))
            if entry.soldCost == 0.0:
                self.sPrice.set("{}\n\n".format(self.sPrice.get()))
            else:
                self.sPrice.set("{}${}\n\n".format(self.sPrice.get(), entry.soldCost))
            if entry.soldDate.strftime('%B %d, %Y') == "January 01, 2000":
                self.sDate.set("{}\n\n".format(self.sDate.get()))
            else:
                self.sDate.set("{}{}\n\n".format(self.sDate.get(), entry.soldDate.strftime('%B %d, %Y')))
            self.sLocation.set("{}{}\n\n".format(self.sLocation.get(), entry.soldLocation))
            self.profit.set("{}${}\n\n".format(self.profit.get(), int(entry.soldCost-entry.purchaseCost)))

    def editPage(self):
        self.editErrorLog.set("")
        self.editPage = tk.Toplevel(background=self.background)
        self.editPage.title("Edit Inventory")
        logo = tk.Label(self.editPage, image=self.inventoryTracker)
        logo.grid(row=0, column=1, pady=10, padx=10)
        edit = tk.Button(self.editPage, image=self.edit, command=self.editEntry)
        edit.grid(row=0, column=0, padx=10, pady=10)
        self.editTitles()
        self.buildEditErrorLog()

    def editTitles(self):
        name = tk.Label(self.editPage, bg=self.color, fg='white', text='Shoe Name: ')
        size = tk.Label(self.editPage, bg=self.color, fg='white', text='Shoe Size: ')
        pinfo = tk.Label(self.editPage, bg=self.color, fg='white', text='Purchasing Info')
        pcost = tk.Label(self.editPage, bg=self.color, fg='white', text='Purchase Cost: ')
        pday = tk.Label(self.editPage, bg=self.color, fg='white', text='Purchase Day: ')
        pmonth = tk.Label(self.editPage, bg=self.color, fg='white', text='Purchase Month: ')
        pyear = tk.Label(self.editPage, bg=self.color, fg='white', text='Purchase Year: ')
        sinfo = tk.Label(self.editPage, bg=self.color, fg='white', text='Sold Info (Leave blank if not sold yet)')
        scost = tk.Label(self.editPage, bg=self.color, fg='white', text='Sold Cost: ')
        sday = tk.Label(self.editPage, bg=self.color, fg='white', text='Sold Day: ')
        smonth = tk.Label(self.editPage, bg=self.color, fg='white', text='Sold Month: ')
        syear = tk.Label(self.editPage, bg=self.color, fg='white', text='Sold Year: ')
        sLocation = tk.Label(self.editPage, bg=self.color, fg='white', text='Sold Location: ')
        errorLog = tk.Label(self.editPage, bg=self.color, fg='white', text='Error Log: ')
        self.ename = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.esize = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.epcost = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.epday = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.epmonth = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.epyear = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.escost = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.esday = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.esmonth = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.esyear = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)
        self.esLocation = tk.Entry(self.editPage, width=50, bg=self.color, fg='white', borderwidth=0)

        name.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
        size.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)
        pinfo.grid(row=3, column=0, sticky='nsew', pady=10, padx=10, columnspan=2)
        pcost.grid(row=4, column=0, sticky='nsew', pady=10, padx=10)
        pday.grid(row=5, column=0, sticky='nsew', pady=10, padx=10)
        pmonth.grid(row=6, column=0, sticky='nsew', pady=10, padx=10)
        pyear.grid(row=7, column=0, sticky='nsew', pady=10, padx=10)
        sinfo.grid(row=8, column=0, sticky='nsew', pady=10, padx=10, columnspan=2)
        scost.grid(row=9, column=0, sticky='nsew', pady=10, padx=10)
        sday.grid(row=10, column=0, sticky='nsew', pady=10, padx=10)
        smonth.grid(row=11, column=0, sticky='nsew', pady=10, padx=10)
        syear.grid(row=12, column=0, sticky='nsew', pady=10, padx=10)
        sLocation.grid(row=13, column=0, sticky='nsew', pady=10, padx=10)
        errorLog.grid(row=4, column=2, sticky='nsew', pady=10, padx=10)

        self.ename.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
        self.esize.grid(row=2, column=1, sticky='nsew', pady=10, padx=10)
        self.epcost.grid(row=4, column=1, sticky='nsew', pady=10, padx=10)
        self.epday.grid(row=5, column=1, sticky='nsew', pady=10, padx=10)
        self.epmonth.grid(row=6, column=1, sticky='nsew', pady=10, padx=10)
        self.epyear.grid(row=7, column=1, sticky='nsew', pady=10, padx=10)
        self.escost.grid(row=9, column=1, sticky='nsew', pady=10, padx=10)
        self.esday.grid(row=10, column=1, sticky='nsew', pady=10, padx=10)
        self.esmonth.grid(row=11, column=1, sticky='nsew', pady=10, padx=10)
        self.esyear.grid(row=12, column=1, sticky='nsew', pady=10, padx=10)
        self.esLocation.grid(row=13, column=1, sticky='nsew', pady=10, padx=10)

    def editEntry(self):
        self.editErrorLog.set("")
        name = self.ename.get()
        size = self.esize.get()
        pcost = self.epcost.get()
        pday = self.epday.get()
        pmonth = self.epmonth.get()
        pyear = self.epyear.get()
        scost = self.escost.get()
        sday = self.esday.get()
        smonth = self.esmonth.get()
        syear = self.esyear.get()
        sLocation = self.esLocation.get()

        if name == "":
            self.editErrorLog.set("Name invalid\n")
        if size == "":
            self.editErrorLog.set("{}Size invalid\n".format(self.editErrorLog.get()))
        else:
            try:
                size = float(size)
            except ValueError:
                self.editErrorLog.set("{}Size invalid\n".format(self.editErrorLog.get()))

        if self.editErrorLog.get() == "":
            entryUpdated = False
            for entry in Entry.select():
                if not entryUpdated:
                    if (entry.name==name) and (entry.size == size):
                        if pcost !="":
                            pcost = float(pcost)
                            if entry.purchaseCost !=pcost:
                                entry.purchaseCost = pcost
                                entry.save(force_insert=False)
                                self.editErrorLog.set("{}Purchase Cost Updated".format(self.editErrorLog.get()))
                                entryUpdated = True

                        if (pday!="") and (pmonth!="") and (pyear!=""):
                            valid = True
                            try:
                                pday = int(pday)
                            except ValueError:
                                self.editErrorLog.set("{}Purchase Day invalid\n".format(self.editErrorLog.get()))
                                valid=False
                            try:
                                pmonth = int(pmonth)
                            except ValueError:
                                self.editErrorLog.set("{}Purchase Month invalid\n".format(self.editErrorLog.get()))
                                valid = False
                            try:
                                pyear = int(pyear)
                            except ValueError:
                                self.editErrorLog.set("{}Purchase Year invalid\n".format(self.editErrorLog.get()))
                                valid = False
                            if valid:
                                pdate = datetime.datetime(pyear, pmonth, pday)
                                if pdate != entry.purchaseDate:
                                    entry.purchaseDate=pdate
                                    entry.save(force_insert=False)
                                    self.editErrorLog.set("{}Purchase Date Updated".format(self.editErrorLog.get()))
                                    entryUpdated = True

                        if scost !="":
                            scost = float(scost)
                            if entry.soldCost !=scost:
                                entry.soldCost=scost
                                entry.save(force_insert=False)
                                self.editErrorLog.set("{}Sold Cost Updated".format(self.editErrorLog.get()))
                                entryUpdated = True

                        if (sday!="") and (smonth!="") and (syear!=""):
                            valid = True
                            try:
                                sday = int(sday)
                            except ValueError:
                                self.editErrorLog.set("{}Sold Day invalid\n".format(self.editErrorLog.get()))
                                valid=False
                            try:
                                smonth = int(smonth)
                            except ValueError:
                                self.editErrorLog.set("{}Sold Month invalid\n".format(self.editErrorLog.get()))
                                valid = False
                            try:
                                syear = int(syear)
                            except ValueError:
                                self.editErrorLog.set("{}Sold Year invalid\n".format(self.editErrorLog.get()))
                                valid = False
                            if valid:
                                sdate = datetime.datetime(syear, smonth, sday)
                                if sdate != entry.soldDate:
                                    entry.soldDate=sdate
                                    entry.save(force_insert=False)
                                    self.editErrorLog.set("{}Sold Date Updated".format(self.editErrorLog.get()))
                                    entryUpdated = True

                        if sLocation!="":
                            if sLocation != entry.soldLocation:
                                entry.soldLocation=sLocation
                                entry.save(force_insert=False)
                                self.editErrorLog.set("{}Sold Location Updated".format(self.editErrorLog.get()))
                                entryUpdated = True

                if entryUpdated:
                    break

    def deletePage(self):
        self.deleteErrorLog.set("")
        self.deletePage = tk.Toplevel(background=self.background)
        self.deletePage.title("Delete Inventory")
        logo = tk.Label(self.deletePage, image=self.inventoryTracker)
        logo.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)
        error = tk.Label(self.deletePage, bg=self.color, fg='white', text="Error Log: ")
        error.grid(row=1, column=2, sticky='nsew', pady=10, padx=10)
        self.buildDeleteErrorLog()
        self.delname = tk.Entry(self.deletePage, fg='white', width=50, background=self.color, borderwidth=0)
        self.delsize = tk.Entry(self.deletePage, fg='white', width=50, background=self.color, borderwidth=0)
        name = tk.Label(self.deletePage, bg=self.color, fg='white', text="Name of the shoe: ")
        size = tk.Label(self.deletePage, bg=self.color, fg='white',text="Size of the Shoe: ")
        deleteButton = tk.Button(self.deletePage, image=self.delete, command=self.deleteEntry)

        name.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
        size.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)
        self.delname.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
        self.delsize.grid(row=2, column=1, sticky='nsew', pady=10, padx=10)
        deleteButton.grid(row=0, column=1, padx=10, pady=10)

    def deleteEntry(self):
        name = self.delname.get()
        size = self.delsize.get()
        self.deleteErrorLog.set("")
        if name == "":
            self.deleteErrorLog.set("Shoe name invalid\n")
        try:
            size = float(size)
        except ValueError:
            self.deleteErrorLog.set("{}Size invalid".format(self.deleteErrorLog.get()))
            return

        for entry in Entry.select():
            if (entry.name == name) and (entry.size == size):
                entry.delete_instance()
                self.deleteErrorLog.set('Deleted')
                return
        self.deleteErrorLog.set("Shoe not found")

    def buildEditErrorLog(self, *args):
        log = tk.Label(self.editPage, background=self.color, foreground='white', text=self.editErrorLog.get(), font=30)
        log.grid(row=3, rowspan=4, column=3, sticky='nsew', pady=10, padx=10)

    def buildDeleteErrorLog(self, *args):
        text = tk.Label(self.deletePage, background=self.color, foreground='white', text=self.deleteErrorLog.get(), font=30)
        text.grid(row=1, column=3, sticky='nsew', pady=10, padx=10)

    def buildPage(self, *args):
        name = tk.Label(self.frame, bg=self.color, fg='white', text='Shoe Name')
        size = tk.Label(self.frame, bg=self.color, fg='white', text='Shoe Size')
        pcost = tk.Label(self.frame, bg=self.color, fg='white', text='Purchase Cost')
        pdate = tk.Label(self.frame, bg=self.color, fg='white', text='Purchase Date')
        scost = tk.Label(self.frame, bg=self.color, fg='white', text='Sold Cost')
        sdate = tk.Label(self.frame, bg=self.color, fg='white', text='Sold Date')
        sLocation = tk.Label(self.frame, bg=self.color, fg='white', text='Sold Location')
        profit = tk.Label(self.frame, bg=self.color, fg='white', text='Profit')

        name.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
        size.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)
        pcost.grid(row=1, column=2, sticky='nsew', pady=10, padx=10)
        pdate.grid(row=1, column=3, sticky='nsew', pady=10, padx=10)
        scost.grid(row=1, column=4, sticky='nsew', pady=10, padx=10)
        sdate.grid(row=1, column=5, sticky='nsew', pady=10, padx=10)
        sLocation.grid(row=1, column=6, sticky='nsew', pady=10, padx=10)
        profit.grid(row=1, column=7, sticky='nsew', pady=10, padx=10)

    def buildName(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.name.get(),font=30)
        text.grid(row=3, column=0, sticky='nsew', pady=10, padx=10)

    def buildSize(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.size.get(), font=30)
        text.grid(row=3, column=1, sticky='nsew', pady=10, padx=10)

    def buildPCost(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.pCost.get(), font=30)
        text.grid(row=3, column=2, sticky='nsew', pady=10, padx=10)

    def buildPDate(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.pDate.get(), font=30)
        text.grid(row=3, column=3, sticky='nsew', pady=10, padx=10)

    def buildSPrice(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.sPrice.get(), font=30)
        text.grid(row=3, column=4, sticky='nsew', pady=10, padx=10)

    def buildSDate(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.sDate.get(), font=30)
        text.grid(row=3, column=5, sticky='nsew', pady=10, padx=10)

    def buildSLocation(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.sLocation.get(), font=30)
        text.grid(row=3, column=6, sticky='nsew', pady=10, padx=10)

    def buildProfit(self, *args):
        text = tk.Label(self.frame, background=self.color, foreground='white', text=self.profit.get(), font=30)
        text.grid(row=3, column=7, sticky='nsew', pady=10, padx=10)