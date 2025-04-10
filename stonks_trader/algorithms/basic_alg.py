from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from algorithms.algorithm import Algorithm

class BasicAlgorithm(Algorithm):

    #def __init__(self, paper=True):
    def __init__(self, api_key, api_secret, paper=True):
        #super().__init__(paper=True)
        super().__init__(api_key, api_secret, paper)

    def buyMarket(self):
        market_order_request = MarketOrderRequest(
                            symbol="TSLA",
                            qty=1,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.GTC,
                            extended_hours=True
                            )
        
        market_order_response = self.trading_client.submit_order(market_order_request)
        # market_order_response.id gives us a status id 

    def sellMarket(self):
        market_order_request = MarketOrderRequest(
                            symbol="TSLA",
                            qty=1,
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.GTC,
                            extended_hours=True
                            )
        
        market_order_response = self.trading_client.submit_order(market_order_request)
        # market_order_response.id gives us a status id 

    def buyCondition(self):
        pass

    def sellCondition(self):
        pass

    def run(self):
        pass

if __name__ == "__main__":
    pass