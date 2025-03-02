from EngulfingCandle import engulfingCandle
from ScalperAlgorithm import ScalperAlgorithm
from SuperTrendAlgorithm import SuperTrendAlgorithm
import config
from EMA import EMA
from SMA import SMA
#import datetime
from datetime import timedelta
from datetime import datetime
import pandas as pd
from alpaca.trading.requests import GetCalendarRequest


api_key = config.api_key
api_secret = config.api_secret

scalper_algorithm = ScalperAlgorithm(api_key, api_secret)
supertrend_algorithm = SuperTrendAlgorithm(api_key, api_secret)
day = timedelta(days=365)
end_time = datetime.now().date()
start_time = end_time - day

#day = pd.Timedelta(days=1)
#end_time = pd.to_datetime("today")
#start_time = end_time - day
#start_time_pd = pd.to_datetime("2024-02-21").tz_localize("America/New_York")
#start_time_pd = pd.to_datetime("2024-02-21") # TODO: this matches the date time syntax more i think

#print(start_time)
#print(end_time)

#calendar_request = GetCalendarRequest(start=start_time, end=end_time)
# TODO: use these dates to test if we can get data from most recent trade day even if it isn't the most recent calendar day
# this is needed for Mondays that need to use the data from friday... but start_date obviously won't be accurate if we do Monday - Day cuz that would be sunday not friday
#calendar_request = GetCalendarRequest(start='2025-02-16', end='2025-02-17') 

# TODO: i guess all of this get calendar shit isn't needed cuz it wont actually get the most recent trade day without doing extra manipulation
#calendar_request = GetCalendarRequest(start='2025-02-13', end='2025-02-14') 
#print(scalper_algorithm.trading_client.get_calendar(calendar_request))

# TODO: this is only testing on historical data... eventually we want to actively update the market data as we continue throughout the current day
#start_time = datetime(2025, 2, 20) # TODO: hard coded for quick testing purposes... change later
#start_time = datetime(2024, 2, 21) # TODO: hard coded for quick testing purposes... change later
#end_time = datetime(2025, 2, 21) # TODO: hard coded for quick testing purposes... change later



#scalper_algorithm.getMarketData(start_time)
#scalper_algorithm.updateMarketData()
supertrend_algorithm.getMarketData(start_time)
#supertrend_algorithm.updateMarketData()
#print(scalper_algorithm.bars)
import btalib
#print(scalper_algorithm.bars.df)

#print(scalper_algorithm.df['close'])

# TODO: this data shouldn't be parsed just for scalper_algorithm cuz it can be reused in other algs?
"""
data = {
    'time': [bar[1] for bar in scalper_algorithm.df.index],
    'open': [bar for bar in scalper_algorithm.df.open],
    'high': [bar for bar in scalper_algorithm.df.high],
    'low': [bar for bar in scalper_algorithm.df.low],
    'close': [bar for bar in scalper_algorithm.df.close],
    'volume': [bar for bar in scalper_algorithm.df.volume],
}
"""
"""
data = {
    'time': [bar[1] for bar in supertrend_algorithm.df.index],
    'open': [bar for bar in supertrend_algorithm.df.open],
    'high': [bar for bar in supertrend_algorithm.df.high],
    'low': [bar for bar in supertrend_algorithm.df.low],
    'close': [bar for bar in supertrend_algorithm.df.close],
    'volume': [bar for bar in supertrend_algorithm.df.volume],
}
"""

#scalper_algorithm_df = pd.DataFrame(data)
#scalper_algorithm_df['time'] = pd.to_datetime(scalper_algorithm_df['time'])
#scalper_algorithm_df.set_index('time', inplace=True) # sort by time
#supertrend_algorithm_df = pd.DataFrame(data)
#supertrend_algorithm_df['time'] = pd.to_datetime(supertrend_algorithm_df['time'])
#supertrend_algorithm_df.set_index('time', inplace=True) # sort by time
print(supertrend_algorithm.df)
#length = 200
# SMA Calculation
#df['200_DAY_SMA'] = df['close'].rolling(window=length).mean()
#print(df)

# EMA Calculation
#scalper_algorithm_df['200_DAY_EMA'] = scalper_algorithm_df['close'].ewm(span=length, adjust=False).mean() # TODO when adjust=False... data is calculated recursively
#print(df)

#ema = EMA(df)
#ema(200)
#print(ema.df)

#print(ema.df.tail(1))
#scalper_algorithm.buyConditions()
supertrend_algorithm.buyConditions()
#print(supertrend_algorithm.bars)

#print(supertrend_algorithm.df['buySignal'])

# TODO: remove this return

#scalper_algorithm_df = scalper_algorithm.df
#df.set_index('time', inplace=True) # sort by time

import plotly.graph_objects as go
fig = go.Figure()
"""
fig.add_trace(go.Candlestick(x=supertrend_algorithm.df.index,
                                     open=supertrend_algorithm.df['open'],
                                     high=supertrend_algorithm.df['high'],
                                     low=supertrend_algorithm.df['low'],
                                     close=supertrend_algorithm.df['close']))
"""
#fig.update_layout(template="plotly_dark") # DARK_MODE GRAPH
fig.add_trace(go.Candlestick(x=supertrend_algorithm.df.index,
                                     open=supertrend_algorithm.df['open'],
                                     high=supertrend_algorithm.df['high'],
                                     low=supertrend_algorithm.df['low'],
                                     close=supertrend_algorithm.df['close'],
                                     name="Candles"))

fig.add_trace(go.Scatter(x=supertrend_algorithm.df.index,
                         y=supertrend_algorithm.df['Upper_ATR'],
                         mode='lines',
                         name='Upper ATR',
                         line=dict(color='RED', width=2)))

fig.add_trace(go.Scatter(x=supertrend_algorithm.df.index,
                         y=supertrend_algorithm.df['Lower_ATR'],
                         mode='lines',
                         name='Lower ATR',
                         line=dict(color='GREEN', width=2)))
fig.show()

"""
fig = go.Figure()
fig.add_trace(go.Candlestick(x=scalper_algorithm_df.index,
                                     open=scalper_algorithm_df['open'],
                                     high=scalper_algorithm_df['high'],
                                     low=scalper_algorithm_df['low'],
                                     close=scalper_algorithm_df['close']))


fig.update_layout(title=f"{scalper_algorithm.symbol} Stock Price with 200-Day SMA",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    xaxis_rangeslider_visible=True)

fig.add_trace(go.Scatter(x=scalper_algorithm_df.index,
                         y=scalper_algorithm_df['200_DAY_EMA'],
                         mode='lines',
                         name='200-day EMA',
                         line=dict(color='CYAN', width=2)))

fig.update_layout(title=f"{scalper_algorithm.symbol} Stock Price with 200-Day EMA",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    xaxis_rangeslider_visible=True)

fig.show()
"""