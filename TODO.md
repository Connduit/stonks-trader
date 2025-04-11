# TODO

### ALG1 (MACD)

##### Logic

    func ALG1()
        macd_diff = getMACD(); // assuming that MACD lengths and other params are already set

        // bool position; // do we have an active position for the stock we're looking at 

        if position == true
            // wait till macd_diff is negative (confirmation of downtrend)
            // maybe also check if selling at this current price will give us profits?
            if macd_diff < 0
                sell();
                position = false;
            end
            // if macd_diff > 0 we keep holding onto our position
        else if position == false
            // check if macd_diff goes from negative to positive (sign of an uptrend)
            if macd_diff > 0 && prev_macd_diff < 0 // something like this?
                but();
                position = true;
            end
            // if macd_diff < 0 we don't buy
        end

        // TODO: can also add checks for other things like rsi, sma/ema, volume, and maybe vwap?
        // if rsi > 70% ... risky buy?
        // if rsi < 30% ... good potential buy?
        // if current price is below sma or ema, wait for it to break above the indicator before buying. Should also have a condition where it needs to be above indicator for X amount of time after breaking
        // idk about volume... need to research more (TODO)
        // idk about vwap... need to research more (TODO)
    end

### ALG2 (Scalper)

##### Logic


    TODO: Need to do research on how scalping works
    
    Super Conservative Scalping Strategy: https://www.youtube.com/watch?v=XBcMiYK7qYY
        - ONLY take positions when the chart is in an up trend and sell after small gains
            - This should result in higher accuracy but smaller/slower growth
            - Start by using 200 day ema to determine trend of the stock (can always fine tune this by using a combination of other indicators)
                - rsi DIVERGENCE? ONLY enter trade when rsi is above 50%
                - bullish DIVERGENCE is a bonus
                - momentum candles? (bullish engulfing candle... good indicator for a start of an uptrend). only enter after the engulfing candle closes
        - STOP LOSS = 2 times the length of the entry candle
        - TAKE PROFIT to a 2:1 ratio

### ALG3 (Bounds)

##### Logic

    Strategy: https://www.youtube.com/watch?v=ik0YD2soVj0
        - look at what price the stock is most commonly sold at and/or how long it stays at that price to identify support and resistance price points

### ALG4 (Weekly Trends)

##### Logic

    - If the friday high is not as high as the high on thursday, then the friday low will be visited on monday. 
        - Therefore, short the stock if it opens higher than friday's low on monday and take profits once it reaches that low
    - If the wednsday high is lower than monday's high, then the wednsday low will be visited on thursday
        - Therefore, short the stock if it opens higher than wednsday's low and take profits once it reaches that low

### ALG5 (Thane Brooker - extreme human high freq)

##### Logic
    
    https://www.youtube.com/watch?v=Wv7P0L8Ojnw
    - AS = First, Fast, Large sellers
    - AB = First, Fast, Large Buyers 
    - SS = Sell Stops triggered in the downward direction.
    - SB = Buy Stops triggered in the upward direction. 
    
    - The indicator filters the most important order flow and provides invaluable insight into why price is moving. 
    - Idea: profit from trapped traders understand which way consolidation is likely to break understand the safest and riskiest times and places to enter a trade 

### Scanner1

##### Strategy

    - Scan for stocks that have strong bullish candles in a 1min time frame (this probs works best and is most accureate for well known companies and non-meme garabage stocks)


### Testing

##### Logic

    - Use historical market data to test ALGS to help fine tune their performance 
