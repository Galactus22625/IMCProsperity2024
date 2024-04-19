class Fish:
    def __init__ (self, reserve):
        self.reserveprice = reserve
        self.quantity = reserve - 900

    def profitgenerated(self, bid1, bid2, bid2average):
        profit = 0
        if bid1 > self.reserveprice:
            profit += (1000 - bid1) * self.quantity
        elif bid2 == 1000:
            profit += 0
        elif bid2> self.reserveprice and bid2<=bid2average:
            profit += (1000 - bid2) * self.quantity * (1000-bid2average)/(1000-bid2)
        elif bid2> self.reserveprice and bid2>bid2average:
            profit += (1000 - bid2) * self.quantity
        return profit
    
def calculateprofit(allfishes, bid1, bid2, bid2average):
    profit = 0
    for fish in allfishes:
        profit+= fish.profitgenerated(bid1, bid2, bid2average)
    return profit
    
allfishes = []
for reserveprice in range(900,1001):
    allfishes.append(Fish(reserveprice))

def printstatsforbid2average(bid2average):
    maxprofit = 0
    bids = [None, None]
    failprofit = 0
    for bid1 in range(900,1001):
        for bid2 in range(bid1, 1001):
            profit = calculateprofit(allfishes, bid1, bid2, bid2average)
            if profit > maxprofit:
                maxprofit = profit
                bids = [bid1, bid2]
    print(f"maxprofit for bid 2 average of {bid2average} is {maxprofit} with bids {bids}")
    return

def profitfor1(bid1):
    maxprofit = 0
    bids = [None, None]
    profit = calculateprofit(allfishes, bid1, 1000, 1000)

    # print(f"maxprofit for a failed second bid at bid 1: {bid1} is {profit}")
    return profit

def maxprofitifbid1(bid1):
    maxprofit = 0
    bids = [None, None]
    for bid2 in range(bid1, 1001):
        profit = calculateprofit(allfishes, bid1, bid2, 0)
        if profit > maxprofit:
            maxprofit = profit
            bids = [bid1, bid2]
    print(f"for bid 1 of {bid1} , bid of {bids} gives maxprofit of {maxprofit}")
    return

def maxprofitifbid1withbid2constraint(bid1, bid2min):
    maxprofit = 0
    bids = [None, None]
    for bid2 in range(bid1, 1001):
        profit = calculateprofit(allfishes, bid1, bid2, bid2min)
        if profit > maxprofit:
            maxprofit = profit
            bids = [bid1, bid2]
    #print(f"for bid 1 of {bid1} with bid2 min of {bid2min}, bid of {bids} gives maxprofit of {maxprofit}")
    return maxprofit, bids[1]

# for bid2average in range(950, 1000):
#     printstatsforbid2average(bid2average)
def maxprofitgivenbid2(bid2):
    maxprofit = 0
    bids = [None, None]
    for bid1 in range(900, bid2):
        profit = calculateprofit(allfishes, bid1, bid2, bid2)
        if profit > maxprofit:
            maxprofit = profit
            bids = [bid1, bid2]
    #print(f"for bid 1 of {bid1} with bid2 min of {bid2min}, bid of {bids} gives maxprofit of {maxprofit}")
    return maxprofit, bids[0]

maxbid1forbid2 = {}
print("\n")
for bid1 in range(950,978):
    guaranteed = profitfor1(bid1)
    # maxprofitifbid1(bid1)
    totalprofit, bid2 = maxprofitifbid1withbid2constraint(bid1, 981)
    print(f"Bids are {(bid1, bid2)} with guaranteed profit {guaranteed} and totalprofit {totalprofit}")

print("\n")
for bid2 in range(977,1001):
    profit, bid1 = maxprofitgivenbid2(bid2)
    maxbid1forbid2[bid2] = bid1
    print(f"if bid2 is {bid2}then best profit is with bid1 of {bid1} giving profit of {profit}")

# print("\n") about 2000 per
# for bid2 in range(977, 991):
#     for bid2average in range(bid2, bid2+8):
#         bid1 = maxbid1forbid2[bid2]
#         print(f"volatility of optimal at bid2 {bid2}, bids are {bid1, bid2}, for bid2average {bid2average} profit of {calculateprofit(allfishes, bid1, bid2, bid2average)}")