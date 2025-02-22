"""
determines if candle is engulfing or not... not sure if needs to be a class or just a simple func.
at the moment, a class kind of seems overkill
"""

# TODO: figure out if param type should be BarSet or if it should have already been converted into a DataFrame
def engulfingCandle(bar_set, direction):
    # TODO: we should really only be looking at the current candle and previous candle
    # we don't really need to be passing all the bar_set data

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
    pass