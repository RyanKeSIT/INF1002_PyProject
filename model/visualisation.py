# Import libraries
import plotly.graph_objects as go
import json
import plotly
from pandas import DataFrame


def plot_daily_returns(df: DataFrame) -> str:
    """Plots The Daily Returns

    Args:
        df (DataFrame): The supplied DataFrame

    Returns:
        str: The JSON output of the DataFrame for Plotly ingestion
    """

    fig = go.Figure()
    # Bar Graph for Daily Returns
    fig.add_trace(
        go.Bar(
            x=df["Date"],
            y=[float(x) for x in df["Daily Return"]],
            hovertemplate=(
                "<b>Date:</b> %{x|%d-%m-%Y}<br>"
                "<b>Daily Return:</b> %{y:.2%}<br>"
                "<extra></extra>"
            ),
            marker_color=["green" if val >= 0 else "red" for val in df["Daily Return"]],
        )
    )

    fig.update_layout(
        title="Daily Returns",
        xaxis_title="Date",
        yaxis_title="Return",
        template="plotly_white",
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def plot_price_sma_plotly(df: DataFrame, sma_period: int) -> str:
    """Plots The Closing Price with Simple Moving Average (SMA) Markers

    Args:
        df (DataFrame): The supplied DataFrame

    Returns:
        str: The JSON output of the DataFrame for Plotly ingestion
    """

    fig = go.Figure()
    # Plot the close price as an orange solid line
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=[float(x) for x in df["Close"]],
            name="Close",
            line=dict(color="orange", width=2),
        )
    )

    # Plot the {{ sma_period }}-day SMA as blue solid line
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=[float(x) for x in df["SMA"]],
            name=f"{sma_period}-Day SMA",
            line=dict(color="blue", width=2),
        )
    )

    # Add green up-arrows for buy signals
    fig.add_trace(
        go.Scatter(
            x=df["Date"][df["buy_signal"]],
            y=[float(x) for x in df["Close"][df["buy_signal"]]],
            mode="markers",
            marker=dict(symbol="arrow-up", color="green", size=14),
            name="Buy Signal",
        )
    )

    # Add red down-arrows for sell signals
    fig.add_trace(
        go.Scatter(
            x=df["Date"][df["sell_signal"]],
            y=[float(x) for x in df["Close"][df["sell_signal"]]],
            mode="markers",
            marker=dict(symbol="arrow-down", color="red", size=14),
            name="Sell Signal",
        )
    )

    # Layout Style
    fig.update_layout(
        title=f"Close & { sma_period }-Day SMA with Buy/Sell Signals",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title_font=dict(size=24),
    )

    # Convert Plotly figure to JSON for rendering in HTML
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def plot_overall(df: DataFrame, sma_period: int) -> str:
    """Plots all the above plots together in one plot

    Args:
        df (DataFrame): The supplied DataFrame

    Returns:
        str: The JSON output of the DataFrame for Plotly ingestion
    """

    fig = go.Figure()

    # Candlestick trace
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=[float(x) for x in df["Open"]],
            high=[float(x) for x in df["High"]],
            low=[float(x) for x in df["Low"]],
            close=[float(x) for x in df["Close"]],
            name="OHLC",
        )
    )

    # Plot the close price as an orange solid line
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=[float(x) for x in df["Close"]],
            name="Close",
            line=dict(color="orange", width=2),
        )
    )

    # SMA trace
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=[float(x) for x in df["SMA"]],
            name=f"{sma_period}-Day SMA",
            line=dict(color="blue", width=2),
        )
    )

    # Buy signals
    fig.add_trace(
        go.Scatter(
            x=df["Date"][df["buy_signal"]],
            y=[float(x) for x in df["Close"][df["buy_signal"]]],
            mode="markers",
            marker=dict(symbol="arrow-up", color="green", size=14),
            name="Buy Signal",
        )
    )

    # Sell signals
    fig.add_trace(
        go.Scatter(
            x=df["Date"][df["sell_signal"]],
            y=[float(x) for x in df["Close"][df["sell_signal"]]],
            mode="markers",
            marker=dict(symbol="arrow-down", color="red", size=14),
            name="Sell Signal",
        )
    )

    # Layout Style
    fig.update_layout(
        title=f"Candlestick Chart with {sma_period}-Day SMA and Buy/Sell Signals",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=700,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title_font=dict(size=24),
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
