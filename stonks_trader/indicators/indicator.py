"""
Abstract class for indicators/studies
TODO: maybe instead of making this an abstract base class for indicators/studies,
      just have the individual indicators/studies be functions of the Indicator class. 
      maybe for more complex indicators/studies we can switch back to having Indicator
      be an abstract base class?
"""

# from abc import ABC # not sure if this is actually needed for an abstract base class

# class Indicator(ABC):
class Indicator:
    def __init__(self, df):
        self.df = df
