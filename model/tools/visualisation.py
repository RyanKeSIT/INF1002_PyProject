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


def plot_updown_runs(df):
    closes = df["Close"].values
    dates = df["Date"] if "Date" in df.columns else df.index

    # Store OHLC values for each day
    ohlc_values = df[["Open", "High", "Low", "Close"]].values

    fig = go.Figure()

    for i in range(1, len(closes)):
        color = "green" if closes[i] > closes[i - 1] else "red"

        # Get the OHLC data for the specific day
        hover_data = ohlc_values[i]

        fig.add_trace(
            go.Scatter(
                x=[dates[i - 1], dates[i]],
                y=[closes[i - 1], closes[i]],
                mode="lines",
                line=dict(color=color, width=2),
                showlegend=False,
                # Use hovertemplate to display the OHLC data
                hovertemplate=(
                    "<b>Date:</b> %{x|%d-%m-%Y}<br>"
                    "<b>Open:</b> %{customdata[0]:$.2f}<br>"
                    "<b>High:</b> %{customdata[1]:$.2f}<br>"
                    "<b>Low:</b> %{customdata[2]:$.2f}<br>"
                    "<b>Close:</b> %{customdata[3]:$.2f}<br>"
                    "<extra></extra>"
                ),
                # Pass the OHLC data to customdata
                customdata=[hover_data],
            )
        )

    fig.update_layout(
        title="Up and Down Runs",
        xaxis_title="Date",
        yaxis_title="Closing Price",
        template="plotly_white",
    )

    # Return JSON for Plotly
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
