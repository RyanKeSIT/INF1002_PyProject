"""References
1. https://plotly.com/python/bar-charts/
"""

import plotly.graph_objects as go
import json
import plotly


def plot_daily_returns(df):
    fig = go.Figure()
    #Bar Graph for Daily Returns
    fig.add_trace(
        go.Bar(
            x=df["Date"],
            y=[float(x) for x in df["Daily Return"]],
            # Stock went up (>0) = Green; Stock Went Down (<0) = red
            marker_color=["green" if ret > 0 else "red" for ret in df["Daily Return"]],  
            #Custom template for hovered data
            hovertemplate=(
                "<b>Date:</b> %{x|%d-%m-%Y}<br>"
                "<b>Daily Return:</b> %{y:.2%}<br>"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title="Daily Returns",
        xaxis_title="Date",
        yaxis_title="Return",
        template="plotly_white",
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def plot_price_sma_plotly(df):
    fig = go.Figure()
    # Closing price
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines+markers",
            name="Close Price",
            line=dict(color="blue", width=1),
        )
    )

    # SMA
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["SMA"],
            mode="lines",
            name="SMA",
            line=dict(color="orange"),
        )
    )

    fig.update_layout(
        title="Stock Closing Price vs SMA",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        xaxis=dict(rangeslider=dict(visible=True)),
    )

    # Convert Plotly figure to JSON for rendering in HTML
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def plot_candlestick(df):
    """
    Generates a Plotly candlestick chart without SMA or markers.
    """
    fig = go.Figure(
        go.Candlestick(
            x=df["Date"],
            open=[float(x) for x in df["Open"]],
            high=[float(x) for x in df["High"]],
            low=[float(x) for x in df["Low"]],
            close=[float(x) for x in df["Close"]],
            name="OHLC",
        )
    )

    fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        xaxis=dict(rangeslider=dict(visible=False)),
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
