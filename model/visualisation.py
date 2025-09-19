import plotly.graph_objects as go
import pandas as pd
import json
import plotly

def plot_price_sma_plotly(df):
    fig = go.Figure()
    # Closing price
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue')
    ))

    # SMA
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['SMA'],
        mode='lines',
        name='SMA',
        line=dict(color='orange')
    ))

    fig.update_layout(
        title='Stock Closing Price vs SMA',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        xaxis=dict(rangeslider=dict(visible=True))
    )

    # Convert Plotly figure to JSON for rendering in HTML
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def plot_candlestick(df):
    """
    Generates a Plotly candlestick chart without SMA or markers.
    """
    df= pd.read_csv("data/AAPL.csv")
    fig = go.Figure(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='OHLC'
    ))

    fig.update_layout(
        title='Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        xaxis=dict(rangeslider=dict(visible=False))
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)