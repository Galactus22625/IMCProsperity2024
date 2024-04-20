from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
from jsonpickle import encode, decode
from statistics import linear_regression, stdev, mean
from math import ceil, floor
#import math

class Trader:

    def run(self, state: TradingState):
        #takes in a trading state, outputs list of orders to send
        tradeOrders = {}
        if state.traderData == "":
            traderdata = {}
        else:
            traderdata = decode(state.traderData)

        conversions = 0     #for testing when orchids is 
        for product in state.order_depths:
            match product:
                case "AMETHYSTS":
                   tradeOrders[product] = self.amethystsTrader(state.order_depths[product], state.position.get(product, 0))

                case "STARFRUIT":
                   tradeOrders[product], traderdata["STARFRUIT"] = self.starFruitTrader(state.order_depths[product], state.position.get(product, 0), state.timestamp, traderdata.get("STARFRUIT", {}))

                case "ORCHIDS":
                    tradeOrders[product], conversions, traderdata["ORCHIDS"] = self.orchidTrader(state.observations.conversionObservations[product], state.position.get(product,0), traderdata.get("ORCHIDS", {"traded": [0], "markup": 1.5}))

                case "GIFT_BASKET":
                    tradeOrders[product], tradeOrders["STRAWBERRIES"], tradeOrders["CHOCOLATE"], tradeOrders["ROSES"] = self.basketTrader(state.order_depths[product], state.order_depths["STRAWBERRIES"], state.order_depths["CHOCOLATE"], state.order_depths["ROSES"], state.position)

                case "COCONUT_COUPON":
                    tradeOrders[product], tradeOrders["COCONUT"] = self.coconutTrader(state.order_depths["COCONUT"], state.position.get("COCONUT", 0), state.order_depths[product], state.position.get(product, 0))

        traderDataJson = encode(traderdata) #string(starfruitprice) #delivered as TradeingState.traderdata
        return tradeOrders, conversions, traderDataJson
    #buy when break apart, return to 0 when together
    def coconutTrader(self, coconutOrderDepth, coconutPosition, coconutCouponOrderDepth, coconutCouponPosition):
        #trade coconut coupons, hedge with coconut
        coconutPositionLimit = 300
        couponPositonLimit = 600
        couponBuyLimit = couponPositonLimit - coconutCouponPosition
        couponSellLimit = couponPositonLimit + coconutCouponPosition
        coconutOrders = []
        coconutCouponOrders = []
        divergeLimit = 0

        if (not coconutOrderDepth.buy_orders or not coconutOrderDepth.sell_orders or not coconutCouponOrderDepth.buy_orders or not coconutCouponOrderDepth.sell_orders):
            return [], []
        coconutPrice = self.getMidPrice(coconutOrderDepth)
        coconutCouponPrice = self.getMidPrice(coconutCouponOrderDepth)

        #predicted coconut = coupon + difference (9365)
        #true relation coconutprice - 10000 = (predictedcoconut - 10000) * 1.8
        predictedCoconut = coconutCouponPrice + 9365
        trueRelationCoconut = coconutPrice - 10000
        trueRelationCoupon = (predictedCoconut - 10000) * 1.8341708

        if trueRelationCoconut > trueRelationCoupon + divergeLimit:
            coconutCouponOrders, couponBuyLimit, couponSellLimit = self.orderBookTrader("COCONUT_COUPON", coconutCouponOrderDepth, couponBuyLimit, couponSellLimit, "BUY")
        elif trueRelationCoupon + divergeLimit > trueRelationCoconut:
            coconutCouponOrders, couponBuyLimit, couponSellLimit = self.orderBookTrader("COCONUT_COUPON", coconutCouponOrderDepth, couponBuyLimit, couponSellLimit, "SELL")
        
        #marketmake at way above and way below? probably not needed since it is a shift back and forth strat

        averagecouponspercoconut = 1.5748031496
        coconutsneededtohedge = min(coconutPositionLimit, abs(coconutCouponPosition/averagecouponspercoconut))
        if coconutCouponPosition > 0:
            coconutsneededtohedge = coconutsneededtohedge * -1 
        # coconutOrders = self.hedgeTrader("COCONUT", coconutOrderDepth, coconutPosition, round(coconutsneededtohedge))
        print(f"coconut positoin {coconutPosition}, coupon positoin {coconutCouponPosition}")
        return coconutCouponOrders, coconutOrders
    
    def getMidPrice(self, orderDepth):
        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = True)
        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0], reverse = False)
        midprice = (active_buy_orders[0][0] + active_sell_orders[0][0])/2
        return midprice
    
    def orderBookTrader(self, product, orderDepth, buyLimit, sellLimit, buyorsell):
        orders = []
        buylimit = buyLimit
        selllimit = sellLimit
        if buyorsell == "BUY":
            active_sell_orders = list(orderDepth.sell_orders.items())
            active_sell_orders.sort(key = lambda x: x[0], reverse = False)
            for price, quantity in active_sell_orders:
                orders.append(Order(product, price, min(abs(quantity), buylimit)))
                buylimit -= min(abs(quantity), buylimit)
        if buyorsell == "SELL":
            active_buy_orders = list(orderDepth.buy_orders.items())
            active_buy_orders.sort(key = lambda x: x[0], reverse = True)
            for price, quantity in active_buy_orders:
                orders.append(Order(product, price, -min(abs(quantity), selllimit)))
                selllimit -= min(abs(quantity), selllimit)
        return orders, buylimit, selllimit
                

    def hedgeTrader(self, product, orderDepth, currentPosition, intendedPosition):
        tradeDif = intendedPosition - currentPosition
        orders = []
        active_buy_orders = list(orderDepth.buy_orders.items())
        active_buy_orders.sort(key = lambda x: x[0], reverse = False)
        active_sell_orders = list(orderDepth.sell_orders.items())
        active_sell_orders.sort(key = lambda x: x[0], reverse = True)
        if tradeDif > 0:
            orders.append(Order(product, active_sell_orders[0][0],tradeDif))
        elif tradeDif < 0:
            orders.append(Order(product, active_buy_orders[0][0], tradeDif))
        return orders
    
    def basketTrader(self, orderDepth, strawberryOrders, chocolateOrders, roseOrders, positions):
        currentPosition = positions.get("GIFT_BASKET", 0)
        positionLimit = 60
        orders: List[Order] = []
        strawberryorders: List[Order] = []
        chocolateorders: List[Order] = []
        roseorders: List[Order] = []
        basketMarkup = 380      #alculated ideal from all 3 datasets, using calculated mean diff
        arbitrageLimit = 40

        basketmidPrice = self.getMidPrice(orderDepth)
        strawberryPrice = self.getMidPrice(strawberryOrders)
        chocolatePrice = self.getMidPrice(chocolateOrders)
        rosePrice = self.getMidPrice(roseOrders)
        predictedBasketPrice = 6*strawberryPrice +  4*chocolatePrice + rosePrice + basketMarkup

        difference = basketmidPrice-predictedBasketPrice

        if difference > arbitrageLimit:
            orders = self.hedgeTrader("GIFT_BASKET", orderDepth, currentPosition, -positionLimit)
        elif difference < -arbitrageLimit:
            orders = self.hedgeTrader("GIFT_BASKET", orderDepth, currentPosition, positionLimit)

        #Can only predict forwards, can't go from basket to components?
        print(f"Difference of Basket from base price prediction {difference}, GiftBasketPosition {currentPosition}")
        return orders, strawberryorders, chocolateorders, roseorders

    def orchidTrader(self, observations, position, orchidData):
        orders: List[Order] = []
        positionLimit = 100
        sellLimit = positionLimit     #position converted immediately
        memory = 5
        shiftspeed = .1
        markupMin = 0
        markup = orchidData["markup"]
        trades = orchidData["traded"]
        trades.append(-position)
        if len(trades) > memory:
            trades.pop(0)
        if mean(trades) >= 80:
            markup += shiftspeed
        elif mean(trades) <= 50:
            markup -= shiftspeed
        markup = max(markupMin, markup)

        print(f"Orchid Markup: {markup}, Orchid position: {position}")
        
        southsell = observations.askPrice
        costtobuyfromsouth = southsell + observations.importTariff + observations.transportFees

        orders.append(Order("ORCHIDS", ceil(costtobuyfromsouth + markup), -sellLimit))
        convert = -position

        orchiddata = {"traded": trades, "markup": markup}
        return orders, convert, orchiddata

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

    def starFruitTrader(self, orderDepth, currentPosition, currentTime, oldstarfruitData):
        #we can also try tracking previous price or try looking at previou trades
        positionLimit = 20
        buyLimit = positionLimit - currentPosition
        sellLimit = positionLimit + currentPosition
        nextTime = currentTime + 100
        dataTimeLimit = 1500
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
        if len(buyorders) >= 2:
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
            orders.append(Order("STARFRUIT", buyprice, buyLimit))
            orders.append(Order("STARFRUIT", sellprice, -sellLimit))

        starfruitData["sellorders"] = sellorders
        starfruitData["buyorders"] = buyorders
        return orders, starfruitData
