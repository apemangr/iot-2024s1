from django.contrib.auth import get_user_model
from django.db import models

# Obtén el modelo de usuario de Django
User = get_user_model()

# Modelo para guardar selecciones de acciones por usuario
class UserStockSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_selections')
    stock_symbol = models.CharField(max_length=50)  # Símbolo de la acción seleccionada

    def __str__(self):
        return f"{self.user.username} - {self.stock_symbol}"
