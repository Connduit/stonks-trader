"""
determines if candle is engulfing or not... not sure if needs to be a class or just a simple func.
at the moment, a class kind of seems overkill
"""

# TODO: figure out if param type should be BarSet or if it should have already been converted into a DataFrame
# def engulfingCandle(bar_set, direction):
# TODO: assume that this function is called from ScalperAlgorithm.updateMarketData() ?
def engulfingCandle(minute_bars, symbol, direction):  
    # TODO: we should really only be looking at the current candle and previous candle
    # we don't really need to be passing all the bar_set data

    latest_bars = minute_bars[symbol].tail(-2) # get 2 most recent bars (prev and current)
    current_bar = latest_bars[1]
    previous_bar = latest_bars[0]

    # TODO: double check that all the code in here runs so far

    """
    Bullish Engulfing Candle:

    if curr.close > prev.open and curr.open < prev.close and direction==Bullish:
        candle is bullish engulfing... return True

    Bearish Engulfing Candle:
    if curr.open > prev.close and curr.close < prev.open and direction == Bearish:
        candle is bearish engulfing... return True
    
    Non-Engulfing Candle:
    else:
        candle is neither bearish or bullish engulfing... return False
    """

    #TODO: we already get minute bars from ScalperAlgorithm.updateMarketData so maybe we can reuse that code here
    pass
