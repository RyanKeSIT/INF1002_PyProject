# Import libraries
import yfinance as yf
from pandas import DataFrame

# Import modules
from model.tools.calculations import simple_moving_average, daily_returns


def load_stock_data(ticker: dict[str, str], start: str, end: str, sma_period: int) -> DataFrame | str:
    """Downloads NRT data from YFinance and loads them to the DataFrame

    Args:
        ticker (dict[str, str]): The stock name
        start (str): Start Date
        end (str): End Date
        sma_period (int): The SMA period

    Returns:
        DataFrame | str: The prepared DataFrame or error string
    """

    # Download stock data
    df = yf.download(ticker, start=start, end=end)

    if df is None or df.empty:
        return f"No data found for {ticker} between {start} and {end}."

    # Remove spaces from column names
    df.columns = [column[0].replace(" ", "") for column in df.columns]

    # Reset index so 'Date' becomes a column
    df.reset_index(inplace=True)
    df = simple_moving_average(df, sma_period) # Calculate SMA based on user input
    df = daily_returns(df)  # Calculate daily returns

    return df
