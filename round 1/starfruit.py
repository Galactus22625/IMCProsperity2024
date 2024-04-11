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
                    tradeOrders[product], traderdata["STARFRUIT"] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.market_trades.get(product, []), state.timestamp, traderdata.get("STARFRUIT", []))

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

    def starFruitTrader(self, orderDepth, currentPosition, marketTrades, currentTime, oldtrades):
        #we can also try tracking previous price or try looking at previou trades
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        hedgelimit = 2
        spreadMultiplier = 1
        priceCushion = 2
        movingAverageTimeLimit = 20000
        orders: List[Order] = []

        starfruitTrades = oldtrades     #list of timestamp, price, quanitty for each trade
        for trade in marketTrades:
            if trade.timestamp == currentTime:
                starfruitTrades.append([trade.timestamp, trade.price, trade.quantity])
        recentTrades = [trade for trade in starfruitTrades if trade[0] > currentTime - movingAverageTimeLimit]
        starfruitTrades = recentTrades

        calculatedPrice = None
        if len(starfruitTrades) >= 2:
            x = [time for trade in starfruitTrades for time in [trade[0]]*trade[2]]
            y = [price for trade in starfruitTrades for price in [trade[1]]*trade[2]]
            slope, intercept = linear_regression(x, y)
            calculatedPrice = slope * currentTime + intercept
            differences = [price - (slope * time + intercept) for time, price in zip(x,y)]
            spread = stdev(differences) * spreadMultiplier


        if calculatedPrice != None:
            buyprice = round(calculatedPrice - spread)
            sellprice = round(calculatedPrice + spread)
            if currentPosition > hedgelimit: 
                orders.append(Order("STARFRUIT", sellprice, -currentPosition))
            elif currentPosition < -hedgelimit:
                orders.append(Order("STARFRUIT", buyprice, -currentPosition))
            else:
                orders.append(Order("STARFRUIT", buyprice, buyLimit))
                orders.append(Order("STARFRUIT", sellprice, -sellLimit))

        # if calculatedPrice != None:
        #     buyLimit, sellLimit = self.arbitrageOrders(orders, orderDepth, "STARFRUIT", calculatedPrice, priceCushion, buyLimit, sellLimit)

        return orders, starfruitTrades
