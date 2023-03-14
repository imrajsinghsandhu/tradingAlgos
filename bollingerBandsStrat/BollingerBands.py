import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load financial data into a pandas dataframe
df = pd.read_csv('FinancialData-Analysis-AAPL.csv')

# Calculate the 20-day moving average and standard deviation
df['MA20'] = df['Close'].rolling(window=20).mean()
df['STD20'] = df['Close'].rolling(window=20).std()

# Calculate the upper and lower Bollinger Bands
df['UpperBand'] = df['MA20'] + 2*df['STD20']
df['LowerBand'] = df['MA20'] - 2*df['STD20']

# Define constants for starting position, risk, and max drawdown
STARTING_POSITION = 10000.0
RISK_PER_TRADE = 0.1
MAX_DRAWDOWN = 0.5

# Define a function to generate trade signals based on the Bollinger Bands
def generate_signals(data):
    buy_signals = []
    sell_signals = []
    long_position = False
    position_size = 0.0
    max_position_size = STARTING_POSITION * RISK_PER_TRADE
    for i in range(len(data)):
        if data['Close'][i] > data['UpperBand'][i]:
            if not long_position and position_size < max_position_size:
                buy_signals.append(i)
                long_position = True
                position_size = max_position_size
        elif data['Close'][i] < data['LowerBand'][i]:
            if long_position:
                sell_signals.append(i)
                long_position = False
                position_size = 0.0
        # Check for max drawdown
        if position_size > 0 and (data['Close'][i] - data['Close'][buy_signals[-1]]) / data['Close'][buy_signals[-1]] < -MAX_DRAWDOWN:
            sell_signals.append(i)
            long_position = False
            position_size = 0.0
    # If we still have a position open at the end of the data, close it
    if long_position:
        sell_signals.append(len(data) - 1)
    return buy_signals, sell_signals

# Generate trade signals based on the Bollinger Bands
buy_signals, sell_signals = generate_signals(df)

# Plot the Bollinger Bands and the trade signals
# fig, ax = plt.subplots(figsize=(15,7))
# ax.plot(df.index, df['Close'], color='blue', label='Close')
# ax.plot(df.index, df['MA20'], color='red', label='MA20')
# ax.plot(df.index, df['UpperBand'], color='green', label='Upper Band')
# ax.plot(df.index, df['LowerBand'], color='orange', label='Lower Band')
# ax.plot(df.iloc[buy_signals].index, df['Close'][buy_signals], '^', markersize=10, color='green', label='Buy Signal')
# ax.plot(df.iloc[sell_signals].index, df['Close'][sell_signals], 'v', markersize=10, color='red', label='Sell Signal')
# ax.legend()
# plt.show()

# Calculate the returns based on the trade signals
returns = [0.0]
position_size = 0.0
max_position_size = STARTING_POSITION * RISK_PER_TRADE
for i in range(1, len(df)):
    if i in buy_signals:
        position_size = max_position_size
    elif i in sell_signals:
        position_size = 0.0
    returns.append(position_size * (df['Close'][i] - df['Close'][i-1]))
df['Returns'] = returns
df['CumulativeReturns'] = STARTING_POSITION + np.cumsum(df['Returns'])

print('Cumulative returns:', df['CumulativeReturns'].iloc[-1])