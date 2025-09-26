from flask import Flask, render_template, request
from model.tools.calculations import (
    upward_downward_runs,
    max_profit,
)
from model.tools.data_loader import (
    load_stock_data,
)
from model.tools.visualisation import (
    plot_price_sma_plotly,
    plot_candlestick,
    plot_daily_returns,
    plot_overall,
)

import plotly.graph_objects as go

# app = Flask(__name__, template_folder="../static/templates")
app = Flask(__name__, static_folder="../static", template_folder="../static/templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def analyze():
    ticker = request.form["ticker"]
    start = request.form["start"]
    end = request.form["end"]
    df = load_stock_data(ticker, start, end)
    runs = upward_downward_runs(df)
    profit, buy_and_sell_dates = max_profit(df)

    graph_sma = plot_price_sma_plotly(df)  # Original chart with SMA + markers
    graph_candle = plot_candlestick(df)  # New plain candlestick chart
    graph_daily_returns = plot_daily_returns(df)
    graph_overall = plot_overall(df)  # Combined chart with candlestick, SMA, and markers

    # DH Safely compute latest daily return and absolute price change
    if len(df) >= 2:
        latest_return = float(df["Daily Return"].iloc[-1])  # e.g. 0.0123 for +1.23%
        latest_change = float(df["Close"].iloc[-1] - df["Close"].iloc[-2])
        latest_close = float(df["Close"].iloc[-1])
    else:
        latest_return = None
        latest_change = None
        latest_close = None

    return render_template(
        "result.html",
        ticker=ticker,
        graph_sma=graph_sma,
        graph_candle=graph_candle,
        runs=runs,
        graph_daily_returns=graph_daily_returns,
        buy_and_sell_dates=buy_and_sell_dates,
        profit=profit,
        latest_return=latest_return,
        latest_change=latest_change,
        latest_close=latest_close,
        graph_overall=graph_overall,
    )