import csv
import statistics

#4 percetn decrease every 10 minutes below 7 hours per day of sunlight
#humidity good between 60-80 percent, falls 2 percent every 5 percent change in humidity

#trading for 12 hours per day, 720 min per day, 1000000 time stamps, 10000 ticks per day, .072 ticks per minute
#.72 ticks is 10 minutes, 1 tick is 7.2*4 percent decreas is 2.88 percent decresae
#assume price up = quantity down
orchidPrice = []
transportFees = []
exportTariff = []
importTariff = []
sunlight = []
sunlightproductiondecrease = []
instanateoussulightproductiondecrease = []
humidity = []
humidityproductiondecrease = []
sunlightdaydecrease = 100
def processround2data(filename):
    dayssunlight = []
    with open(filename, mode = "r") as file:
        csvfile = csv.reader(file)
        next(csvfile)
        for line in csvfile:
            data = line[0].split(";")
            orchidPrice.append(float(data[1]))
            transportFees.append(float(data[2]))
            exportTariff.append(float(data[3]))
            importTariff.append(float(data[4]))
            sunlight.append(float(data[5]))
            dayssunlight.append(float(data[5]))
            humidity.append(float(data[6]))
    currentproduction = 100
    for sun in dayssunlight:
        if sun < 2500:
            currentproduction = currentproduction * (1-.000288)
        sunlightproductiondecrease.append(currentproduction)
    print(f"sunlight decrase for day: {currentproduction}")

#processround2data("round 2/round-2-island-data-bottle/prices_round_2_day_-1.csv")

#processround2data("round 2/round-2-island-data-bottle/prices_round_2_day_0.csv")

processround2data("round 2/round-2-island-data-bottle/prices_round_2_day_1.csv")

changeinorchid = [orchidPrice[x] - orchidPrice[x-1] for x in range(1, len(orchidPrice))]
currentproduction = 100
for humid in humidity:
    productiondecrease = 100
    if humid< 60:
        productiondecrease = 100*(.98**((60 - humid) /5 ))
    if humid > 80:
        productiondecrease = 100*(.98**((humid-80) /5 ))
    humidityproductiondecrease.append(productiondecrease)

humidity.pop()
sunlight.pop()
sunlightproductiondecrease.pop()
humidityproductiondecrease.pop()
##instanateoussulightproductiondecrease.pop()
print(statistics.correlation(changeinorchid, sunlight))
print(statistics.correlation(changeinorchid, sunlightproductiondecrease))
#print(statistics.correlation(changeinorchid, instanateoussulightproductiondecreaseß))
print(statistics.correlation(changeinorchid, humidity))
print(statistics.correlation(changeinorchid, humidityproductiondecrease))

# print(statistics.correlation(orchidPrice, transportFees))
# print(statistics.correlation(orchidPrice, exportTariff))
# print(statistics.correlation(orchidPrice, importTariff))
# print(statistics.correlation(orchidPrice, sunlight))
# print(statistics.correlation(orchidPrice, sunlightproductiondecrease))
# print(statistics.correlation(orchidPrice, humidity))
# print(statistics.correlation(orchidPrice, humidityproductiondecrease))
# laterprices = orchidPrice[80::]
# delayhumidity = humidity[0:-80]
# delayhumditiyproductiondecrease = humidityproductiondecrease[0:-80]
# print(len(laterprices))
# print(len(delayhumidity))
# print(statistics.correlation(laterprices, delayhumidity))
# print(statistics.correlation(laterprices, delayhumditiyproductiondecrease))


