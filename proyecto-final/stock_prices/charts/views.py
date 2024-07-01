from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

@login_required
def stock_chart_view(request):
    template_name = "charts/stock_chart.html"

    # Valores predeterminados
    period = request.POST.get("period", "1y")
    interval = request.POST.get("interval", "1d")

    stock = yf.Ticker("USDCLP=x")
    hist = stock.history(period=period, interval=interval)

    # Crear el gráfico con Plotly
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
        ),
        col=2,
        row=1,
    )
    fig.add_trace(
        go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name="USD/CAD"),
        col=1,
        row=1,
    )
    fig.update_layout(
        title="USD/CLP Stock Price", xaxis_title="Date", yaxis_title="Close Price"
    )

    # Convertir el gráfico a HTML
    chart_html = pio.to_html(fig, full_html=False)

    context = {
        "chart": chart_html,
        "selected_period": period,
        "selected_interval": interval,
    }

    return render(request, template_name, context)

