
# charts/urls.py

from django.urls import path
from .views import stock_chart

urlpatterns = [
    path('stock/<str:ticker>/', stock_chart, name='stock_chart'),
]
