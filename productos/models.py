from django.db import models
from categorias.models import Categoria  

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"
    
    class Meta:
        db_table = 'productos'