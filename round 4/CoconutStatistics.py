import csv
import statistics
import numpy
import matplotlib.pyplot as plt

coconutprices = []
coconutcouponprices = []
#mdoel coconut coupon (635) = coconut (10000) - difference (9365)
ccoupdif = 9365
#predicted coconut = coupon + difference (9365)
#true relation coconutprice - 10000 = (predictedcoconut - 10000) * 1.8


def processround2data(files):
    for filename in files:
        with open(filename, mode = "r") as file:
            csvfile = csv.reader(file)
            next(csvfile)
            for data in csvfile:
                line = data[0].split(";")
                if line[2] == "COCONUT":
                    coconutprices.append(float(line[15]))
                elif line[2] == "COCONUT_COUPON":
                    coconutcouponprices.append(float(line[15]))

files = ["round-4-island-data-bottle/prices_round_4_day_1.csv", "round-4-island-data-bottle/prices_round_4_day_2.csv", "round-4-island-data-bottle/prices_round_4_day_3.csv"]

processround2data(files)
coconutaverage = statistics.mean(coconutprices)
coconutcouponaverage = statistics.mean(coconutcouponprices)
print(f"coconut averge: {coconutaverage}, coconut coupon average: {coconutcouponaverage}")
print(f"averge difference {coconutaverage-coconutcouponaverage}")

x= [a for a in range(len(coconutprices))]
predictedcoupon = [coconutprices[a] - ccoupdif for a in range(len(coconutprices))]
predictedcoconut = [coconutcouponprices[a] + ccoupdif for a in range(len(coconutprices))]

bestmultiplier = 0
bestspread = 1000000
for scaledmultiplier in range(18341700,18341800, 1):
    multiplier = scaledmultiplier/10000000
    coconutfrom1000 = [coconutprices[a] - 10000 for a in range(len(coconutprices))]
    cocpredictfrom1000timessome = [(predictedcoconut[a] - 10000)*multiplier for a in range(len(coconutprices))]
    modeldif = [coconutfrom1000[a] - cocpredictfrom1000timessome[a] for a in range(len(coconutprices))]
    absmodeldif = [abs(num) for num in modeldif]
    modeldifavg = statistics.mean(absmodeldif)
    if modeldifavg < bestspread:
        bestmultiplier = multiplier
        bestspread = modeldifavg
    print(modeldifavg)
print(bestmultiplier)
# plt.plot(x, cocpredictfrom1000timessome)
# plt.plot(x, coconutfrom1000)
coconutfrom1000 = [coconutprices[a] - 10000 for a in range(len(coconutprices))]
cocpredictfrom1000timessome = [(predictedcoconut[a] - 10000)*bestmultiplier for a in range(len(coconutprices))]
modeldif = [coconutfrom1000[a] - cocpredictfrom1000timessome[a] for a in range(len(coconutprices))]


#predicted coconut = coupon + difference (9365)
#true relation coconutprice - 10000 = (predictedcoconut - 10000) * 1.8
plt.plot(x[20000::], modeldif[20000::])
# plt.plot(x, coconutfrom1000)
# plt.plot(x, cocpredictfrom1000timessome)

plt.show()