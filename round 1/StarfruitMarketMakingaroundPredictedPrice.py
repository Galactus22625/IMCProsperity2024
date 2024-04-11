from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle
#import math

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send
        tradeOrders = {}
        if state.traderData == "":
            traderdata = {}
        else:
            traderdata = jsonpickle.decode(state.traderData)

        for product in state.order_depths:
            match product:
                #case "AMETHYSTS":
                #    tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))

                case "STARFRUIT":
                    tradeOrders[product], traderdata["STARFRUIT"] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.market_trades.get(product, []), state.timestamp, traderdata.get("STARFRUIT", []))

        traderDataJson = jsonpickle.encode(traderdata) #string(starfruitprice) #delivered as TradeingState.traderdata
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
        Spread = 4
        movingAverageTimeLimit = 10000
        orders: List[Order] = []
        print(oldtrades)
        starfruitTrades = oldtrades     #list of timestamp, price, quanitty for each trade
        for trade in marketTrades:
            if trade.timestamp == currentTime:
                starfruitTrades.append([trade.timestamp, trade.price, trade.quantity])
        recentTrades = [trade for trade in starfruitTrades if trade[0] > currentTime - movingAverageTimeLimit]
        starfruitTrades = recentTrades

        print(starfruitTrades)
        # calculatedPrice = None
        # totalquantity = 0
        # totalpricequantity = 0
        # if starfruitTrades:
        #     for trade in starfruitTrades:
        #         totalquantity += trade[2]
        #         totalpricequantity += trade[1] * trade[2]
        #     calculatedPrice = totalpricequantity/totalquantity

        # if calculatedPrice != None:
        #     buyprice = round(calculatedPrice - Spread)
        #     sellprice = round(calculatedPrice + Spread)
        #     orders.append(Order("STARFRUIT", buyprice, buyLimit))
        #     orders.append(Order("STARFRUIT", sellprice, -sellLimit))

        # if calculatedPrice != None:
        #     buyLimit, sellLimit = self.arbitrageOrders(orders, "STARFRUIT", calculatedPrice, priceCushion, active_buy_orders, active_sell_orders, buyLimit, sellLimit)

        return orders, starfruitTrades
