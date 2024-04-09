from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import logging

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send
        #logging.print(test)
        tradeOrders = {}
        for product in state.order_depths:
            match product:
                case "AMETHYSTS":
                    tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))

                case "STARFRUIT":
                    #tradeOrders[product] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0))
                    pass


        traderData = "Knowledge for the future" #delivered as TradeingState.traderdata
        return tradeOrders, 0, traderData
    
    def amethystsTrader(self, orderDepth, currentPosition):
        positionLimit = 20
        position = currentPosition
        buyLimit = positionLimit - position
        sellLimit = positionLimit + position
        neutralPrice = 10000
        orders: List[Order] = []

        active_sell_orders = [list(x) for x in orderDepth.sell_orders.items()] #if x[0] < neutralPrice]
        active_sell_orders.sort(key = lambda x: x[0], reverse = False)
        active_buy_orders = [list(x) for x in orderDepth.buy_orders.items()] #if x[0] > neutralPrice]
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        buys = 0
        sells = 0
        while True:
            if active_sell_orders and position < 20:
                buyLimit = positionLimit - position
                price = active_sell_orders[0][0]
                quantity = -active_sell_orders[0][1]
                if quantity <= buyLimit:
                    orders.append(Order("AMETHYSTS", price, quantity))
                    position += quantity
                    active_sell_orders.pop(0)
                    buys+= quantity
                else:
                    orders.append(Order("AMETHYSTS", price, buyLimit))
                    active_sell_orders[0][1] += buyLimit
                    position += buyLimit
                    buys += buyLimit
            if active_buy_orders and position > -20:
                sellLimit = positionLimit + position
                price = active_buy_orders[0][0]
                quantity = active_buy_orders[0][1]
                if quantity <= sellLimit:
                    orders.append(Order("AMETHYSTS", price, -quantity))
                    position -= quantity
                    active_buy_orders.pop(0)
                    sells += quantity
                else:
                    orders.append(Order("AMETHYSTS", price, -sellLimit))
                    active_buy_orders[0][1] -= sellLimit
                    position -= sellLimit
                    sells += sellLimit
            if (position == 20 and not active_buy_orders) or (position == -20 and not active_sell_orders) or (not active_sell_orders and not active_buy_orders):
                break


        # buyLimit = positionLimit - position
        # sellLimit = positionLimit + position
        # # #finish with market maker
        # orders.append(Order("AMETHYSTS", neutralPrice - 1, buyLimit))
        # orders.append(Order("AMETHYSTS", neutralPrice + 1, -sellLimit))
        print(f"buys = {buys}")
        print(f"sells = {sells}")
        return orders

    def starFruitTrader(self, orderDepth, currentPosition):
        #we can also try tracking previous price or try looking at previou trades
        positionLimit = 20
        hedgelimit = 10
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        buyprice = None
        sellprice = None
        minimumSpread = 4
        orders: List[Order] = []

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
            #if buy sell orders are empty, buy the spreadsheets this never happens
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

        if currentPosition > hedgelimit: 
            orders.append(Order("STARFRUIT", sellprice, -currentPosition))
        elif currentPosition < -hedgelimit:
            orders.append(Order("STARFRUIT", buyprice, -currentPosition))
        elif sellprice - buyprice > minimumSpread:
            orders.append(Order("STARFRUIT", buyprice, buyLimit))
            orders.append(Order("STARFRUIT", sellprice, -sellLimit))
        return orders
