import tkinter as tk
from peewee import *
import datetime
from databases import Cost
from databases import Entry
from matplotlib import pyplot as plt

class analysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        color = "#2b99b3"
        background = "#42d4f5"
        tk.Frame.config(self, background=background)
        tk.Frame.rowconfigure(self, index=0, weight=0)
        tk.Frame.rowconfigure(self, index=1, weight=1)
        tk.Frame.rowconfigure(self, index=2, weight=1)
        tk.Frame.rowconfigure(self, index=3, weight=1)
        tk.Frame.columnconfigure(self, index=0, weight=0)
        tk.Frame.columnconfigure(self, index=1, weight=1)
        tk.Frame.columnconfigure(self, index=2, weight=1)

        self.inventoryTracker = tk.PhotoImage(file='images/InventoryTracker.png')
        self.profitCost = tk.PhotoImage(file='images/CostVsProfit.png')
        self.sizecost = tk.PhotoImage(file='images/sizeVSprofit.png')
        self.purchaseProfit = tk.PhotoImage(file='images/purchaseVSprofit.png')
        self.purchaseSold = tk.PhotoImage(file='images/purchaseVSsold.png')
        self.soldProfit = tk.PhotoImage(file='images/soldVSprofit.png')
        self.soldPriceProfit = tk.PhotoImage(file='images/soldpriceVSprofit.png')
        startPageButton = tk.Button(self, image=self.inventoryTracker, fg="#2b99b3",command=lambda: controller.showFrame("startPage"))
        startPageButton.grid(row=0, column=0, padx=10, pady=10)


        self.getData()
        profitCostButton = tk.Button(self, image = self.profitCost, fg= "#2b99b3", command=self.profitVScost)
        profitCostButton.grid(row=1, column=1, pady=10, padx=10)

        sizeProfitButton = tk.Button(self, image=self.sizecost, fg = "#2b99b3", command=self.sizeVSprofit)
        sizeProfitButton.grid(row=2, column=1, pady=10, padx=10)

        soldPriceProfitButton = tk.Button(self, image=self.soldPriceProfit, command=self.soldpriceVSprofit)
        soldPriceProfitButton.grid(row=3, column=1, pady=10, padx=10)

        purchaseDayProfitButton = tk.Button(self, image=self.purchaseProfit, command=self.purchaseVSprofit)
        purchaseDayProfitButton.grid(row=1, column=2, pady=10, padx=10)

        soldDayProfitButton = tk.Button(self, image=self.soldProfit, command=self.soldVSprofit)
        soldDayProfitButton.grid(row=2, column=2, pady=10, padx=10)

        soldDayPurchaseDayButton = tk.Button(self, image=self.purchaseSold, command=self.purchaseVSsold)
        soldDayPurchaseDayButton.grid(row=3, column=2, pady=10, padx=10)




    def profitVScost(self):
        plt.scatter(self.shoeCost, self.shoeProfit)
        plt.ylabel("Profit")
        plt.xlabel("Cost")
        plt.title("Cost vs Profit")
        plt.show()

    def purchaseVSprofit(self):
        plt.scatter(self.shoePurchaseDay, self.shoeProfit)
        plt.ylabel("Profit")
        plt.xlabel("Purchase Date")
        plt.title("Purchase Date vs Profit")
        plt.show()

    def soldVSprofit(self):
        plt.scatter(self.shoeSoldDay, self.shoeProfit)
        plt.ylabel("Profit")
        plt.xlabel("Sold Date")
        plt.title("Sold Date vs Profit")
        plt.show()

    def soldpriceVSprofit(self):
        plt.scatter(self.shoeSoldPrice, self.shoeProfit)
        plt.ylabel("Sold Date")
        plt.xlabel("Sold Price")
        plt.title("Sold Price vs Profit")
        plt.show()

    def purchaseVSsold(self):
        plt.scatter(self.shoePurchaseDay, self.shoeSoldDay)
        plt.ylabel("Sold Date")
        plt.xlabel("Purchase Date")
        plt.title("Purchase Date vs Sold Date")
        plt.show()

    def sizeVSprofit(self):
        plt.scatter(self.shoeSize, self.shoeProfit)
        plt.ylabel("Profit")
        plt.xlabel("Size")
        plt.title("Size vs Profit")
        plt.show()

    def getData(self):
        self.shoeCost = []
        self.shoeProfit = []
        self.shoeSize = []
        self.shoePurchaseDay = []
        self.shoeSoldDay = []
        self.shoeSoldPrice = []
        for entry in Entry:
            if entry.soldCost > 0:
                self.shoeCost.append(entry.purchaseCost)
                self.shoeProfit.append(entry.soldCost-entry.purchaseCost)
                try:
                    float(entry.size)
                    self.shoeSize.append(entry.size)
                except ValueError:
                    pass
                self.shoePurchaseDay.append(entry.purchaseDate)
                self.shoeSoldDay.append(entry.soldDate)
                self.shoeSoldPrice.append(entry.soldCost)
            else:
                pass
