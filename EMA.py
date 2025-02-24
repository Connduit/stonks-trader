"""
Exponential Moving Average Indicator

Formula:

"""

from Indicator import Indicator

class EMA(Indicator):
    def __init__(self, df):
        super().__init__(df)
        self.df = df

    #def __call__(self, *args, **kwds):
        #return super().__call__(*args, **kwds)

    def __call__(self):
        pass
