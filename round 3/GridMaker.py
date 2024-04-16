BaseMoney = 7500
Multiplier = [[24, 70, 41, 21,60], [47, 82, 87, 80, 35], [73, 89, 100, 90, 17], [77, 83, 85, 79, 55], [12, 27, 52, 15, 30]]
Hunters = [[2,4,3,2,4], [3,5,5,5,3], [4,5,8,7,2], [5,5,5,5,4], [2,3,4,2,3]]

rowNames = ["G", "H", "I", "J", "K"]
columnNames = ["26", "27", "28", "29", "30"]

BaseList = []

print("sensitivity")
for row in range(5):
    for column in range(5):
        print(f"{(10- Hunters[row][column]): .0f}", end = ", ")
    print("", end = "\n")
    
print("money with no percent")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/Hunters[row][column]: .0f}", end = ", ")
        BaseList.append((rowNames[row] + columnNames[column], BaseMoney * Multiplier[row][column]/Hunters[row][column]))

    print("", end = "\n")
BaseList.sort(key = lambda x: x[1], reverse=True)
for thing in BaseList:
    print(thing)

print("money with aveage percent, 1% each")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+1): .0f}", end = ", ")
    print("", end = "\n")

print("money with aveage percent, 2.5% each")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+2.5): .0f}", end = ", ")
    print("", end = "\n")

print("money with aveage percent, 4% each")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+4): .0f}", end = ", ")
    print("", end = "\n")

print("money with aveage percent, 8% each")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+8): .0f}", end = ", ")
    print("", end = "\n")

print("money with aveage percent, 10% each")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+10): .0f}", end = ", ")
    print("", end = "\n")

print("money with max percent everyone uses all expeditions")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+33): .0f}", end = ", ")
    print("", end = "\n")

print("money with max percent everyone uses one expedition")
for row in range(5):
    for column in range(5):
        print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+100): .0f}", end = ", ")
    print("", end = "\n")

