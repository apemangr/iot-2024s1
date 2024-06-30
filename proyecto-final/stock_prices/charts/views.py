# charts/views.py

from django.shortcuts import render
from .utils import get_stock_data

def stock_chart(request, ticker):
    data = get_stock_data(ticker)
    context = {
        'ticker': ticker,
        'dates': data.index.strftime('%Y-%m-%d').tolist(),
        'prices': data['Close'].tolist(),
    }
    return render(request, 'charts/stock_chart.html', context)

