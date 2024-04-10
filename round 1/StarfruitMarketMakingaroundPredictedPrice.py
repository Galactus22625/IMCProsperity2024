from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import numpy as np
#import math

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send
        tradeOrders = {}
        starfruitTradesString = state.traderData
        for product in state.order_depths:
            match product:
                #case "AMETHYSTS":
                #    tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))

                case "STARFRUIT":
                    tradeOrders[product], starfruitTradesString = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.market_trades.get(product, []), state.timestamp, starfruitTradesString)

        traderData = starfruitTradesString #string(starfruitprice) #delivered as TradeingState.traderdata
        return tradeOrders, 0, traderData
    
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

    def stringtoTradeList(self, tradesstring):
        #time, price, quanitity
        if tradesstring == "":
            return []
        tradeList = []
        separatedtrades = tradesstring.split(",")
        for trade in separatedtrades:
            tradeList.append([int(x) for x in trade.split("-")])
        return tradeList

    def tradeListtoString(self, tradeslist):
        #time, price, quanittiy
        if not tradeslist:
            return ""
        finalstring = ""
        stringtrades = []
        for trade in tradeslist:
            stringtrades.append("-".join(str(x) for x in trade))
        finalstring = ",".join(stringtrades)
        return finalstring

    def starFruitTrader(self, orderDepth, currentPosition, marketTrades, currentTime, oldtradesstring):
        #we can also try tracking previous price or try looking at previou trades
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        Spread = 4
        movingAverageTimeLimit = 10000
        orders: List[Order] = []

        print(oldtradesstring)
        starfruitTrades = self.stringtoTradeList(oldtradesstring)
        starfruitTrades = []
        for trade in marketTrades:
            starfruitTrades.append([trade.timestamp, int(trade.price), trade.quantity])

        print(starfruitTrades)
        # calculatedPrice = None
        # totalquantity = 0
        # totalpricequantity = 0
        # if starfruitTrades:
        #     for trade in starfruitTrades:
        #         totalquantity += trade[2]
        #         totalpricequantity += trade[1] * trade[2]
        #     calculatedPrice = totalpricequantity/totalquantity

        starfruitTradesString = self.tradeListtoString(starfruitTrades)

        # if calculatedPrice != None:
        #     buyprice = round(calculatedPrice - Spread)
        #     sellprice = round(calculatedPrice + Spread)
        #     orders.append(Order("STARFRUIT", buyprice, buyLimit))
        #     orders.append(Order("STARFRUIT", sellprice, -sellLimit))

        # if calculatedPrice != None:
        #     buyLimit, sellLimit = self.arbitrageOrders(orders, "STARFRUIT", calculatedPrice, priceCushion, active_buy_orders, active_sell_orders, buyLimit, sellLimit)

        return orders, starfruitTradesString
