
# charts/urls.py

from django.urls import path
from .views import StockChartView

urlpatterns = [
    path('stock/', StockChartView.as_view(), name='stock_chart'),
]
