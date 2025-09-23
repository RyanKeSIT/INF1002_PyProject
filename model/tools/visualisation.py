"""References
1. https://plotly.com/python/hover-text-and-formatting/
"""

import plotly.graph_objects as go
import json
import plotly


def plot_daily_returns(df):
    df_plot = df.iloc[1:].copy()

    if df_plot.empty:
        # Return a valid empty Plotly figure
        return json.dumps(go.Figure(), cls=plotly.utils.PlotlyJSONEncoder)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_plot["Date"],
            y=df_plot["Daily Return"],
            orientation="v",  # Vertical bar graph
            marker_color=[
                "green" if ret > 0 else "red" if ret < 0 else "gray"
                for ret in df_plot["Daily Return"]
            ],  # Stock went up (>0) = Green; Stock Went Down (<0) = Red else Gray
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
