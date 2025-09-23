from flask import Flask, render_template, request
from model.tools.calculations import simple_moving_average, daily_returns, upward_downward_runs, max_profit
from model.tools.visualisation import plot_daily_returns,plot_price_sma_plotly, plot_candlestick, plot_updown_runs

#import plotly.graph_objects as go
import yfinance as yf

app = Flask(__name__, template_folder="../static/templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def analyze():
    ticker = request.form['ticker'].strip().upper()
    start = request.form['start']
    end = request.form['end']

    # Download stock data based on given ticker, start and end date
    df = yf.download(ticker, start=start, end=end)

    #Checks if dataframe is empty; no data within selected timeframe/ ticker
    if df.empty:
        return f"No data found for {ticker} between {start} and {end}."

    # Remove spaces from column names
    df.columns = [column[0].replace(' ', '') for column in df.columns]

    # Reset index so 'Date' becomes a column
    df.reset_index(inplace=True)

    df = simple_moving_average(df)
    df = daily_returns(df)
    profit, buy_and_sell_dates = max_profit(df)
    runs = upward_downward_runs(df)

    graph_daily_returns = plot_daily_returns(df)
    graph_sma = plot_price_sma_plotly(df)  # Original chart with SMA + markers
    graph_candle = plot_candlestick(df)   # New plain candlestick chart
    graph_runs = plot_updown_runs(df)

    return render_template('result.html', ticker=ticker, graph_daily_returns=graph_daily_returns, graph_sma=graph_sma,
                           graph_candle=graph_candle, graph_runs=graph_runs, runs=runs, buy_and_sell_dates=buy_and_sell_dates, profit=profit)