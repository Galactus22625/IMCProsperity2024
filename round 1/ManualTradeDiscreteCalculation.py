class Fish:
    def __init__ (self, reserve):
        self.reserveprice = reserve
        self.quantity = reserve - 900

    def profitgenerated(self, bid1, bid2):
        profit = 0
        if bid1 > self.reserveprice:
            profit += (1000 - bid1) * self.quantity
        elif bid2> self.reserveprice:
            profit += (1000 - bid2) * self.quantity
        return profit
    
def calculateprofit(allfishes, bid1, bid2):
    profit = 0
    for fish in allfishes:
        profit+= fish.profitgenerated(bid1, bid2)
    return profit
    
allfishes = []
for reserveprice in range(900,1001):
    allfishes.append(Fish(reserveprice))

maxprofit = 0
bids = [None, None]
for bid1 in range(900,1001):
    for bid2 in range(bid1, 1001):
        profit = calculateprofit(allfishes, bid1, bid2)
        if profit > maxprofit:
            maxprofit = profit
            bids = [bid1, bid2]

print(maxprofit)
print(bids)

