import csv
import statistics
import numpy
import matplotlib.pyplot as plt
#6 strawberry 4 chocolate 1 rose
basketprices = []
strawberryprices = []
chocolateprices = []
roseprices = []

def processround2data(filename, basketprices, strawberryprices, chocolateprices, roseprices):
    with open(filename, mode = "r") as file:
        csvfile = csv.reader(file)
        next(csvfile)
        for data in csvfile:
            line = data[0].split(";")
            if line[2] == "CHOCOLATE":
                chocolateprices.append(float(line[15]))
            elif line[2] == "STRAWBERRIES":
                strawberryprices.append(float(line[15]))
            elif line[2] == "ROSES":
                roseprices.append(float(line[15]))
            elif line[2] == "GIFT_BASKET":
                basketprices.append(float(line[15]))

processround2data("round-3-island-data-bottle/prices_round_3_day_2.csv",basketprices, strawberryprices, chocolateprices, roseprices)

# processround2data("round-3-island-data-bottle/prices_round_3_day_0.csv")

# processround2data("round-3-island-data-bottle/prices_round_3_day_1.csv")

# basketchange = [basketprices[x] - basketprices[x-1] for x in range(1, len(basketprices))]
# roseschange = [roseprices[x] - roseprices[x-1] for x in range(1, len(roseprices))]
# strawberrychange = [6*(strawberryprices[x] - strawberryprices[x-1]) for x in range(1, len(strawberryprices))]
# chocolatechange = [chocolateprices[x] - chocolateprices[x-1] for x in range(1, len(chocolateprices))]

difference = [basketprices[x] - 6*strawberryprices[x] - 4*chocolateprices[x] - roseprices[x] for x in range(1000)]
def estimatePNL(differences, mean, arbitragelimit):
    state = "NONE"
    totalPNL = 0
    profit = 0
    for diff in differences:
        offset = diff - mean
        if offset > arbitragelimit:
            if state == "LONG":
                # profit -= basket*58 * 2
                totalPNL += 2*(arbitragelimit-3)*58
            state = "SHORT"
        if offset < -arbitragelimit:
            if state == "SHORT":
                totalPNL += 2*(arbitragelimit-3)*58 
                # profit+= basket*58 * 2
            state = "LONG"
    # if state == "LONG":
    #     profit += basketprices[-1]*58*2
    # else:
    #     profit -= basketprices[-1]*58*2
    return totalPNL
# print(estimatePNL(difference, basketprices, 380, 53))
def printBestCombo(file1, file2, file3):
    basketprices = []
    strawberryprices = []
    chocolateprices = []
    roseprices = []
    basketprices2 = []
    strawberryprices2 = []
    chocolateprices2 = []
    roseprices2 = []
    basketprices3 = []
    strawberryprices3 = []
    chocolateprices3 = []
    roseprices3 = []
    processround2data(file1, basketprices, strawberryprices, chocolateprices, roseprices)
    processround2data(file2, basketprices2, strawberryprices2, chocolateprices2, roseprices2)
    processround2data(file3, basketprices3, strawberryprices3, chocolateprices3, roseprices3)
    difference = [basketprices[x] - 6*strawberryprices[x] - 4*chocolateprices[x] - roseprices[x] for x in range(len(basketprices))]
    difference2 = [basketprices2[x] - 6*strawberryprices2[x] - 4*chocolateprices2[x] - roseprices2[x] for x in range(len(basketprices2))]
    difference3 = [basketprices3[x] - 6*strawberryprices3[x] - 4*chocolateprices3[x] - roseprices3[x] for x in range(len(basketprices3))]
    maxarb = 0
    pnl = 0
    maxmid = 0
    for mid in range(330, 440):
        for arb in range(20, 150, 1):
            newpnl = estimatePNL(difference, mid, arb)
            newpnl += estimatePNL(difference2, mid, arb)
            newpnl += estimatePNL(difference3, mid, arb)
            if newpnl > pnl:
                maxmid = mid
                pnl = newpnl
                maxarb = arb
    print(maxarb)
    print(maxmid)
    print(pnl)
    return
printBestCombo("round-3-island-data-bottle/prices_round_3_day_2.csv", "round-3-island-data-bottle/prices_round_3_day_0.csv", "round-3-island-data-bottle/prices_round_3_day_1.csv")
# x = [a for a in range(1000)]
# y= [basketprices[a] for a in range(1000)]
# plt.plot(x, y)
# plt.show()