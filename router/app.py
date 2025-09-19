# Import libraries
from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
import pandas as pd

# Import modules
from model.index import *
from model.tools import *

# API config
app = Flask(__name__)

# API routes
@app.route('/')
def index():
    #  Download stock data (e.g., Apple) for the last 3 months
    ticker = "AAPL"   # You can change this to any stock symbol
    #data = yf.download(ticker, period="3mo", interval="1d")
    data = pd.read_csv("AAPL.csv")
    print(data.head())  # <--- Add this
    data.reset_index(inplace=True)  # Make 'Date' a column instead of index
    
    #  Create Plotly candlestick
    fig = go.Figure(data=[go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    fig.update_layout(
        title=f"{ticker} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False
    )

    #Convert figure to HTML snippet
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('index.html', plot=graph_html, ticker=ticker)

if __name__ == "__main__":
    app.run(debug=True)
