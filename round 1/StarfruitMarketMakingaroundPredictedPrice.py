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
                    tradeOrders[product], starfruitprice = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.market_trades.get(product, []))

        traderData = "Knowledge for the future" #string(starfruitprice) #delivered as TradeingState.traderdata
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

        priceCushion = 4
        tradedPriceQuantity = 0
        tradedQuantity = 0
        calculatedPrice = None
        for trade in marketTrades:
            tradedPriceQuantity += trade.price * trade.quantity
            tradedQuantity += trade.quantity
        if tradedQuantity != 0:
            calculatedPrice = tradedPriceQuantity/tradedQuantity
        #probably use previous prices in current price estimate

        if calculatedPrice != None:
            buyprice = round(calculatedPrice - 4)
            sellprice = round(calculatedPrice + 4)
            position = 20-buyLimit
            orders.append(Order("STARFRUIT", buyprice, buyLimit))
            orders.append(Order("STARFRUIT", sellprice, -sellLimit))
            # if position > hedgelimit: 
            #     orders.append(Order("STARFRUIT", sellprice, -min(abs(position), sellLimit)))
            #     return orders
            # elif position < -hedgelimit:
            #     orders.append(Order("STARFRUIT", buyprice, min(abs(position),buyLimit)))
            #     return orders
            # else:
            #     orders.append(Order("STARFRUIT", buyprice, buyLimit))
            #     orders.append(Order("STARFRUIT", sellprice, -sellLimit))
                              

        # if calculatedPrice != None:
        #     buyLimit, sellLimit = self.arbitrageOrders(orders, "STARFRUIT", calculatedPrice, priceCushion, active_buy_orders, active_sell_orders, buyLimit, sellLimit)

        # position = 20-buyLimit
        # if position > hedgelimit: 
        #     orders.append(Order("STARFRUIT", sellprice, -min(abs(position), sellLimit)))
        #     return orders
        # elif position < -hedgelimit:
        #     orders.append(Order("STARFRUIT", buyprice, min(abs(position),buyLimit)))
        #     return orders
        # elif sellprice - buyprice > minimumSpread:
        #     orders.append(Order("STARFRUIT", buyprice, buyLimit))
        #     orders.append(Order("STARFRUIT", sellprice, -sellLimit))
        return orders, calculatedPrice
