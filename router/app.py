from flask import Flask, render_template, request
from model.tools.calculations import simple_moving_average, daily_returns, upward_downward_runs, max_profit
from model.tools.visualisation import plot_price_sma_plotly, plot_candlestick

import pandas as pd
import plotly
import plotly.graph_objects as go
import yfinance as yf
import json

app = Flask(__name__, template_folder="../static/templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def analyze():
    ticker = request.form['ticker'].strip().upper()
    start = request.form['start']
    end = request.form['end']

    # Download stock data
    df = yf.download(ticker, start=start, end=end)

    if df is None:
        return f"No data found for {ticker} between {start} and {end}."

    # Reset index so 'Date' becomes a column
    df.reset_index(inplace=True)

    # Simple Moving Average (5-day)
    df['SMA'] = df['Close'].rolling(window=5).mean()

    # Create interactive Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'], mode='lines', name='Close Price'
    ))
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['SMA'], mode='lines', name='5-Day SMA'
    ))
    fig.update_layout(
        title=f"{ticker} Closing Price & 5-Day SMA",
        xaxis_title="Date", yaxis_title="Price",
        template="plotly_white"
    )

    df = simple_moving_average(df)
    df = daily_returns(df)
    runs = upward_downward_runs(df)
    profit = max_profit(df['Close'].values)
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    graph_sma = plot_price_sma_plotly(df)  # Original chart with SMA + markers
    graph_candle = plot_candlestick(df)   # New plain candlestick chart

    return render_template('result.html', ticker=ticker, graph_json=graph_json, graph_sma=graph_sma,
                           graph_candle=graph_candle, runs=runs, profit=profit)