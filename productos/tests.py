from django.test import TestCase, Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from productos.models import Producto
from productos.services import ProductoService
from productos.repositories import ProductoRepository
from categorias.models import Categoria
import json


class CategoriaModelTests(TestCase):
    """Tests para el modelo Categoria"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Electrónica",
            descripcion="Productos electrónicos"
        )
    
    def test_crear_categoria(self):
        """Verifica que una categoría se crea correctamente"""
        self.assertEqual(self.categoria.nombre, "Electrónica")
        self.assertEqual(self.categoria.descripcion, "Productos electrónicos")
    
    def test_str_categoria(self):
        """Verifica la representación en string de la categoría"""
        self.assertEqual(str(self.categoria), "Electrónica")
    
    def test_categoria_sin_descripcion(self):
        """Verifica que la descripción puede ser nula"""
        categoria = Categoria.objects.create(nombre="Ropa")
        self.assertIsNone(categoria.descripcion)


class ProductoModelTests(TestCase):
    """Tests para el modelo Producto"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Electrónica",
            descripcion="Productos electrónicos"
        )
        self.producto = Producto.objects.create(
            nombre="Laptop",
            descripcion="Laptop de alta gama",
            precio=1500,
            stock=10,
            categoria=self.categoria,
            imagen_url="https://example.com/laptop.jpg"
        )
    
    def test_crear_producto(self):
        """Verifica que un producto se crea correctamente"""
        self.assertEqual(self.producto.nombre, "Laptop")
        self.assertEqual(self.producto.precio, 1500)
        self.assertEqual(self.producto.stock, 10)
        self.assertEqual(self.producto.categoria.nombre, "Electrónica")
    
    def test_str_producto(self):
        """Verifica la representación en string del producto"""
        self.assertEqual(str(self.producto), "Laptop (Electrónica)")
    
    def test_producto_precio_cero(self):
        """Verifica que un producto puede tener precio 0"""
        producto = Producto.objects.create(
            nombre="Producto Gratis",
            precio=0,
            stock=5,
            categoria=self.categoria
        )
        self.assertEqual(producto.precio, 0)
    
    def test_producto_sin_imagen(self):
        """Verifica que imagen_url puede estar vacía"""
        producto = Producto.objects.create(
            nombre="Producto Sin Imagen",
            precio=100,
            stock=1,
            categoria=self.categoria
        )
        self.assertEqual(producto.imagen_url, "")
    
    def test_producto_stock_default(self):
        """Verifica que el stock por defecto es 0"""
        producto = Producto.objects.create(
            nombre="Producto Sin Stock",
            precio=50,
            categoria=self.categoria
        )
        self.assertEqual(producto.stock, 0)


class ProductoRepositoryTests(TestCase):
    """Tests para la capa de repositorio"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.categoria2 = Categoria.objects.create(nombre="Ropa")
        
        self.producto1 = Producto.objects.create(
            nombre="Laptop",
            precio=1500,
            stock=10,
            categoria=self.categoria
        )
        self.producto2 = Producto.objects.create(
            nombre="Mouse",
            precio=25,
            stock=100,
            categoria=self.categoria
        )
        self.producto3 = Producto.objects.create(
            nombre="Camiseta",
            precio=20,
            stock=50,
            categoria=self.categoria2
        )
    
    def test_listar_productos(self):
        """Verifica que se listan todos los productos"""
        productos = ProductoRepository.listar()
        self.assertEqual(len(productos), 3)
    
    def test_obtener_por_id(self):
        """Verifica que se obtiene un producto por ID"""
        producto = ProductoRepository.obtener_por_id(self.producto1.id)
        self.assertIsNotNone(producto)
        self.assertEqual(producto.nombre, "Laptop")
    
    def test_obtener_por_id_inexistente(self):
        """Verifica que retorna None si el ID no existe"""
        producto = ProductoRepository.obtener_por_id(9999)
        self.assertIsNone(producto)
    
    def test_obtener_por_categoria(self):
        """Verifica que se filtran productos por categoría"""
        productos = ProductoRepository.obtener_por_categoria(self.categoria.id)
        self.assertEqual(len(productos), 2)
        self.assertIn(self.producto1, productos)
        self.assertIn(self.producto2, productos)
        self.assertNotIn(self.producto3, productos)
    
    def test_crear_producto(self):
        """Verifica que se crea un producto correctamente"""
        datos = {
            'nombre': 'Monitor',
            'precio': 300,
            'stock': 5,
            'categoria': self.categoria
        }
        producto = ProductoRepository.crear(datos)
        self.assertIsNotNone(producto.id)
        self.assertEqual(producto.nombre, 'Monitor')
    
    def test_actualizar_producto(self):
        """Verifica que se actualiza un producto correctamente"""
        datos = {'precio': 2000, 'stock': 5}
        producto_actualizado = ProductoRepository.actualizar(self.producto1.id, datos)
        self.assertIsNotNone(producto_actualizado)
        self.assertEqual(producto_actualizado.precio, 2000)
        self.assertEqual(producto_actualizado.stock, 5)
    
    def test_actualizar_producto_inexistente(self):
        """Verifica que actualizar un producto inexistente retorna None"""
        datos = {'precio': 100}
        resultado = ProductoRepository.actualizar(9999, datos)
        self.assertIsNone(resultado)
    
    def test_eliminar_producto(self):
        """Verifica que se elimina un producto correctamente"""
        producto_id = self.producto1.id
        resultado = ProductoRepository.eliminar(producto_id)
        self.assertTrue(resultado)
        self.assertIsNone(ProductoRepository.obtener_por_id(producto_id))
    
    def test_eliminar_producto_inexistente(self):
        """Verifica que eliminar un producto inexistente retorna False"""
        resultado = ProductoRepository.eliminar(9999)
        self.assertFalse(resultado)


class ProductoServiceTests(TestCase):
    """Tests para la capa de servicio"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.categoria2 = Categoria.objects.create(nombre="Ropa")
        
        self.producto1 = Producto.objects.create(
            nombre="Laptop",
            precio=1500,
            stock=10,
            categoria=self.categoria
        )
        self.producto2 = Producto.objects.create(
            nombre="Camiseta",
            precio=20,
            stock=50,
            categoria=self.categoria2
        )
    
    def test_listar_productos(self):
        """Verifica que se listan todos los productos"""
        productos = ProductoService.listar_productos()
        self.assertEqual(len(productos), 2)
    
    def test_listar_por_categoria(self):
        """Verifica que se listan productos por categoría"""
        productos = ProductoService.listar_por_categoria(self.categoria.id)
        self.assertEqual(len(productos), 1)
        self.assertEqual(productos[0].nombre, "Laptop")
    
    def test_obtener_producto(self):
        """Verifica que se obtiene un producto correctamente"""
        producto = ProductoService.obtener_producto(self.producto1.id)
        self.assertEqual(producto.nombre, "Laptop")
    
    def test_obtener_producto_inexistente(self):
        """Verifica que lanza error si el producto no existe"""
        with self.assertRaises(ValueError) as context:
            ProductoService.obtener_producto(9999)
        self.assertEqual(str(context.exception), "Producto no encontrado")
    
    def test_crear_producto_exitoso(self):
        """Verifica que se crea un producto correctamente"""
        datos = {
            'nombre': 'Monitor',
            'precio': 300,
            'stock': 5,
            'categoria': self.categoria
        }
        producto = ProductoService.crear_producto(datos)
        self.assertIsNotNone(producto.id)
        self.assertEqual(producto.nombre, 'Monitor')
    
    def test_crear_producto_precio_negativo(self):
        """Verifica que rechaza precios negativos"""
        datos = {
            'nombre': 'Producto Inválido',
            'precio': -100,
            'stock': 5,
            'categoria': self.categoria
        }
        with self.assertRaises(ValueError) as context:
            ProductoService.crear_producto(datos)
        self.assertEqual(str(context.exception), "El precio no puede ser negativo")
    
    def test_crear_producto_categoria_inexistente(self):
        """Verifica que rechaza categorías inexistentes"""
        datos = {
            'nombre': 'Producto Inválido',
            'precio': 100,
            'stock': 5,
            'categoria': 9999
        }
        with self.assertRaises(ValueError) as context:
            ProductoService.crear_producto(datos)
        self.assertEqual(str(context.exception), "Categoría no encontrada")
    
    def test_actualizar_producto(self):
        """Verifica que se actualiza un producto correctamente"""
        datos = {'precio': 2000, 'stock': 20}
        producto = ProductoService.actualizar_producto(self.producto1.id, datos)
        self.assertEqual(producto.precio, 2000)
        self.assertEqual(producto.stock, 20)
    
    def test_eliminar_producto(self):
        """Verifica que se elimina un producto correctamente"""
        producto_id = self.producto1.id
        resultado = ProductoService.eliminar_producto(producto_id)
        self.assertTrue(resultado)


class ProductoAPITests(APITestCase):
    """Tests para los endpoints de la API"""
    
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            nombre="Electrónica",
            descripcion="Productos electrónicos"
        )
        self.producto1 = Producto.objects.create(
            nombre="Laptop",
            descripcion="Laptop de alta gama",
            precio=1500,
            stock=10,
            categoria=self.categoria,
            imagen_url="https://example.com/laptop.jpg"
        )
        self.producto2 = Producto.objects.create(
            nombre="Mouse",
            descripcion="Mouse inalámbrico",
            precio=25,
            stock=100,
            categoria=self.categoria,
            imagen_url="https://example.com/mouse.jpg"
        )
    
    def test_get_todos_productos(self):
        """Verifica que GET /productos/ retorna todos los productos"""
        response = self.client.get(reverse('productos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_productos_por_categoria(self):
        """Verifica que GET /productos/?categoria=id filtra por categoría"""
        response = self.client.get(reverse('productos'), {'categoria': self.categoria.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_producto_por_id(self):
        """Verifica que GET /productos/<id>/ retorna un producto específico"""
        response = self.client.get(reverse('producto', args=[self.producto1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Laptop')
        self.assertEqual(response.data['precio'], 1500)
    
    def test_get_producto_no_existente(self):
        """Verifica que GET de un producto inexistente retorna 404"""
        response = self.client.get(reverse('producto', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post_producto_exitoso(self):
        """Verifica que POST crea un producto correctamente"""
        datos = {
            'nombre': 'Monitor',
            'descripcion': 'Monitor 4K',
            'precio': 300,
            'stock': 5,
            'categoria_id': self.categoria.id,
            'imagen_url': 'https://example.com/monitor.jpg'
        }
        response = self.client.post(
            reverse('productos'),
            data=json.dumps(datos),
            content_type='application/json'
        )
        # Si no funciona, revisamos la respuesta
        if response.status_code != status.HTTP_201_CREATED:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, 
                           f"Error: {response.data}")
        else:
            self.assertEqual(response.data['nombre'], 'Monitor')
            self.assertTrue(Producto.objects.filter(nombre='Monitor').exists())
    
    def test_post_producto_precio_negativo(self):
        """Verifica que POST rechaza precios negativos"""
        datos = {
            'nombre': 'Producto Inválido',
            'precio': -100,
            'stock': 5,
            'categoria_id': self.categoria.id
        }
        response = self.client.post(
            reverse('productos'),
            data=json.dumps(datos),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_producto_categoria_inexistente(self):
        """Verifica que POST rechaza categorías inexistentes"""
        datos = {
            'nombre': 'Producto Inválido',
            'precio': 100,
            'stock': 5,
            'categoria_id': 9999
        }
        response = self.client.post(
            reverse('productos'),
            data=json.dumps(datos),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_serializador_producto(self):
        """Verifica que el serializador funciona correctamente"""
        from productos.serializers import ProductoSerializer
        serializer = ProductoSerializer(self.producto1)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'Laptop')
        self.assertEqual(data['precio'], 1500)
        self.assertEqual(data['categoria']['nombre'], 'Electrónica')
        # categoria_id es write_only, por lo que no debe aparecer en la salida
        self.assertNotIn('categoria_id', data)


class IntegrationTests(TestCase):
    """Tests de integración del flujo completo"""
    
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            nombre="Electrónica",
            descripcion="Productos electrónicos"
        )
    
    def test_flujo_completo_crear_listar_obtener(self):
        """Verifica el flujo: crear producto -> listar -> obtener por ID"""
        # Crear producto
        datos = {
            'nombre': 'Laptop',
            'descripcion': 'Laptop de alta gama',
            'precio': 1500,
            'stock': 10,
            'categoria_id': self.categoria.id,
            'imagen_url': 'https://example.com/laptop.jpg'
        }
        response = self.client.post(
            reverse('productos'),
            data=json.dumps(datos),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        producto_id = response.data['id']
        
        # Listar productos
        response = self.client.get(reverse('productos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Obtener producto específico
        response = self.client.get(reverse('producto', args=[producto_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Laptop')
    
    def test_stock_actualizado(self):
        """Verifica que el stock se puede actualizar correctamente"""
        producto = Producto.objects.create(
            nombre='Producto Test',
            precio=100,
            stock=10,
            categoria=self.categoria
        )
        
        # Actualizar stock
        producto.stock = 5
        producto.save()
        
        # Verificar
        producto_actualizado = Producto.objects.get(pk=producto.id)
        self.assertEqual(producto_actualizado.stock, 5)
