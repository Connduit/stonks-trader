from datetime import datetime
import time

import numpy as np
import pandas as pd

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, TimeFrame, StockLatestTradeRequest, StockLatestQuoteRequest, StockLatestBarRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.requests import MarketOrderRequest, TakeProfitRequest, StopLossRequest
from algorithms.src.algorithm import Algorithm

"""
TODO: There should be a general class (maybe just a data frame?) that gets updated based
upon what these algs request / whatever data they need

"""
class MajorityMovingAverages(Algorithm):
    def __init__(self, api_key, api_secret, paper=True):
        super().__init__(api_key, api_secret, paper)

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
        pass



    def sellConditions(self):
        pass

    def trade(self):
        pass

    def run(self):
        pass