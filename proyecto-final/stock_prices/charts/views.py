# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
from .models import UserStockSelection

@login_required
def stock_chart_view(request):
    all_stocks = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "FB",
        "TSLA", "NFLX", "NVDA", "INTC", "AMD"
    ]
    template_name = "charts/stock_chart.html"
    user = request.user

    if request.method == 'POST':
        # Obtener selecciones del formulario
        period = request.POST.get("period", "1y")
        interval = request.POST.get("interval", "1d")
        selected_stocks = request.POST.getlist("stocks")

        # Limpiar selecciones anteriores del usuario
        UserStockSelection.objects.filter(user=user).delete()

        # Guardar nuevas selecciones en UserStockSelection
        for stock_symbol in selected_stocks:
            selection = UserStockSelection(user=user, stock_symbol=stock_symbol)
            selection.save()

    else:
        # Valores predeterminados para period e interval
        period = "1y"
        interval = "1d"

    # Obtener las selecciones actuales del usuario
    user_selections = UserStockSelection.objects.filter(user=user)
    selected_stocks = [selection.stock_symbol for selection in user_selections]

    # Obtener datos de las acciones seleccionadas y crear gráficos
    if selected_stocks:
        fig = make_subplots(rows=len(selected_stocks), cols=1, shared_xaxes=True)

        for idx, stock_symbol in enumerate(selected_stocks, start=1):
            stock = yf.Ticker(stock_symbol)
            hist = stock.history(period=period, interval=interval)

            fig.add_trace(
                go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name=f"{stock_symbol}"),
                row=idx,
                col=1,
            )

        fig.update_layout(
            title="Precios de Acciones",
            xaxis_title="Fecha",
            yaxis_title="Precio de Cierre",
            height=len(selected_stocks) * 400,
            showlegend=True,
        )

        # Convertir el gráfico a HTML
        chart_html = pio.to_html(fig, full_html=False)
    else:
        chart_html = None

    context = {
        "chart": chart_html,
        "selected_period": period,
        "selected_interval": interval,
        "selected_stocks": selected_stocks,
        "all_stocks": all_stocks,
    }

    return render(request, template_name, context)

