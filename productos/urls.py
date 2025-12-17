from django.urls import path
from productos.views import productos_view, producto_view


urlpatterns = [
    path('productos/', productos_view, name='productos'),
    path('productos/<int:id>/', producto_view, name='producto'),
]