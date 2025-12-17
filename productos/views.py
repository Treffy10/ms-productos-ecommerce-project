from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from productos.serializers import ProductoSerializer
from .services import ProductoService

@api_view(['GET', 'POST'])
def productos_view(request):
    if request.method == 'GET':
        categoria_id = request.GET.get('categoria')
        try:
            if categoria_id:
                productos = ProductoService.listar_por_categoria(categoria_id)
            else:
                productos = ProductoService.listar_productos()

            serializer = ProductoSerializer(productos, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=404)

    elif request.method == 'POST':
        try:
            producto = ProductoService.crear_producto(request.data)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def producto_view(request, id):
    try:
        producto = ProductoService.obtener_producto(id)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    except ValueError as e:
        return Response({'error': str(e)}, status=404)
