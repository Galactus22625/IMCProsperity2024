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
        #logging.print(currentPosition)
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        neutralPrice = 10000
        orders: List[Order] = []


        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0], reverse = False)
        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        currentbuy = list(active_buy_orders.pop(0)) #price quantity
        currentsell = list(active_sell_orders.pop(0))  #price, quantity
        done = False
        while not done:
            currentsellprice = currentsell[0]
            currentsellquantity = currentsell[1]
            currentbuyprice = currentbuy[0]
            currentbuyquantity = currentbuy[1]
            numberoforders = len(orders)
            if currentsellprice < neutralPrice:
                if abs(currentsellquantity) <= buyLimit:
                    orders.append(Order("AMETHYSTS", currentsellprice, -currentsellquantity))
                    buyLimit += currentsellquantity
                    sellLimit -= currentsellquantity
                    try:
                        currentsell = list(active_sell_orders.pop(0))
                    except IndexError:
                        done = True
                else:
                    orders.append(Order("AMETHYSTS", currentsellprice, buyLimit))
                    buyLimit -= buyLimit
                    sellLimit += buyLimit
                    currentsell[1] -= buyLimit
            if currentbuyprice > neutralPrice:
                if currentbuyquantity <= sellLimit:
                    orders.append(Order("AMETHYSTS", currentbuyprice, -currentbuyquantity))
                    sellLimit -= currentbuyquantity
                    buyLimit += currentbuyquantity
                    try:
                        currentbuy = list(active_buy_orders.pop(0))
                    except IndexError:
                        done = True
                else:
                    orders.append(Order("AMETHYSTS", currentbuyprice, -sellLimit))
                    sellLimit -= sellLimit
                    buyLimit += sellLimit
                    currentbuy[1] -= sellLimit
            if len(orders) == numberoforders:
                done = True

        #finish with market maker
        orders.append(Order("AMETHYSTS", neutralPrice - 1, buyLimit))
        orders.append(Order("AMETHYSTS", neutralPrice + 1, -sellLimit))

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
