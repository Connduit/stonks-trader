from ScalperAlgorithm import ScalperAlgorithm

import plotly.graph_objects as go

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import TimeFrame
from alpaca.data.models import Bar
from alpaca.data.requests import StockQuotesRequest, StockBarsRequest

# Your Alpaca API credentials
api_key = ''
api_secret = ''

# Set up the configuration
#config = Config(API_KEY_ID=api_key, API_SECRET_KEY=api_secret)

# Initialize the Alpaca historical data client
client = StockHistoricalDataClient(api_key, api_secret)

# Define the symbol and the timeframe
symbol = 'AAPL'  # Example: Apple stock
timeframe = TimeFrame.Day  # Can be 'Minute', 'Hour', 'Day', etc.
lookback_period = 100  # Number of days to fetch
start_time = pd.to_datetime("2024-02-21").tz_localize("America/New_York") # TODO: start time should be current date - 1 year?

request_params = StockBarsRequest(
    symbol_or_symbols=symbol,
    timeframe=timeframe,
    start=start_time
)

# Fetch the historical data
bars = client.get_stock_bars(request_params).df.tz_convert("America/New_York", level=1)

# Convert the data into a pandas DataFrame
data = {
    'time': [bar[1] for bar in bars.index],
    'open': [bar for bar in bars.open],
    'high': [bar for bar in bars.high],
    'low': [bar for bar in bars.low],
    'close': [bar for bar in bars.close],
    'volume': [bar for bar in bars.volume],
}

df = pd.DataFrame(data)
df['time'] = pd.to_datetime(df['time'])  # Convert time to datetime format
df.set_index('time', inplace=True)

# Calculate the Moving Average (e.g., 10-day moving average)
df['50_day_MA'] = df['close'].rolling(window=10).mean()

# Display the results
print(df[['close', '50_day_MA']].tail())  # Show the most recent data with moving average

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']))

fig.add_trace(go.Scatter(x=df.index,
                         y=df['50_day_MA'],
                         mode='lines',
                         name='20-day SMA',
                         line=dict(color='orange', width=2)))

fig.update_layout(title=f"{symbol} Stock Price with 20-Day SMA",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    xaxis_rangeslider_visible=True)

fig.show()