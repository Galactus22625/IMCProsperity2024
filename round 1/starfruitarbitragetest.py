from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from jsonpickle import encode, decode
from statistics import linear_regression, stdev
from numpy import polyfit as np_polyfit
#import math

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send
        tradeOrders = {}
        if state.traderData == "":
            traderdata = {}
        else:
            traderdata = decode(state.traderData)

        for product in state.order_depths:
            match product:
                #case "AMETHYSTS":
                #    tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))

                case "STARFRUIT":
                    tradeOrders[product], traderdata["STARFRUIT"] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.market_trades.get(product, []), state.timestamp, traderdata.get("STARFRUIT", {}))

        traderDataJson = encode(traderdata) #string(starfruitprice) #delivered as TradeingState.traderdata
        return tradeOrders, 0, traderDataJson
    
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

    def starFruitTrader(self, orderDepth, currentPosition, marketTrades, currentTime, oldstarfruitData):
        #we can also try tracking previous price or try looking at previou trades
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        nextTime = currentTime + 100
        dataTimeLimit = 1500
        priceCushion = 0
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
        if len(buyorders) >= 5:
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
            calculatedPrice = (buyprice + sellprice)/2

            buyLimit, sellLimit = self.arbitrageOrders(orders, orderDepth, "STARFRUIT", calculatedPrice, priceCushion, buyLimit, sellLimit)

            orders.append(Order("STARFRUIT", buyprice, buyLimit))
            orders.append(Order("STARFRUIT", sellprice, -sellLimit))

        starfruitData["sellorders"] = sellorders
        starfruitData["buyorders"] = buyorders
        return orders, starfruitData
