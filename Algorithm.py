"""
Abstract base class from which all trading algorithms will be derived from
"""

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient

# from abc import ABC # not sure if this is actually needed for an abstract base class

# class Algorithm(ABC):
class Algorithm:
    # TODO: not sure if base_url is needed?
    def __init__(self, api_key, api_secret, paper=True): # TODO: maybe have trading_client initialized somewhere else and just passed in as a paramter to this class (i think this is the better way of doing it)
        self.api_key = api_key
        self.api_secret = api_secret
        self.paper = paper
        #self.base_url=base_url # TODO: not sure if this is needed for anyting?
        self.trading_client = TradingClient(self.api_key, self.api_secret, paper=self.paper)
        self.data_client = StockHistoricalDataClient(self.api_key, self.api_secret)

    # TODO: figure out what params are needed
    # params: time interval which alg should run?
    # def run():
