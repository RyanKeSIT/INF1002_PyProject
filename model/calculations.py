import numpy as np

def simple_moving_average(df, window=5):
    df['SMA'] = df['Close'].rolling(window=window).mean()
    return df

def daily_returns(df):
    df['Daily Return'] = df['Close'].pct_change()
    return df

def upward_downward_runs(df):
    df['Direction'] = np.where(
        df['Close'] > df['Close'].shift(1), 1,
        np.where(df['Close'] < df['Close'].shift(1), -1, 0)
    )
    runs = {'up_count': 0, 'down_count': 0,
            'longest_up': 0, 'longest_down': 0}
    current_up = current_down = 0
    for d in df['Direction']:
        if d == 1:
            current_up += 1
            runs['up_count'] += 1
            runs['longest_up'] = max(runs['longest_up'], current_up)
            current_down = 0
        elif d == -1:
            current_down += 1
            runs['down_count'] += 1
            runs['longest_down'] = max(runs['longest_down'], current_down)
            current_up = 0
        else:
            current_up = current_down = 0
    return runs

def max_profit(prices):
    profit = 0 #Initialize total profit
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]: #check if today’s price is higher than yesterday’s
            profit += prices[i] - prices[i-1] #add the difference to total profit
    return profit
