from django.db.models import ObjectDoesNotExist
from productos.models import Producto
from categorias.models import Categoria

class ProductoRepository:
    # --- Consultas ---
    @staticmethod
    def listar():
        # Django ORM: Devuelve todos los objetos.
        return Producto.objects.all() 

    @staticmethod
    def obtener_por_id(id):
        try:
            # Django ORM: Usa get para obtener por Clave Primaria (pk)
            # Si no lo encuentra, lanza una excepción (mejor que devolver None)
            return Producto.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None # Devolvemos None para mantener la firma original
    
    @staticmethod
    def obtener_por_categoria(categoria_id):
        # 🟢 Opción 1: Filtrar usando el campo ForeignKey_id
        return Producto.objects.filter(categoria_id=categoria_id)

    # --- Mutaciones ---
    @staticmethod
    def crear(datos):
        # 🟢 Mejor práctica: Usa el método .create() del Manager
        return Producto.objects.create(**datos)

    @staticmethod
    def actualizar(id, datos):
        try:
            producto = Producto.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None
        
        # Actualizar usando setattr() es correcto.
        for campo, valor in datos.items():
            setattr(producto, campo, valor)
            
        producto.save()
        return producto

    @staticmethod
    def eliminar(id):
        try:
            producto = Producto.objects.get(pk=id)
            producto.delete() # 🟢 Usa el método delete()
            return True
        except ObjectDoesNotExist:
            return False