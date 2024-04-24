def calculateyield(percent):
    fee = 90*(percent**2) * 8
    investment = 8*percent *750000 / 100

    for move in range(5,50, 5):
        yieldamount = (investment * move/100) - fee
        print(f"a move of {move} will yield {yieldamount}")


for percent in range(2,13):
    print(f"percent at {percent}")
    calculateyield(percent)