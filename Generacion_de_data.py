import os
import django
from faker import Faker
import random
from django.db import IntegrityError # Importamos para manejar errores de duplicidad

# --- 1. Configuración de Django ---
# Configura el entorno, asumiendo que tu settings.py ya apunta a PostgreSQL
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicio_productos.settings')
django.setup()

# ❌ Se elimina la conexión a MongoDB (import mongoengine y connect)

from productos.models import Producto
from categorias.models import Categoria

fake = Faker('es_ES')

# --- URLs de Imagenes Falsas para el campo 'imagen_url' ---
# Usaremos Placehold.it o un servicio similar para generar URLs de imágenes de prueba.
def generar_imagen_url_falsa(ancho=400, alto=300):
    """Devuelve una URL de imagen falsa (ej: https://picsum.photos/400/300)."""
    # Puedes cambiar 'picsum.photos' por 'placehold.it' si prefieres cuadrados grises.
    return f"https://picsum.photos/{ancho}/{alto}?random={random.randint(1, 1000)}"


# --- 2. Funciones de Seeding (PostgreSQL/Django ORM) ---

def generar_categorias():
    nombres = ['Tecnología', 'Ropa', 'Hogar', 'Deportes', 'Salud', 'Libros', 'Mascotas', 'Juguetes']
    categorias = []
    
    for nombre in nombres:
        try:
            # 🟢 Usamos get_or_create() para obtener la categoría si existe o crearla si no.
            cat, created = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': fake.sentence()}
            )
            categorias.append(cat)
            
            if created:
                print(f"   -> Creada: {nombre}")

        except IntegrityError as e:
            # Manejar cualquier posible error de integridad, aunque get_or_create lo maneja bien.
            print(f"   -> Error al crear {nombre}: {e}")
            
    print(f"✅ {len(categorias)} categorías gestionadas (creadas/existentes).")
    return categorias

def generar_productos(n=2000):
    categorias = generar_categorias()
    if not categorias:
        print("🛑 No se pudieron generar productos: No hay categorías disponibles.")
        return

    productos_a_crear = []
    
    for i in range(n):
        producto = Producto(
            # 🟢 La creación de instancias es la misma, pero ahora usando models.Model
            nombre=fake.unique.catch_phrase(),
            descripcion=fake.text(max_nb_chars=100),
            precio=round(random.uniform(5.0, 2000.0), 2),
            stock=random.randint(1, 500),
            
            # 🟢 Campo Nuevo: Usando la URL falsa
            imagen_url=generar_imagen_url_falsa(),
            
            # 🟢 Asigna el objeto Categoria (ForeignKey)
            categoria=random.choice(categorias) 
        )
        productos_a_crear.append(producto)
        
    # 🟢 MEJORA: Usar bulk_create para insertar productos de golpe (mucho más rápido en SQL)
    Producto.objects.bulk_create(productos_a_crear)

    print(f"✅ {n} productos generados exitosamente en PostgreSQL (bulk_create).")

# --- 3. Ejecución ---

if __name__ == "__main__":
    # Opcional: Limpiar datos anteriores (si quieres empezar de cero)
    # print("Limpiando datos antiguos...")
    # Producto.objects.all().delete()
    # Categoria.objects.all().delete()
    
    generar_productos(n=500) # Reducido a 500 para una prueba más rápida.