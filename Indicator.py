"""
Abstract class for indicators/studies
"""

# from abc import ABC # not sure if this is actually needed for an abstract base class

# class Indicator(ABC):
class Indicator:
    def __init__(self, df):
        self.df = df