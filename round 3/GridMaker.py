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
    
def printGridPayouts(percentChoose):
    for row in range(5):
        for column in range(5):
            print(f"{BaseMoney * Multiplier[row][column]/(Hunters[row][column]+percentChoose): .0f}", end = ", ")
        print("", end = "\n")
    return
    
print("money with no percent")
printGridPayouts(0)

for row in range(5):
    for column in range(5):
        BaseList.append((rowNames[row] + columnNames[column], BaseMoney * Multiplier[row][column]/Hunters[row][column]))
BaseList.sort(key = lambda x: x[1], reverse=True)
for thing in BaseList:
    print(thing)

print("money with aveage percent, 1% each")
printGridPayouts(1)

print("money with aveage percent, 2.5% each")
printGridPayouts(2.5)

print("money with aveage percent, 4% each")
printGridPayouts(4)

print("money with aveage percent, 8% each")
printGridPayouts(8)

print("money with aveage percent, 10% each")
printGridPayouts(10)

print("money with max percent everyone uses all expeditions")
printGridPayouts(33)

print("money with max percent everyone uses one expedition")
printGridPayouts(100)

