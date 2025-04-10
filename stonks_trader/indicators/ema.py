"""
Exponential Moving Average Indicator

Formula:

"""

from indicators.indicator import Indicator

# TODO: i really don't think these small indicators need to be their own class. we shouldn't have to store self.df either cuz we
# can just pass it as an arg. that way we save a lot of space espeically when stock history is large
class EMA(Indicator):
    def __init__(self, df):
        super().__init__(df)
        self.df = df

    #def __call__(self, *args, **kwds):
        #return super().__call__(*args, **kwds)

    def __call__(self, length):
        # TODO when adjust=False... data is calculated recursively
        self.df[f'{length}_DAY_EMA'] = self.df['close'].ewm(span=length, adjust=False).mean()
