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

#processround2data("round-3-island-data-bottle/prices_round_3_day_2.csv",basketprices, strawberryprices, chocolateprices, roseprices)

# processround2data("round-3-island-data-bottle/prices_round_3_day_0.csv")

# processround2data("round-3-island-data-bottle/prices_round_3_day_1.csv")

# basketchange = [basketprices[x] - basketprices[x-1] for x in range(1, len(basketprices))]
# roseschange = [roseprices[x] - roseprices[x-1] for x in range(1, len(roseprices))]
# strawberrychange = [6*(strawberryprices[x] - strawberryprices[x-1]) for x in range(1, len(strawberryprices))]
# chocolatechange = [chocolateprices[x] - chocolateprices[x-1] for x in range(1, len(chocolateprices))]

#difference = [basketprices[x] - 6*strawberryprices[x] - 4*chocolateprices[x] - roseprices[x] for x in range(1000)]
def estimatePNL(differences, mean, arbitragelimit):
    state = "NONE"
    totalPNL = 0
    profit = 0
    for diff in differences:
        offset = diff 
        if offset > arbitragelimit:
            if state == "LONG":
                # profit -= basket*58 * 2
                totalPNL += 2*(arbitragelimit)*58
            state = "SHORT"
        if offset < -arbitragelimit:
            if state == "SHORT":
                totalPNL += 2*(arbitragelimit)*58 
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
    baskets = basketprices+basketprices2+basketprices3
    strawberry = strawberryprices+strawberryprices2+strawberryprices3
    chocolate = chocolateprices+chocolateprices2+chocolateprices3
    rose = roseprices+roseprices2+roseprices3
    basketmean = statistics.mean(baskets)
    strawberrymean = statistics.mean(strawberry)
    chocolatemean = statistics.mean(chocolate)
    rosemean = statistics.mean(rose)
    print(strawberrymean/(basketmean))
    print(chocolatemean/(basketmean ))
    print(rosemean/(basketmean))
    truestrawberry = [basketprices[x] * 0.05694959204415752 for x in range(len(basketprices))]     #0.05725730161380604
    truestrawberry2 = [basketprices2[x] * 0.05694959204415752 for x in range(len(basketprices))]     #0.05725730161380604
    truestrawberry3 = [basketprices3[x] * 0.05694959204415752 for x in range(len(basketprices))]     #0.05725730161380604
    
    truechocolate = [(basketprices[x] - 380) * 0.11254773547564821 for x in range(len(basketprices))]        #0.11254773547564821
    truechocolate2 = [(basketprices2[x] - 380) * 0.11254773547564821 for x in range(len(basketprices))]        #0.11254773547564821
    truechocolate3 = [(basketprices3[x] - 380) * 0.11254773547564821 for x in range(len(basketprices))]        #0.11254773547564821
    truerose = [(basketprices[x] - 380) * 0.206272493194264 for x in range(len(basketprices))]       #0.206272493194264
    truerose2 = [(basketprices2[x] - 380) * 0.206272493194264 for x in range(len(basketprices))]       #0.206272493194264
    truerose3 = [(basketprices3[x] - 380) * 0.206272493194264 for x in range(len(basketprices))]       #0.206272493194264
    # difference = [round(rose[x] - truerose[x]) for x in range(len(strawberry))]
    # print(difference)
    # print(min(difference))
    # print(max(difference))
    difference = [strawberryprices[x] - truestrawberry[x] for x in range(len(strawberryprices))]    # print(max(difference))
    difference2 = [strawberryprices2[x] - truestrawberry2[x] for x in range(len(strawberryprices))]    # print(max(difference))
    difference3 = [strawberryprices3[x] - truestrawberry3[x] for x in range(len(strawberryprices))]
    maxarb = 0
    pnl = 0


    basketdif = [basketprices[x] - 6*strawberryprices[x] - 4*chocolateprices[x] - roseprices[x] for x in range(len(basketprices))]

    # maxmid = 0
# for mid in range(330, 440):
    portion = 0.206272493194264
    for arb in range(0, 200, 2):
        newpnl = estimatePNL(difference, portion, arb)
        newpnl += estimatePNL(difference2, portion, arb)
        newpnl += estimatePNL(difference3, portion, arb)
        if newpnl > pnl:
            pnl = newpnl
            maxarb = arb
    print(maxarb)
    tiltedtowers = difference+difference2 + difference3
    x = [a for a in range(len(tiltedtowers))]
    y= [tiltedtowers[a] for a in range(len(tiltedtowers))]
    plt.plot(x, y)
    plt.show()
    print(pnl)
    return
printBestCombo("round-3-island-data-bottle/prices_round_3_day_2.csv", "round-3-island-data-bottle/prices_round_3_day_0.csv", "round-3-island-data-bottle/prices_round_3_day_1.csv")
# x = [a for a in range(1000)]
# y= [basketprices[a] for a in range(1000)]
# plt.plot(x, y)
# plt.show()