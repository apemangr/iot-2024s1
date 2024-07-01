
# charts/urls.py

from django.urls import path
from . import views
urlpatterns = [
    path('stock/', views.stock_chart_view, name='stock_chart'),
]
