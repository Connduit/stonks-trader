from datetime import datetime
import time

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, TimeFrame, StockLatestTradeRequest, StockLatestQuoteRequest, StockLatestBarRequest
from algorithms.algorithm import Algorithm
from indicators.engulfing_candle import engulfingCandle
from indicators.ema import EMA
from indicators.rsi import RSI

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
    - TAKE PROFIT to a 2:1 ratio - for every dollar ur willing to risk, u profit 2 dollars
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
    # TODO: this will not get data from the current day... might have to use api.get_latest_bars(symbol)
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
        rq = StockLatestBarRequest(symbol_or_symbols=self.symbol)
        temp = self.data_client.get_stock_latest_bar(rq)
        print(temp)
        #self.df.concat([self.df, temp], ignore_index=True)
        #self.data_client.get_bar

    # update market data (this might be specific for our case where we're doing intraday trading...)
    # TODO: add start_time and end_time as params
    # TODO: this function needs to be running concurrently?
    def updateMarketData(self, end_time = datetime.now().date()):
        from datetime import timedelta
        #start_time = end_time - timedelta(days=1)
        # TODO: have start and end times only be during active trading hours
        start_time = datetime(2025, 2, 21)
        while True:
            #end_time = datetime.now().date()
            end_time = datetime.now()
            request_params = StockBarsRequest(
                symbol_or_symbols=self.symbol,
                timeframe=TimeFrame.Minute,
                start=start_time,
                end=end_time
            )
            minute_bars = self.data_client.get_stock_bars(request_params=request_params)
            latest_bar = minute_bars[self.symbol][-1]
            self.bars[self.symbol].append(latest_bar)
            self.df = self.bars.df.tz_convert("America/New_York", level=1) # TODO: check if we are in normal trading hours... might have to do this check somewhere else
            #time.sleep(60)
            time.sleep(5)
            break

    # TODO: maybe watchlist is just made up of all stocks that meet 50% of the buy conditions? in addition to the most popular and active stocks of the day and just good reputable stocks
    def generateWatchlist(self):
        pass

    def buyConditions(self):
        # TODO: might actuall have to call getMarketData or updateMarketData from here
        # getCurrentEma or SMA... then check stuff against it
        # getRSI... then check stuff
        # engulfingCandle("Bullish")
        ema_length = 200
        rsi_length = 14
        ema = EMA(self.df)
        ema(ema_length)
        #print(ema.df.tail(1)['close'].values)
        #print(ema.df.tail(1)['close'].iloc[-1])
        #print(ema.df.tail(1)['close'].tail())
        print(f"ema = {ema.df.tail(1)['200_DAY_EMA'].tail(1)}") # TODO: not sure if 2nd tail is needed or if i should just do .iloc[-1]
        #ema_value = ema.df.tail(1)['200_DAY_EMA'].tail(1)
        # TODO: pretty sure iloc will return out of bounds if ema is empty
        ema_value = ema.df.tail(1)['200_DAY_EMA'].iloc[-1] # USE iloc cuz it returns numpy.float instead of pd.Series... however will this cause errors when ema.df is empty?


        rsi = RSI(self.df)
        rsi(rsi_length)
        #print({rsi(rsi_length).tail(1)}) TODO: could just do this instead because we're returning from RSI.__call__()
        #print(rsi.df.tail(1)['close'].values)
        #print(rsi.df.tail(1)['close'].iloc[-1])
        #print(f"rsi = {rsi.df.tail(1)['close'].tail()}")
        print(f"rsi = {rsi.df.tail(1)['14_DAY_RSI'].tail(1)}") # TODO: not sure if 2nd tail is needed or if i should just do .iloc[-1]
        #rsi_value = rsi.df.tail(1)['14_DAY_RSI'].tail(1)
        # TODO: pretty sure iloc will return out of bounds if rsi is empty
        rsi_value = rsi.df.tail(1)['14_DAY_RSI'].iloc[-1] # USE iloc cuz it returns numpy.float instead of pd.Series... however will this cause errors when rsi.df is empty?

        #print(rsi.df.tail(1)['14_DAY_RSI'])

        #trade_request_params = StockLatestTradeRequest(symbol_or_symbols=self.symbol)
        quote_request_params = StockLatestQuoteRequest(symbol_or_symbols=self.symbol)

        #latest_trade = self.data_client.get_stock_latest_trade(trade_request_params)
        latest_quote = self.data_client.get_stock_latest_quote(quote_request_params)
        #print(latest_trade[self.symbol].price)
        print(f"ask_price = {latest_quote[self.symbol].ask_price}")
        ask_price = latest_quote[self.symbol].ask_price
        #print(latest_quote[self.symbol].bid_price)

        # TODO: add engulfing candle check
        # TODO: maybe make this first if statement condition a function or SAP that can be changed if we want different conditions. this might allow us to not have to rewrite this if statement everytime we want to change the conditions
        if ask_price > ema_value and rsi_value > 50:
            print("BUY")
            return True
        else:
            print("DON'T BUY")
            return False



    def sellConditions(self):
        # check we that we have an active position
        # sell once we reach X profits or sell once stop loss is triggered

        # TODO: maybe also sell once we encounter a bearish engulfing candle? 
        # also, if we run into another bullish engulfing candle update our takeProfits and stopLoss marks
        pass

    def trade(self):
        # TODO: do checks to make sure stock we want to trade is valid, our account doesn't have restrictions, and we have enough money
        # also should determine how much of the stock we want to trade... do we want to use all of our buying power? this probs should be termined by what self.risk_tolerance is set to?
        # If we don't want to use all of our buying power just do: amount_to_trade = balance * 0.50 # this will use half of our balance as buying power

        # TODO: this is where we actually execute the trades and create orders
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

        # TODO: 60 seconds maybe because that's how long it takes a candle to form?
        #time.sleep(variable_time) for this alg we should probs sleep for maybe 0.5-1 second? do tests to see how changing variable_time affects accuracy
