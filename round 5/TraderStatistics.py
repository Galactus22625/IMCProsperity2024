import csv
import statistics
import numpy
import matplotlib.pyplot as plt

Products = {}

class productTraders:
    def __init__(self, product, buyers = None, sellers = None):
        if buyers == None:
            self.buyers = set()
        else:
            self.buyers = buyers
        if sellers == None:
            self.sellers = set()
        else:
            self.sellers = sellers
        self.product = product

class Trades:
    def __init__(self, timestamp, price, quantity):
        self.timestamp = int(timestamp)
        self.price = float(price)
        self.quantity = int(quantity)

class Snake:
    def __init__(self, name):
        self.name = name
        self.tradeHistoryBuys = {}          #key is product, list of buy trades
        self.tradeHistorySells = {}         #key is product, list of sell trades

    def addTrade(self, product, timestamp, price, quantity, buyorsell):
        if buyorsell == "BUY":
            if product not in self.tradeHistoryBuys:
                self.tradeHistoryBuys[product] = []
            self.tradeHistoryBuys[product].append(Trades(timestamp, price, quantity))
        elif buyorsell == "SELL":
            if product not in self.tradeHistorySells:
                self.tradeHistorySells[product] = []
            self.tradeHistorySells[product].append(Trades(timestamp, price, quantity))

snakes = {}

def processround5data(files):
    for filenum, filename in enumerate(files):
        daycounter = filenum %3
        with open(filename, mode = "r") as file:
            csvfile = csv.reader(file)
            next(csvfile)
            for data in csvfile:
                line = data[0].split(";")
                product = line[3]
                buyer = line[1]
                seller = line[2]
                timestamp = int(line[0]) + daycounter * 1000000
                price = line[5]
                quantity = line[6]
                if buyer not in snakes:
                    snakes[buyer] = Snake(buyer)
                if seller not in snakes:
                    snakes[seller] = Snake(seller)
                snakes[buyer].addTrade(product, timestamp, price, quantity, "BUY")
                snakes[seller].addTrade(product,timestamp, price, quantity, "SELL")

Prices = {}
def processpricedata(files):
    for filenum, filename in enumerate(files):
        daycounter = filenum %3
        with open(filename, mode = "r") as file:
            csvfile = csv.reader(file)
            next(csvfile)
            for data in csvfile:
                line = data[0].split(";")
                product = line[2]
                price = float(line[15])
                timestamp = int(line[1]) + daycounter * 1000000
                if product not in Prices:
                    Prices[product] ={}
                Prices[product][timestamp] = price

def FindTraders(files):
    for filename in files:
        with open(filename, mode = "r") as file:
            csvfile = csv.reader(file)
            next(csvfile)
            for data in csvfile:
                line = data[0].split(";")
                product = line[3]
                if product not in Products.keys():
                    productstraders = productTraders(product)
                    Products[product] = productstraders
                Products[product].buyers.add(line[1])
                Products[product].sellers.add(line[2])

files = ["round-5-island-data-bottle/trades_round_1_day_-2_wn.csv", "round-5-island-data-bottle/trades_round_1_day_-1_wn.csv","round-5-island-data-bottle/trades_round_1_day_0_wn.csv", "round-5-island-data-bottle/trades_round_3_day_0_wn.csv","round-5-island-data-bottle/trades_round_3_day_1_wn.csv", "round-5-island-data-bottle/trades_round_3_day_2_wn.csv",  "round-5-island-data-bottle/trades_round_4_day_1_wn.csv", "round-5-island-data-bottle/trades_round_4_day_2_wn.csv", "round-5-island-data-bottle/trades_round_4_day_3_wn.csv"]
pricefiles = ["../round 1/round-1-island-data-bottle/prices_round_1_day_-2.csv", "../round 1/round-1-island-data-bottle/prices_round_1_day_-1.csv", "../round 1/round-1-island-data-bottle/prices_round_1_day_0.csv", "../round 3/round-3-island-data-bottle/prices_round_3_day_0.csv", "../round 3/round-3-island-data-bottle/prices_round_3_day_1.csv", "../round 3/round-3-island-data-bottle/prices_round_3_day_2.csv",  "../round 4/round-4-island-data-bottle/prices_round_4_day_1.csv", "../round 4/round-4-island-data-bottle/prices_round_4_day_2.csv", "../round 4/round-4-island-data-bottle/prices_round_4_day_3.csv"]
processround5data(files)
processpricedata(pricefiles)

def showtrades(product):
    for name, snake in snakes.items():
        if product in snake.tradeHistoryBuys:
            x = [trade.timestamp/100 for trade in snake.tradeHistoryBuys[product]]
            y = [trade.price for trade in snake.tradeHistoryBuys[product]]
            x1 = [trade.timestamp/100 for trade in snake.tradeHistorySells[product]]
            y1 = [trade.price for trade in snake.tradeHistorySells[product]]
            plt.plot(x,y, label = "buys")
            plt.plot(x1,y1, label = "sells")
            plt.title(name+ " " + product + " Graph")
            plt.legend()
            plt.show()
            plt.clf()

def showtradesRelativePrice(product):
    for name, snake in snakes.items():
        if product in snake.tradeHistoryBuys:
            x = [trade.timestamp/100 for trade in snake.tradeHistoryBuys[product]]
            y = [trade.price - Prices[product][trade.timestamp] for trade in snake.tradeHistoryBuys[product]]
            x1 = [trade.timestamp/100 for trade in snake.tradeHistorySells[product]]
            y1 = [trade.price - Prices[product][trade.timestamp] for trade in snake.tradeHistorySells[product]]
            plt.plot(x,y, label = "buys")
            plt.plot(x1,y1, label = "sells")
            plt.title(name+ " " + product + " Graph")
            plt.legend()
            plt.show()
            plt.clf()

def showbuyandselltimes(product):
    for name, snake in snakes.items():
        if product in snake.tradeHistoryBuys:
            print(name)
            buytradeTimes = [trade.timestamp for trade in snake.tradeHistoryBuys[product]]
            selltradeTimes = [trade.timestamp for trade in snake.tradeHistorySells[product]]
            # print(buytradeTimes)
            x = [a for a in range(0, 3000001, 100)]
            y = [1 if a in buytradeTimes else 0 for a in range(0,3000001, 100)]
            x1 = [a for a in range(0, 3000001, 100)]
            y1 = [1 if a in selltradeTimes else 0 for a in range(0, 3000001, 100)]
            plt.plot(x,y, label = "buys")
            plt.title(name+ " " + product + " Graph")
            plt.legend()
            plt.show()
            plt.clf()
            plt.plot(x1,y1, label = "sells")
            plt.title(name+ " " + product + " Graph")
            plt.legend()
            plt.show()
            plt.clf()


def showpricegraph(product):
    x = []
    y = []
    for time in Prices[product].keys():
        x.append(time)
        y.append(Prices[product][time])
    plt.plot(x,y)
    plt.title(product + " price graph")
    plt.show()
    plt.clf()

# for product in Prices:
#     showbuyandselltimes(product)
showbuyandselltimes("STARFRUIT")
# showtradesRelativePrice("rR")


# showtrades("AMETHYSTS")
# showtradesRelativePrice("STARFRUIT")

# FindTraders(files)
# lastbuyers = None
# for product, traders in Products.items():
#     lastbuyers = traders.buyers
#     if len(traders.buyers) != len(traders.sellers):
#         print(f"procuts have different buyer seller numbers")
    # print(f"For Product {traders.product}, {len(traders.sellers)} traders are {sorted(traders.buyers)}")
    # print(f"\"{traders.product}\":{sorted(traders.buyers)}", end=",")
