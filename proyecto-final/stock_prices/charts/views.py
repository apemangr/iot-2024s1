# charts/views.py
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
import yfinance as yf
from django.views.generic.base import TemplateView


class StockChartView(TemplateView):
    template_name = "charts/stock_chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Valores predeterminados
        period = self.request.POST.get("period", "1y")
        interval = self.request.POST.get("interval", "1d")

        stock = yf.Ticker("USDCLP=x")
        hist = stock.history(period=period, interval=interval)

        # Crear el gráfico con Plotly
        # fig = go.Figure()
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

        context["chart"] = chart_html
        context["selected_period"] = period
        context["selected_interval"] = interval

        return context

