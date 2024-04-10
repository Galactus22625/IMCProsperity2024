from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
#import math

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send
        tradeOrders = {}
        for product in state.order_depths:
            match product:
                #case "AMETHYSTS":
                    #tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))

                case "STARFRUIT":
                    tradeOrders[product] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.market_trades.get(product, []))

        traderData = "Knowledge for the future" #delivered as TradeingState.traderdata
        return tradeOrders, 0, traderData
    
    def arbitrageOrders(self, orders, product, truePrice, priceCushion, active_buy_orders, active_sell_orders, buyLimit, sellLimit):
        #to create arbitrage orders when we know a price buy looking at order book, need sorted orderbook
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

        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0], reverse = False)
        buyLimit, sellLimit = self.arbitrageOrders(orders, "AMETHYSTS", neutralPrice, 0, active_buy_orders, active_sell_orders, buyLimit, sellLimit)

        #market making
        orders.append(Order("AMETHYSTS", neutralPrice - 3, buyLimit))
        orders.append(Order("AMETHYSTS", neutralPrice + 3, -sellLimit))
        return orders

    def starFruitTrader(self, orderDepth, currentPosition, marketTrades):
        #we can also try tracking previous price or try looking at previou trades
        positionLimit = 20
        hedgelimit = 10
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        buyprice = None
        sellprice = None
        minimumSpread = 4
        orders: List[Order] = []

        priceCushion = 5
        tradedPriceQuantity = 0
        tradedQuantity = 0
        calculatedPrice = None
        for trade in marketTrades:
            tradedPriceQuantity += trade.price * trade.quantity
            tradedQuantity += trade.quantity
        if tradedQuantity != 0:
            calculatedPrice = tradedPriceQuantity/tradedQuantity
        #probably use previous prices in current price estimate


        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0])

        if active_buy_orders:
            buyprice = active_buy_orders[0][0] + 1
        if active_sell_orders:
            sellprice = active_sell_orders[0][0] - 1

        if buyprice == None and sellprice == None:
            return orders
            #if buy sell orders are empty, by the spreadsheets this never happens
        elif buyprice == None:
            buyprice = sellprice - minimumSpread
        elif sellprice == None:
            sellprice = buyprice + minimumSpread
        else:
            buyweight = 0
            sellweight = 0
            while sellprice - buyprice < minimumSpread:
                buyweight += orderDepth.buy_orders.get(buyprice - 1, 0)
                sellweight -= orderDepth.sell_orders.get(sellprice + 1, 0)
                if buyweight > sellweight:
                    buyprice -= 1
                else:
                    sellprice += 1

        # if currentPosition > hedgelimit: 
        #     orders.append(Order("STARFRUIT", sellprice, -currentPosition))
        #     return orders
        # elif currentPosition < -hedgelimit:
        #     orders.append(Order("STARFRUIT", buyprice, -currentPosition))
        #     return orders

        # if calculatedPrice != None:
        #     buyLimit, sellLimit = self.arbitrageOrders(orders, "STARFRUIT", calculatedPrice, priceCushion, active_buy_orders, active_sell_orders, buyLimit, sellLimit)

        position = 20-buyLimit
        if position > hedgelimit: 
            orders.append(Order("STARFRUIT", sellprice, -min(abs(position), sellLimit)))
            return orders
        elif position < -hedgelimit:
            orders.append(Order("STARFRUIT", buyprice, min(abs(position),buyLimit)))
            return orders
        elif sellprice - buyprice > minimumSpread:
            orders.append(Order("STARFRUIT", buyprice, buyLimit))
            orders.append(Order("STARFRUIT", sellprice, -sellLimit))
        return orders
