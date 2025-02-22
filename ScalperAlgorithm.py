from Algorithm import Algorithm
from EngulfingCandle import engulfingCandle

"""
TODO: Need to do research on how scalping works

Super Conservative Scalping Strategy:
    - ONLY take positions when the chart is in an up trend and sell after small gains
        - This should result in higher accuracy but smaller/slower growth
        - Start by using 200 day ema to determine trend of the stock (can always fine tune this by using a combination of other indicators)
            - rsi DIVERGENCE? ONLY enter trade when rsi is above 50%
            - bullish DIVERGENCE is a bonus
            - momentum candles? (bullish engulfing candle... good indicator for a start of an uptrend). only enter after the engulfing candle closes
    - STOP LOSS = 2 times the length of the entry candle
    - TAKE PROFIT to a 2:1 ratio
"""
class ScalperAlgorithm(Algorithm):
    def __init__(self):
        super().__init__()
        # self.risk_tolerance = HIGH, LOW, MED ??? 
        # TODO: do we want to store different conditions as boolean memeber vars?


    def buyConditions(self):
        pass

    def sellConditions(self):
        pass

    def trade(self):
        # TODO: do checks to make sure stock we want to trade is valid, our account doesn't have restrictions, and we have enough money
        # also should determine how much of the stock we want to trade... do we want to use all of our buying power? this probs should be termined by what self.risk_tolerance is set to?
        pass

    def run(self):
        # create watchlist of stocks that meet or have a potential to meet our criteria and we want to trade 
        # watchlist can be populated from a scanner we choose (TODO: scanner code will have to be written)
        while True:
            # RUN ALG
            try:
                if self.buyConditions() == True:
                    self.trade() # THIS should probs should return a bool if trade was success or not... but do we care to check what it returns or do we need to do anything with that information?
                elif self.sellConditions() == True: # TODO: make sure to come back here and check if we should use elif vs. if
                    self.trade()

            except Exception as e:
                # handle exception?
                pass

        #time.sleep(variable_time) for this alg we should probs sleep for maybe 0.5-1 second? do tests to see how changing variable_time affects accuracy