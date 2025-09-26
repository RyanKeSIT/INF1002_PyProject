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
            y=[float(x) for x in df["Daily Return"]],
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
    # Plot the close price as an orange solid line
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=[float(x) for x in df['Close']],
        name='Close',
        line=dict(color='orange', width=2)
    ))

    # Plot the 20-day SMA as a light blue dashed line
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=[float(x) for x in df['SMA']],
        name='20-Day SMA',
        line=dict(color='lightblue', width=2, dash='dash')
    ))

    # Add green up-arrows for buy signals
    fig.add_trace(go.Scatter(
        x=df["Date"][df['buy_signal']],
        y=[float(x) for x in df['Close'][df['buy_signal']]],
        mode='markers',
        marker=dict(symbol='arrow-up', color='green', size=14),
        name='Buy Signal'
    ))

    # Add red down-arrows for sell signals
    fig.add_trace(go.Scatter(
        x=df["Date"][df['sell_signal']],
        y=[float(x) for x in df['Close'][df['sell_signal']]],
        mode='markers',
        marker=dict(symbol='arrow-down', color='red', size=14),
        name='Sell Signal'
    ))

    # Layout Style
    fig.update_layout(
        title="Close & 20-Day SMA with Buy/Sell Signals",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        legend=dict(orientation="h", y=0.99, x=0.01),
        title_font=dict(size=24)
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

def plot_overall(df):
    fig = go.Figure()

    # Candlestick trace
    fig.add_trace(go.Candlestick(
        x=df["Date"],
        open=[float(x) for x in df["Open"]],
        high=[float(x) for x in df["High"]],
        low=[float(x) for x in df["Low"]],
        close=[float(x) for x in df["Close"]],
        name="OHLC"
    ))

    # 20-day SMA trace
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=[float(x) for x in df['SMA']],
        name='20-Day SMA',
        line=dict(color='blue', width=2)
    ))

    # Buy signals
    fig.add_trace(go.Scatter(
        x=df["Date"][df['buy_signal']],
        y=[float(x) for x in df['Close'][df['buy_signal']]],
        mode='markers',
        marker=dict(symbol='arrow-up', color='green', size=14),
        name='Buy Signal'
    ))

    # Sell signals
    fig.add_trace(go.Scatter(
        x=df["Date"][df['sell_signal']],
        y=[float(x) for x in df['Close'][df['sell_signal']]],
        mode='markers',
        marker=dict(symbol='arrow-down', color='red', size=14),
        name='Sell Signal'
    ))

    # Layout Style
    fig.update_layout(
        title="Candlestick Chart with 20-Day SMA and Buy/Sell Signals",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=700,
        legend=dict(orientation="h", y=0.99, x=0.01),
        title_font=dict(size=24)
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)