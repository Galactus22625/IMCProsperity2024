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
                    #tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))
                    pass

                case "STARFRUIT":
                    tradeOrders[product] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0))


        traderData = "Knowledge for the future" #delivered as TradeingState.traderdata
        return tradeOrders, 0, traderData
    
    def amethystsTrader(self, orderDepth, currentPosition):
        #logging.print(currentPosition)
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        neutralPrice = 10000
        orders: List[Order] = []

        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        for price, quantity in active_buy_orders:
            if price > neutralPrice:
                if quantity < sellLimit:
                    orders.append(Order("AMETHYSTS", price, -quantity))
                    sellLimit -= quantity
                else:
                    orders.append(Order("AMETHYSTS", price, -sellLimit))
                    break
            else:
                break

        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0])
        for price, quantity in active_sell_orders:
            if price < neutralPrice:
                if abs(quantity) <= buyLimit:
                    orders.append(Order("AMETHYSTS", price, -quantity))
                    buyLimit += quantity
                else:
                    orders.append(Order("AMETHYSTS", price, buyLimit))
                    break
            else:
                break
        return orders

    def starFruitTrader(self, orderDepth, currentPosition):
        #test for starfruit no neutral price
        #things to try: force the spread so we can alwasy trade, larger spread, some undercutting, more trades that dont just go to position limit
        #we can also try tracking previous price
        positionLimit = 20
        selfLimit = 10
        buyLimit = selfLimit - currentPosition
        sellLimit = selfLimit + currentPosition
        buyprice = None
        sellprice = None
        minimumSpread = 2
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
            #put around previous price?
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
            
        orders.append(Order("STARFRUIT", buyprice, buyLimit))
        orders.append(Order("STARFRUIT", sellprice, -sellLimit))

        # if currentPosition > 0: 
        #     orders.append(Order("STARFRUIT", sellprice, -currentPosition))
        # elif currentPosition < 0:
        #     orders.append(Order("STARFRUIT", buyprice, -currentPosition))
        # elif sellprice - buyprice > minimumSpread:
        #     orders.append(Order("STARFRUIT", buyprice, selfLimit))
        #     orders.append(Order("STARFRUIT", sellprice, -selfLimit))
        return orders
