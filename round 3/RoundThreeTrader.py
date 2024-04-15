from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from jsonpickle import encode, decode
from statistics import linear_regression, stdev, mean
from math import ceil, floor
#import math

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send
        tradeOrders = {}
        if state.traderData == "":
            traderdata = {}
        else:
            traderdata = decode(state.traderData)

        conversions = 0     #for testing when orchids is 
        for product in state.order_depths:
            match product:
                # case "AMETHYSTS":
                #    tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))

                # case "STARFRUIT":
                #    tradeOrders[product], traderdata["STARFRUIT"] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.timestamp, traderdata.get("STARFRUIT", {}))

                # case "ORCHIDS":
                #     tradeOrders[product], conversions, traderdata["ORCHIDS"] = self.orchidTrader(state.observations.conversionObservations[product], state.position.get(product,0), traderdata.get("ORCHIDS", {"traded": [0], "markup": 1.5}))

                case "GIFT_BASKET":
                    pass

                case "ROSES":
                    pass

        traderDataJson = encode(traderdata) #string(starfruitprice) #delivered as TradeingState.traderdata
        return tradeOrders, conversions, traderDataJson
    
    def basketTrader(self):
        state = "TOBASKET" # "FROMBASKET"
        #notice that buy volume is alwasy sell volume for all products

    def toBasketTrades(self):
        pass

    def fromBasketTrades(self):
        pass

    def orchidTrader(self, observations, position, orchidData):
        orders: List[Order] = []
        positionLimit = 100
        sellLimit = positionLimit     #position converted immediately
        memory = 5
        shiftspeed = .1
        markupMin = 0
        markup = orchidData["markup"]
        trades = orchidData["traded"]
        trades.append(-position)
        if len(trades) > memory:
            trades.pop(0)
        if mean(trades) >= 80:
            markup += shiftspeed
        elif mean(trades) <= 50:
            markup -= shiftspeed
        markup = max(markupMin, markup)

        print(f"Orchid Markup: {markup}, Orchid position: {position}")
        
        southsell = observations.askPrice
        costtobuyfromsouth = southsell + observations.importTariff + observations.transportFees

        orders.append(Order("ORCHIDS", ceil(costtobuyfromsouth + markup), -sellLimit))
        convert = -position

        orchiddata = {"traded": trades, "markup": markup}
        return orders, convert, orchiddata

    def arbitrageOrders(self, orders, orderDepth, product, truePrice, priceCushion, buyLimit, sellLimit):
        #to create arbitrage orders when we know a price buy looking at order book, need sorted orderbook
        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0], reverse = False)
        
        for price, quantity in active_buy_orders:
            if price > truePrice + priceCushion:
                if quantity < sellLimit:
                    orders.append(Order(product, price, -quantity))
                    sellLimit -= quantity
                else:
                    orders.append(Order(product, price, -sellLimit))
                    sellLimit = 0
                    break
            else:
                break

        for price, quantity in active_sell_orders:
            if price < truePrice - priceCushion:
                if abs(quantity) <= buyLimit:
                    orders.append(Order(product, price, -quantity))
                    buyLimit += quantity
                else:
                    orders.append(Order(product, price, buyLimit))
                    buyLimit = 0
                    break
            else:
                break
        return buyLimit, sellLimit
    
    def amethystsTrader(self, orderDepth, currentPosition):
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        neutralPrice = 10000
        orders: List[Order] = []

        buyLimit, sellLimit = self.arbitrageOrders(orders, orderDepth, "AMETHYSTS", neutralPrice, 0, buyLimit, sellLimit)

        #market making
        orders.append(Order("AMETHYSTS", neutralPrice - 3, buyLimit))
        orders.append(Order("AMETHYSTS", neutralPrice + 3, -sellLimit))
        return orders

    def starFruitTrader(self, orderDepth, currentPosition, currentTime, oldstarfruitData):
        #we can also try tracking previous price or try looking at previou trades
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        nextTime = currentTime + 100
        dataTimeLimit = 1500
        orders: List[Order] = []
        undercut = .5

        if oldstarfruitData == {}:
            starfruitData = {}
            starfruitData["buyorders"] = []     #time, price
            starfruitData["sellorders"] = []
        else:
            starfruitData = oldstarfruitData

        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        buyorders = [order for order in starfruitData["buyorders"] if order[0] > currentTime - dataTimeLimit]
        if active_buy_orders:
            buyorders.append((currentTime, active_buy_orders[0][0]))

        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0], reverse = False)
        sellorders = [order for order in starfruitData["sellorders"] if order[0] > currentTime - dataTimeLimit]
        if active_sell_orders:
            sellorders.append((currentTime, active_sell_orders[0][0]))

        predictedBuyOrder = None
        predictedSellOrder = None
        if len(buyorders) >= 2:
            x = [x[0] for x in buyorders]
            y = [x[1] for x in buyorders]
            slope, intercept = linear_regression(x, y)
            predictedBuyOrder = slope * nextTime + intercept
        if len(sellorders) >= 5:
            x = [x[0] for x in sellorders]
            y = [x[1] for x in sellorders]
            slope, intercept = linear_regression(x, y)
            predictedSellOrder = slope * nextTime + intercept
        

        if predictedBuyOrder != None and predictedSellOrder != None:
            buyprice = round(predictedBuyOrder + undercut)
            sellprice = round(predictedSellOrder - undercut)
            orders.append(Order("STARFRUIT", buyprice, buyLimit))
            orders.append(Order("STARFRUIT", sellprice, -sellLimit))

        starfruitData["sellorders"] = sellorders
        starfruitData["buyorders"] = buyorders
        return orders, starfruitData
