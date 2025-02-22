from EngulfingCandle import engulfingCandle
from ScalperAlgorithm import ScalperAlgorithm
#import datetime
from datetime import timedelta
from datetime import datetime
import pandas as pd
from alpaca.trading.requests import GetCalendarRequest


api_key = ''
api_secret = ''

scalper_algorithm = ScalperAlgorithm(api_key, api_secret)
day = timedelta(days=1)
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
start_time = datetime(2024, 2, 21) # TODO: hard coded for quick testing purposes... change later
end_time = datetime(2025, 2, 21) # TODO: hard coded for quick testing purposes... change later

scalper_algorithm.getMarketData(start_time)
#print(scalper_algorithm.bars)
import btalib
print(scalper_algorithm.bars.df)

print(scalper_algorithm.df['close'])

data = {
    'time': [bar[1] for bar in scalper_algorithm.df.index],
    'open': [bar for bar in scalper_algorithm.df.open],
    'high': [bar for bar in scalper_algorithm.df.high],
    'low': [bar for bar in scalper_algorithm.df.low],
    'close': [bar for bar in scalper_algorithm.df.close],
    'volume': [bar for bar in scalper_algorithm.df.volume],
}

df = pd.DataFrame(data)
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True) # sort by time
print(df)
length = 200
# SMA Calculation
df['200_DAY_SMA'] = df['close'].rolling(window=length).mean()
print(df)

# EMA Calculation
df['200_DAY_EMA'] = df['close'].ewm(span=length, adjust=False).mean()
print(df)