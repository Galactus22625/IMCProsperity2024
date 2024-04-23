import csv
import statistics
import numpy
import matplotlib.pyplot as plt


prices = {}

def findprices(filename):
    with open(filename, mode = "r") as file:
        csvfile = csv.reader(file)
        next(csvfile)
        for data in csvfile:
            line = data[0].split(";")
            currentproduct = line[2]
            if currentproduct not in prices:
                prices[currentproduct] = []
            prices[currentproduct].append(float(line[15]))

def showprices(product):
    x = [a for a in range(len(prices[product]))]
    y = prices[product]

    plt.plot(x, y)
    plt.title(f"Prices for {product}")
    plt.show()
    plt.clf()

findprices("TestingData.csv")

for product in prices:
    showprices(product)


