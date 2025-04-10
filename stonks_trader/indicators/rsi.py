"""
Relative Strength Index Indicator

Formula:
    https://www.investopedia.com/terms/r/rsi.asp
"""

from indicators.indicator import Indicator

class RSI(Indicator):
    def __init__(self, df):
        super().__init__(df)
        self.df = df

    #def __call__(self, *args, **kwds):
        #return super().__call__(*args, **kwds)

    def __call__(self, length):
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        self.df[f'{length}_DAY_RSI'] = rsi
        return rsi
