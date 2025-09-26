import pandas as pd
import yfinance as yf
from model.tools.calculations import (
    simple_moving_average,
    daily_returns
)
def load_stock_data(ticker, start, end):
    # Download stock data
    df = yf.download(ticker, start=start, end=end)
    
    if df.empty:
        return f"No data found for {ticker} between {start} and {end}."

    # Remove spaces from column names
    df.columns = [column[0].replace(" ", "") for column in df.columns]

    # Reset index so 'Date' becomes a column
    df.reset_index(inplace=True)
    df = simple_moving_average(df) # Calculate 20-day SMA
    df = daily_returns(df)  # Calculate daily returns
    
    return df
