from datetime import datetime
import time

import talib as ta
import numpy as np
import pandas as pd
import pandas_ta as pdta

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, TimeFrame, StockLatestTradeRequest, StockLatestQuoteRequest, StockLatestBarRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.requests import MarketOrderRequest, TakeProfitRequest, StopLossRequest
from Algorithm import Algorithm
from EngulfingCandle import engulfingCandle
from EMA import EMA
from RSI import RSI

"""
TODO: There should be a general class (maybe just a data frame?) that gets updated based
upon what these algs request / whatever data they need

"""
class SuperTrendAlgorithm(Algorithm):
    def __init__(self, api_key, api_secret, paper=True):
        super().__init__(api_key, api_secret, paper)
        # self.risk_tolerance = HIGH, LOW, MED ??? 
        # TODO: do we want to store different conditions as boolean memeber vars?
        self.symbol = "AAPL" # TODO: hard coded value right now for testing purposes
        #self.symbols = ["AAPL"] # list of stocks ? basically a watchlist of potential stocks we want this alg to run on. maybe we have alg run currently on multiple stocks

        #self.bars # DataFrame of market data... not sure if python makes us declare vars here 
        #self.df # DataFrame of market data... not sure if python makes us declare vars here 


    # get market data required for alg to work 
    #def getMarketData(self, start_time, end_time, timeframe):
    # TODO: this will not get data from the current day... might have to use api.get_latest_bars(symbol)
    def getMarketData(self, start_time, end_time=datetime.now().date()):
        print(start_time)
        print(end_time)
        request_params = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            #timeframe=TimeFrame.Minute,
            timeframe=TimeFrame.Day,
            start=start_time,
            end=end_time
        )

        self.bars = self.data_client.get_stock_bars(request_params)
        self.df = self.bars.df.tz_convert("America/New_York", level=1)
        data = {
            'time': [bar[1] for bar in self.df.index],
            'open': [bar for bar in self.df.open],
            'high': [bar for bar in self.df.high],
            'low': [bar for bar in self.df.low],
            'close': [bar for bar in self.df.close],
            'volume': [bar for bar in self.df.volume],
        }
        self.df = pd.DataFrame(data)
        self.df['time'] = pd.to_datetime(self.df['time'])
        self.df.set_index('time', inplace=True) # sort by time


    def buyConditions(self):
        ATR_period = 10
        #source = (high + low) / 2
        self.df["HL2"] = (self.df["high"] + self.df["low"])/2
        ATR_MULTIPLIER = 3
        # This should return max(high - low, abs(high - close[1]), abs(low - close[1])) where close[1] is the previous candle's close
        # TODO: use atr_period as part of key
        self.df['10_DAY_ATR']= ta.ATR(self.df['high'], self.df['low'], self.df['close'], ATR_period)

        # up
        self.df["Upper_ATR"] = self.df["HL2"] - self.df["10_DAY_ATR"] * ATR_MULTIPLIER
        # dn
        self.df["Lower_ATR"] = self.df["HL2"] + self.df["10_DAY_ATR"] * ATR_MULTIPLIER


        up1 = self.df["Upper_ATR"].fillna(method="bfill")
        dn1 = self.df["Lower_ATR"].fillna(method="bfill")

        # up
        #self.df["Upper_ATR"] = 
        # dn
        #self.df["Lower_ATR"] = 

        self.df['up'] = np.where(self.df['close'].shift(1) > up1, np.maximum(self.df['Upper_ATR'], up1), self.df['Upper_ATR'])
        self.df['dn'] = np.where(self.df['close'].shift(1) < dn1, np.minimum(self.df['Lower_ATR'], dn1), self.df['Lower_ATR'])

        super_trend_df = pdta.supertrend(self.df["high"], self.df["low"], self.df["close"], length=10, multiplier=3)
        print(super_trend_df)

        #self.df['up'] = np.where(self.df['close'].shift(1) > self.df['up1'], np.maximum(self.df['Upper_ATR'], self.df['up1']), self.df['Upper_ATR'])
        #self.df['dn'] = np.where(self.df['close'].shift(1) < self.df['dn1'], np.minimum(self.df['Lower_ATR'], self.df['dn1']), self.df['Lower_ATR'])

        #self.df["New_Upper_ATR"] = value_if_true if cond else value_if_false
        #close1 = self.df["close"].shift(1)

        # Previous values (up1, dn1) handling (shifting values by 1 period)
        #self.df['up1'] = self.df['Upper_ATR'].shift(1)
        #self.df['dn1'] = self.df['Lower_ATR'].shift(1)

        # Reassign the value based on close comparison as per Pine Script logic


        #self.df['up'] = np.where(self.df['close'].shift(1) > self.df['up1'], np.maximum(self.df['Upper_ATR'], self.df['up1']), self.df['Upper_ATR'])

        # condition ? value_if_true : value_if_false
        # value_if_true if cond else value_if_false
        #self.df["trend"] = 1 if (self.df["trend"] == -1 and self.df['close'] > self.df['dn1']) else -1 if (self.df['trend'] == 1 and self.df['close'] < self.df['up1']) else self.df['trend']

        quote_request_params = StockLatestQuoteRequest(symbol_or_symbols=self.symbol)

        #latest_trade = self.data_client.get_stock_latest_trade(trade_request_params)
        latest_quote = self.data_client.get_stock_latest_quote(quote_request_params)
        #print(latest_trade[self.symbol].price)
        print(f"ask_price = {latest_quote[self.symbol].ask_price}")
        ask_price = latest_quote[self.symbol].ask_price
        #print(latest_quote[self.symbol].bid_price)

        #print(f"ema = {ema.df.tail(1)['200_DAY_EMA'].tail(1)}") # TODO: not sure if 2nd tail is needed or if i should just do .iloc[-1]
        print(super_trend_df["SUPERTl_10_3.0"].iloc[-1])
        # TODO: maybe check if ask_price hasn't gone up too much higher from SUPERTl
        # BUT this just sanitiy checks that we're in an upward trend... i think we still need this tho cuz if ask is below that means its gone against the trend we expected
        if ask_price > super_trend_df["SUPERTl_10_3.0"].iloc[-1]:
            try:
                # TODO: check if i funds, check if order is already requested from previous run... do this by comparing prices and supertrend
                # TODO: alpacapy doesn't support trading on weekends even with extended_hours = true.
                #       solution is to set time_in_force = TimeInForce.OPG  which ensures order is executed at market open
                order_request_params = MarketOrderRequest(
                                        symbol=self.symbol,
                                        qty=100,
                                        side=OrderSide.BUY,
                                        #time_in_force=TimeInForce.DAY,
                                        time_in_force=TimeInForce.OPG,
                                        take_profit=TakeProfitRequest(limit_price=self.df["Lower_ATR"].iloc[-1]),
                                        stop_loss=StopLossRequest(stop_price=self.df["Lower_ATR"].iloc[-1]),
                                        extended_hours=True
                                        )
                order = self.trading_client.submit_order(order_data=order_request_params)
                print(f'buy order: {order} has been placed')
            except Exception as e:
                print(f"Error placing order: {e}")

        # if super_trend_df value is nan, we will not enter if block
        if ask_price < super_trend_df["SUPERTs_10_3.0"].iloc[-1]:
            print("short")

        """
        up_cond = close1 > up1
        dn_cond = close1 < dn1
        self.df["up_cond"] = close1 > up1
        self.df["dn_cond"] = close1 < up1

        #self.df["New_Upper_ATR"] = max(self.df["Upper_ATR"], up1) if close1 > up1 else self.df["Upper_ATR"]
        #self.df["New_Down_ATR"] = min(self.df["Lower_ATR"], dn1) if close1 < dn1 else self.df["Down_ATR"]
        self.df["New_Upper_ATR"] = max(self.df["Upper_ATR"], up1) if self.df["up_cond"] else self.df["Upper_ATR"]
        self.df["New_Down_ATR"] = min(self.df["Lower_ATR"], dn1) if self.df["dn_cond"] else self.df["Down_ATR"]
        """


        print(self.df)



    def sellConditions(self):
        # check we that we have an active position
        # sell once we reach X profits or sell once stop loss is triggered

        # TODO: maybe also sell once we encounter a bearish engulfing candle? 
        # also, if we run into another bullish engulfing candle update our takeProfits and stopLoss marks
        pass

    def trade(self):
        # TODO: do checks to make sure stock we want to trade is valid, our account doesn't have restrictions, and we have enough money
        # also should determine how much of the stock we want to trade... do we want to use all of our buying power? this probs should be termined by what self.risk_tolerance is set to?
        # If we don't want to use all of our buying power just do: amount_to_trade = balance * 0.50 # this will use half of our balance as buying power

        # TODO: this is where we actually execute the trades and create orders
        pass

    def run(self):
        # create watchlist of stocks that meet or have a potential to meet our criteria and we want to trade 
        # watchlist can be populated from a scanner we choose (TODO: scanner code will have to be written)
        while True:
            # RUN ALG
            try:
                if self.buyConditions() == True:
                    self.trade() # THIS should probs should return a bool if trade was success or not... but do we care to check what it returns or do we need to do anything with that information?
                elif self.sellConditions() == True: # TODO: make sure to come back here and check if we should use elif vs. if
                    self.trade()

            except Exception as e:
                # handle exception?
                pass

        # TODO: 60 seconds maybe because that's how long it takes a candle to form?
        #time.sleep(variable_time) for this alg we should probs sleep for maybe 0.5-1 second? do tests to see how changing variable_time affects accuracy
