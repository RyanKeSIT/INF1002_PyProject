"""References
1. https://www.geeksforgeeks.org/python/using-pandas-to_datetime-with-timestamps/

"""

import numpy as np
import pandas as pd

def simple_moving_average(df, window=20):
    df["SMA"] = df["Close"].rolling(window=window).mean()
    df["prev_close"] = df["Close"].shift(1)
    df["prev_sma"] = df["SMA"].shift(1)
    # Buy signal when yesterday’s close was at or below the SMA and today’s close is above
    df['buy_signal']  = (df['prev_close'] <= df['prev_sma']) & (df['Close'] > df['SMA'])
    # Sell signal when yesterday’s close was at or above the SMA and today’s close is below
    df['sell_signal'] = (df['prev_close'] >= df['prev_sma']) & (df['Close'] < df['SMA'])
    return df

def daily_returns(df):
    df["Daily Return"] = df["Close"].pct_change()*100
    return df

#   Dong Han
def latest_daily_return_and_change(df):

    # Returns the latest daily return (%) and latest price change.

    latest_return = df["Daily Return"].iloc[-1]
    latest_change = df["Close"].iloc[-1] - df["Close"].iloc[-2]
    latest_close = df["Close"].iloc[-1]  # <-- latest closing price
    return latest_return, latest_change, latest_close

def upward_downward_runs(df):
    df["Direction"] = np.where(
        df["Close"] > df["Close"].shift(1),
        1,
        np.where(df["Close"] < df["Close"].shift(1), -1, 0),
    )
    runs = {"up_count": 0, "down_count": 0, "longest_up": 0, "longest_down": 0}
    current_up = current_down = 0
    for d in df["Direction"]:
        if d == 1:
            current_up += 1
            runs["up_count"] += 1
            runs["longest_up"] = max(runs["longest_up"], current_up)
            current_down = 0
        elif d == -1:
            current_down += 1
            runs["down_count"] += 1
            runs["longest_down"] = max(runs["longest_down"], current_down)
            current_up = 0
        else:
            current_up = current_down = 0
    return runs

def max_profit(df):
    profit = 0  # Initialize total profit
    prices = df["Close"]
    dates = df["Date"]
    buy_and_sell_dates = []
    for i in range(1, len(prices)):
        if (
            prices[i] > prices[i - 1]
        ):  # check if today’s price is higher than yesterday’s
            profit += prices[i] - prices[i - 1]  # add the difference to total profit
            buy_and_sell_dates.append(
                {
                    "Buy Date": pd.to_datetime(dates[i - 1]).strftime("%d-%m-%Y"),
                    "Sell Date": pd.to_datetime(dates[i]).strftime(("%d-%m-%Y")),
                }
            )
    return f"${round(profit,2)}", buy_and_sell_dates
