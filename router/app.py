# Import libraries
from flask import Flask, render_template, request, flash
from model.tools.data_loader import (
    load_stock_data,
)
from model.visualisation import (
    plot_price_sma_plotly,
    plot_daily_returns,
    plot_overall,
)

app = Flask(__name__, static_folder="../static", template_folder="../static/templates")
app.secret_key = "INF1002_P3-4_secret_key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def analyze():
    ticker = request.form["ticker"]
    start = request.form["start"]
    end = request.form["end"]
    sma_period = int(request.form["sma_period"])

    if start >= end:
        flash(
                "Invalid date: Start date must be before end date. Please try again.",
                "error",
            )
        return render_template("index.html")
    elif sma_period > 200:
        flash(
                "Invalid SMA Period: SMA Period must be 200 days or less. Please try again.",
                "error",
            )
        return render_template("index.html")
    else:

        # Load and prepare data 
        df, runs, profit, buy_and_sell_dates, single_best_profit = load_stock_data(
            ticker, start, end, sma_period
        )

        # Graphs plotting
        graph_sma = plot_price_sma_plotly(
            df, sma_period
        )  # Original chart with SMA + markers
        graph_daily_returns = plot_daily_returns(df)  # Daily Returns bar chart
        graph_overall = plot_overall(
            df, sma_period
        )  # Overall chart with candlestick, Close price vs SMA, and markers

        # Safely compute latest daily return and absolute price change
        if len(df) >= 2:
            latest_return = float(df["Daily Return"].iloc[-1])  # e.g. 0.0123 for +1.23%
            latest_change = float(df["Close"].iloc[-1] - df["Close"].iloc[-2])
            latest_close = float(df["Close"].iloc[-1])
        else:
            latest_return = None
            latest_change = None
            latest_close = None
        
        # Render results
        return render_template(
            "result.html",
            ticker=ticker,
            sma_period=sma_period,
            graph_sma=graph_sma,
            runs=runs,
            graph_daily_returns=graph_daily_returns,
            buy_and_sell_dates=buy_and_sell_dates,
            profit=profit,
            single_best_profit=single_best_profit,
            latest_return=latest_return,
            latest_change=latest_change,
            latest_close=latest_close,
            graph_overall=graph_overall,
        )
