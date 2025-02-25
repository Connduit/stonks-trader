"""
Simple Moving Average Indicator

Formula:
    SMA = Sum(Asset_Prices)/len(Asset_Prices)
    Period == len(Asset_Prices)
"""

from Indicator import Indicator
import pandas as pd

"""
TODO: stuff needed to find sma
- window size to know how much history to look at
- period (number of days)
"""
class SMA(Indicator):
    def __init__(self, df):
        super().__init__(df)
        self.df = df

    #def __call__(self, *args, **kwds):
        #return super().__call__(*args, **kwds)

    def __call__(self, length):
        self.df[f'{length}_DAY_SMA'] = self.df['close'].rolling(window=length).mean()
        # TODO: return instead of storing?

