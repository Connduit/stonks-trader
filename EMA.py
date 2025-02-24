"""
Exponential Moving Average Indicator

Formula:
    Period == len(Asset_Prices)
"""

from Indicator import Indicator
import pandas as pd

"""
TODO: stuff needed to find ema
- window size to know how much history to look at
- period (number of days)
"""
class EMA(Indicator):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.df = df

    #def __call__(self, *args, **kwds):
        #return super().__call__(*args, **kwds)

    def __call__(self, length):
        self.df["200_DAY_EMA"] = self.df["close"].ewm(span=length, adjust=False).mean()
        # return self.df.tail(1)
        #return self.df



