
# charts/utils.py

import yfinance as yf

def get_stock_data(ticker, period="1mo", interval="15m"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist
