import numpy as np
import pandas as pd

def simple_moving_average(df, window=5):
    df["SMA"] = df["Close"].rolling(window=window).mean()
    return df


def daily_returns(df):
    df["Daily Return"] = df["Close"].pct_change()
    return df


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

    df['Daily Returns'] = df['Close'].diff() #Difference between current day's and previous day's closing price
    profitable_days =df[df['Daily Returns']>0] #Dataframe rows where daily returns are greater than 0
    total_profit = profitable_days['Daily Returns'].sum() # Sums Profit of all days with positive daily returns
    df['ProfitGroup'] = (df['Daily Returns'] <= 0).cumsum() #Creates new group everytime daily return drops
    profitable_runs = df[df['Daily Returns'] > 0].groupby('ProfitGroup') #Group best buy and sell days 
    buy_and_sell_dates = [] 

    for sellBuyGroup, group_df in profitable_runs: #SellBuyGroup: Group Ids; group_df: date, close, high, low, open, volume, sma, daily return (in %), direction, daily return (in $) and profit group number
        buy_date = group_df['Date'].iloc[0] # First day of the current run 
        sell_date = group_df['Date'].iloc[-1] # Last day of current run 
        groupProfit = group_df['Daily Returns'].sum() #Sum profit of the current run 
        
        buy_and_sell_dates.append({
            "Buy Date": pd.to_datetime(buy_date).strftime("%d-%m-%Y"),
            "Sell Date": pd.to_datetime(sell_date).strftime("%d-%m-%Y"),
            "Profit": f"${groupProfit:.2f}"
        })
        
    single_best_profit = max(buy_and_sell_dates, key=lambda x: float(x['Profit'][1:])) #Get highest profit by slicing $ from all profts
    return f"${round(total_profit, 2)}", buy_and_sell_dates, single_best_profit

