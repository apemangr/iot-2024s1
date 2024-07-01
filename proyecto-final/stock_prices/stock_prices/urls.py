# stock_prices/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Añadir esta línea
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('', include('charts.urls')),
]

