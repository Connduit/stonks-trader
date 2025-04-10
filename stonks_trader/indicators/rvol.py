"""
Relative Volume Indicator

Formula:
    RVOL = CurrentVolume/AverageVolume
    AverageVolume is the average volume over some period of time
"""

from indicators.indicator import Indicator

class RVOL(Indicator):
    def __init__(self, df):
        super().__init__(df)
        self.df = df

    #def __call__(self, *args, **kwds):
        #return super().__call__(*args, **kwds)

    def __call__(self):
        pass
