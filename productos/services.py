from productos.repositories import ProductoRepository
from categorias.models import Categoria
from django.core.exceptions import ObjectDoesNotExist 

class ProductoService:
    @staticmethod
    def listar_productos():
        return ProductoRepository.listar()
    
    @staticmethod
    def listar_por_categoria(categoria_id):
        # Lógica de Servicio: Podrías añadir aquí la verificación de que la categoría existe 
        # o simplemente delegar al repositorio.
        return ProductoRepository.obtener_por_categoria(categoria_id)

    @staticmethod
    def crear_producto(datos):
        # --- Lógica de Negocio (Validaciones) ---
        if datos.get('precio', 0) < 0:
            raise ValueError("El precio no puede ser negativo")

        # 🔄 Validar categoría usando el Django ORM (pk)
        categoria = datos.get('categoria')
        
        # Debug: Ver qué tipo de dato es
        # print(f"DEBUG - categoria type: {type(categoria)}, value: {categoria}")
        
        # Manejar si viene como ID o como objeto
        if isinstance(categoria, int):
            try:
                Categoria.objects.get(pk=categoria)
            except ObjectDoesNotExist:
                raise ValueError("Categoría no encontrada")
        elif isinstance(categoria, Categoria):
            # Ya es un objeto, validar que existe
            pass
        else:
            raise ValueError("Categoría no encontrada")
            
        # --- Persistencia ---
        return ProductoRepository.crear(datos)
    
    @staticmethod
    def obtener_producto(producto_id):
        producto = ProductoRepository.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        return producto

    @staticmethod
    def actualizar_producto(id, datos):
        # Lógica de servicio antes de actualizar, como validar campos o permisos
        return ProductoRepository.actualizar(id, datos)

    @staticmethod
    def eliminar_producto(id):
        # Lógica de servicio, como verificar si hay dependencias antes de eliminar
        return ProductoRepository.eliminar(id)