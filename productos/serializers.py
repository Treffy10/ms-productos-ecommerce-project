from rest_framework import serializers
from .models import Producto 
from categorias.models import Categoria 

class CategoriaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre')

class ProductoSerializer(serializers.ModelSerializer):
    # Campo de lectura: Devuelve el objeto completo de categoría
    categoria = CategoriaSimpleSerializer(read_only=True)
    
    # Campo para escritura: Recibe solo el ID
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        write_only=True,
        source='categoria'
    )

    class Meta:
        model = Producto 
        fields = (
            'id', 
            'nombre', 
            'descripcion', 
            'precio', 
            'stock', 
            'imagen_url',
            'categoria',      # Lectura: objeto completo
            'categoria_id'    # Escritura: solo ID
        )
        read_only_fields = ('id',)