"""from baseDeDatos import UsarBaseDeDatos

from datetime import datetime, timedelta
from random import randint

# Crear una instancia de la clase UsarBaseDeDatos
base_de_datos = UsarBaseDeDatos()

# Obtener la fecha de hoy
fecha_actual = datetime.now().strftime("%d-%m-%y")

# Lista de productos
productos = base_de_datos.ver_inventario()

# Generar ventas
for i in range(5):
    producto = productos[randint(0, len(productos) - 1)]
    codigo = producto['codigo']
    nombre = producto['nombre']
    precio = producto['precio']
    cantidad = randint(1, 10)
    total = round(precio * cantidad, 2)
    nombre_cliente = "Daniel Lopez"
    documento_cliente = "0000000"
    usuario = "aperez1"
    fecha_venta = (datetime.now() + timedelta(days=i)).strftime("%d-%m-%y")
    hora_venta = datetime.now().strftime("%H:%M:%S")

    # Guardar la venta en la base de datos
    base_de_datos.guardar_ventas([{
        'codigo': codigo,
        'nombre': nombre,
        'precio': precio,
        'cantidad': cantidad
    }], total, nombre_cliente, documento_cliente, usuario, fecha_venta, hora_venta)

# Obtener las ventas del mes actual
fecha_inicio = datetime(datetime.now().year, datetime.now().month, 1).strftime("%d-%m-%y")
fecha_fin = fecha_actual

ventas_del_mes = base_de_datos.obtener_ventas(fecha_inicio, fecha_fin)

# Imprimir las ventas
for venta in ventas_del_mes:
    for producto in venta['productos']:
        print(f"{producto['codigo']}\t{producto['nombre']}\t{producto['precio']}\t{producto['cantidad']}\t{venta['total_venta']}\t{venta['nombreCliente']}\t{venta['documentoCliente']}\t{venta['usuario']}\t{venta['fecha']}\t{venta['hora']}")
"""

lista = [
    [{'codigo': '666', 'nombre': 'shampoo', 'precio': 19000.0, 'cantidad': 5}, 
     {'codigo': '555', 'nombre': 'alimento para perro 20kg', 'precio': 9855.4, 'cantidad': 8}, 
     {'codigo': '666', 'nombre': 'shampoo', 'precio': 19000.0, 'cantidad': 1}],
     
    [{'codigo': '555', 'nombre': 'alimento para perro 20kg', 'precio': 9855.4, 'cantidad': 4}, 
     {'codigo': '333', 'nombre': 'yogurt 1l', 'precio': 10300.2, 'cantidad': 6}, 
     {'codigo': '666', 'nombre': 'shampoo', 'precio': 19000.0, 'cantidad': 6}]
]

# Lista de diccionarios resultante
lista_diccionarios = []

for sub_lista in lista:
    lista_diccionarios.extend(sub_lista)

print(lista_diccionarios)