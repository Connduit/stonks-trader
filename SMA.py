"""
Simple Moving Average Indicator

Formula:
    SMA = Sum(Asset_Prices)/len(Asset_Prices)
    Period == len(Asset_Prices)
"""

from Indicator import Indicator

"""
TODO: stuff needed to find sma
- window size to know how much history to look at
- period (number of days)
"""
class SMA(Indicator):
    def __init__(self):
        super().__init__()

    #def __call__(self, *args, **kwds):
        #return super().__call__(*args, **kwds)

    def __call__(self):
        pass

