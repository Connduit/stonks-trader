import numpy as np
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, TimeFrame
import datetime

# Configure Alpaca API keys
API_KEY = ''
API_SECRET = ''

# Initialize Alpaca StockHistoricalDataClient with your API keys
client = StockHistoricalDataClient(API_KEY, API_SECRET)

# Define the symbol, time frame, and date range
symbol = 'AAPL'  # Example symbol (Apple)
time_frame = TimeFrame.Day  # You can use TimeFrame.Hour or TimeFrame.Day as needed
start_date = datetime.datetime(2025, 2, 1)
end_date = datetime.datetime(2025, 2, 21)

# Create a StockBarsRequest object with the desired parameters
request = StockBarsRequest(
    symbol_or_symbols=symbol,
    timeframe=time_frame,
    start=start_date,
    end=end_date
)

# Get the historical bar data using the StockBarsRequest
bar_set = client.get_stock_bars(request)

# Initialize the list to store closing prices
closing_prices = []

# Loop through the BarSet and collect the closing prices
for symbol, bars in bar_set.data.items():
    for bar in bars:
        closing_prices.append(bar.close)

# Calculate the Simple Moving Average (SMA) for a window of size n
window_size = 21  # Example: 10-period moving average
sma_values = []

# Make sure we have enough data to calculate the moving average
if len(closing_prices) >= window_size:
    for i in range(window_size - 1, len(closing_prices)):
        window = closing_prices[i - window_size + 1: i + 1]
        sma = np.mean(window)  # Calculate the average of the window
        sma_values.append(sma)

# Print the results
print(f"SMA values (window size {window_size}):")
for i, sma in enumerate(sma_values):
    print(f"Index {i + window_size - 1}: SMA = {sma:.2f}")
