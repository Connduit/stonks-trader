from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, TimeFrame
from Algorithm import Algorithm
from EngulfingCandle import engulfingCandle

"""
TODO: Need to do research on how scalping works

Super Conservative Scalping Strategy:
    - ONLY take positions when the chart is in an up trend and sell after small gains
        - This should result in higher accuracy but smaller/slower growth
        - Start by using 200 day ema to determine trend of the stock (can always fine tune this by using a combination of other indicators)
            - should also consider the volume... (when using certain days to calculate the ema, if those days have a volume way below the average maybe don't apply them to ema? for example: QBTS)
            - rsi DIVERGENCE? ONLY enter trade when rsi is above 50%
            - bullish DIVERGENCE is a bonus
            - momentum candles? (bullish engulfing candle... good indicator for a start of an uptrend). only enter after the engulfing candle closes
    - STOP LOSS = 2 times the length of the entry candle
    - TAKE PROFIT to a 2:1 ratio
"""
class ScalperAlgorithm(Algorithm):
    def __init__(self, api_key, api_secret, paper=True):
        super().__init__(api_key, api_secret, paper)
        # self.risk_tolerance = HIGH, LOW, MED ??? 
        # TODO: do we want to store different conditions as boolean memeber vars?
        self.symbol = "AAPL" # TODO: hard coded value right now for testing purposes
        #self.symbols = ["AAPL"] # list of stocks ? basically a watchlist of potential stocks we want this alg to run on. maybe we have alg run currently on multiple stocks

        #self.bars # DataFrame of market data... not sure if python makes us declare vars here 
        #self.df # DataFrame of market data... not sure if python makes us declare vars here 


    # get market data required for alg to work 
    #def getMarketData(self, start_time, end_time, timeframe):
    def getMarketData(self, start_time, end_time=datetime.now().date()):
        request_params = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            #timeframe=TimeFrame.Minute,
            timeframe=TimeFrame.Day,
            start=start_time,
            end=end_time
        )

        self.bars = self.data_client.get_stock_bars(request_params)
        self.df = self.bars.df.tz_convert("America/New_York", level=1)

    # update market data (this might be specific for our case where we're doing intraday trading...)
    def updateMarketData(self):
        pass

    # TODO: maybe watchlist is just made up of all stocks that meet 50% of the buy conditions? in addition to the most popular and active stocks of the day and just good reputable stocks
    def generateWatchlist(self):
        pass

    def buyConditions(self):
        # TODO: might actuall have to call getMarketData or updateMarketData from here
        # getCurrentEma or SMA... then check stuff against it
        # getRSI... then check stuff
        # engulfingCandle("Bullish")
        pass

    def sellConditions(self):
        # check we that we have an active position
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
