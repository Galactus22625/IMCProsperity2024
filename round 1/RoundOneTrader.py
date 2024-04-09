from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send

        tradeOrders = {}
        for product in state.order_depths:
            match product:
                case "AMETHYSTS":
                    tradeOrders[product] = self.amethystsTrader(state.order_depths[product])

        traderData = "Knowledge for the future" #delivered as TradeingState.traderdata
        return tradeOrders, 0, traderData
    
    def amethystsTrader(orderDepth, currentPosition):
        positionLimit = 20
        neutralPrice = 10000
        active_buy_orders = orderDepth.buy_orders
        active_sell_orders = orderDepth.sell_orders
        #return list of orders, buy and sell orders

    def starFruitTrader():
        #look at observations and analyze maybe
        pass
