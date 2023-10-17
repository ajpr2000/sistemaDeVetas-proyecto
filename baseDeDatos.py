class Persona():
    def __init__(self):
        self.nombre=""
        self.apellido=""

    def SetNombre(self,x:str):
        self.nombre=x
    def GetNombre(self):
        return self.nombre

    def SetApellido(self,x:str):
        self.apellido=x
    def GetApellido(self):
        return self.apellido
    
class Cliente(Persona):
    def __init__(self):
        super().__init__()
        self.documento=0

    def SetDocumento(self,x:int):
        self.documento=x
    def GetDocumento(self):
        return self.documento
    
class Empleado(Cliente):
    def __init__(self):
        super().__init__()
        self.usuario=""
        self.password=""

    def SetUsuario(self,x:str):
        self.usuario=x
    def GetUsuario(self):
        return self.usuario
    def SetPassword(self,x:str):
        self.password=x
    def GetPassword(self):
        return self.password
    

class UsarBaseDeDatos():
    def __init__(self):
        self.ruta_inventario="BaseDeDatosTienda/inventario.txt"
        self.ruta_ventas="BaseDeDatosTienda/ventas.txt"
        self.ruta_usuarios="BaseDeDatosTienda/usuarios.txt"

    #para agregar nuevo producto al inentario
    def agregar_inventario(self, codigo, nombre, precio, cantida):
        with open(self.ruta_inventario, mode='a') as archivo:
            linea = f"{codigo}\t{nombre}\t{precio}\t{cantida}\n"
            archivo.write(linea)
            print("guardado finalizado")
    
    #para ver el inventario completo 
    def ver_inventario(self):
        with open(self.ruta_inventario, mode="r") as archivo:
            productos=[]
            for linea in archivo:
                codigo, nombre, precio, cantidad=linea.strip().split('\t')
                productos.append({"codigo": codigo, "nombre": nombre, "precio": float(precio), "cantidad":cantidad})
            print("conección exitosa a la Base De Datos 'INVENTARIO'")
            return productos
        
    #usado solo para modificar la cantidad del un producto
    def actualizar_cantidades(self, nuevas_cantidades):
        inventario = self.ver_inventario() 
        for cantidad in nuevas_cantidades:
            producto = next((p for p in inventario if p['codigo'] == cantidad['codigo']), None)
            
            if producto:
                producto['cantidad'] = cantidad['cantidad']
        
        # Guardar los cambios en el archivo del inventario
        with open(self.ruta_inventario, mode='w') as archivo:
            for producto in inventario:
                linea = f"{producto['codigo']}\t{producto['nombre']}\t{producto['precio']}\t{producto['cantidad']}\n"
                archivo.write(linea)
            print("PRODUCTO modificado en la Base De Datos")
    
    #usado para modificar nombre cantidad y precio a un producto ya existente
    def actualizar_productos_en_admin(self, nuevos_productos):
        inventario = self.ver_inventario()
    
        for nuevo_producto in nuevos_productos:
            producto = next((p for p in inventario if p['codigo'] == nuevo_producto['codigo']), None)
            
            if producto:
                producto['nombre'] = nuevo_producto['nombre']
                producto['cantidad'] = nuevo_producto['cantidad']
                producto['precio'] = nuevo_producto['precio']
        
        # Guardar los cambios en el archivo del inventario
        with open(self.ruta_inventario, mode='w') as archivo:
            for producto in inventario:
                linea = f"{producto['codigo']}\t{producto['nombre']}\t{producto['precio']}\t{producto['cantidad']}\n"
                archivo.write(linea)
            print("PRODUCTO modificado en la Base De Datos")

    #usado para eliminar un producto de la base de datos
    def eliminar_producto_Base_Datos(self, indice):
        inventario = self.ver_inventario()
        if 0 <= indice < len(inventario):
            producto = inventario.pop(indice)
            # Guardar los cambios en el archivo del inventario
            with open(self.ruta_inventario, mode='w') as archivo:
                for producto in inventario:
                    linea = f"{producto['codigo']}\t{producto['nombre']}\t{producto['precio']}\t{producto['cantidad']}\n"
                    archivo.write(linea)
            print("Producto eliminado con éxito.")


    #usado para agregar las ventas a la base de datos
    def guardar_ventas(self, productos, total, nombreCliente, documentoCliente, usuario, fecha, hora):
        cliente = Cliente()
        cliente.SetNombre(nombreCliente)
        cliente.SetDocumento(documentoCliente)

        with open(self.ruta_ventas, mode='a') as archivo:
            for producto in productos:
                linea = f"{producto['codigo']}\t{producto['nombre']}\t{producto['precio']}\t{producto['cantidad']}\t{total}\t{cliente.GetNombre()}\t{cliente.GetDocumento()}\t{usuario}\t{fecha}\t{hora}\n"
                archivo.write(linea)

        print("Venta guardada Exitosamente")

    def obtener_ventas(self, fecha_inicio, fecha_fin):
        ventas = []

        with open(self.ruta_ventas, mode='r') as archivo:
            for linea in archivo:
                datos = linea.strip().split('\t')

                codigo = datos[0]
                nombre = datos[1]
                precio = float(datos[2])
                cantidad = int(datos[3])
                total = float(datos[4])
                nombreCliente = datos[5]
                documentoCliente = datos[6]
                usuario = datos[7]
                fecha = datos[8]
                hora = datos[9]

                # Verificar si la fecha coincide con la fecha de búsqueda
                if fecha >= fecha_inicio and fecha <= fecha_fin:
                    # Verificar si ya existe una venta para el mismo cliente, vendedor y fecha
                    venta_existente = None
                    for venta in ventas:
                        if (venta['nombreCliente'] == nombreCliente and venta['usuario'] == usuario and venta['fecha'] == fecha):
                            venta_existente = venta
                            break

                    # Si existe una venta para el mismo cliente, vendedor y fecha, se agrega el producto a esa venta [{}][]
                    if venta_existente:
                        venta_existente['productos'].append({
                            'codigo': codigo,
                            'nombre': nombre,
                            'precio': precio,
                            'cantidad': cantidad})
                        venta_existente['total_venta'] += total
                        venta_existente['totalProductos'] += cantidad
                    # Si no existe una venta para el mismo cliente, vendedor y fecha, se crea una nueva venta
                    else:
                        venta_nueva = {
                            'nombreCliente': nombreCliente,
                            'documentoCliente': documentoCliente,
                            'usuario': usuario,
                            'fecha': fecha,
                            'hora': hora,
                            'productos': [{
                                'codigo': codigo,
                                'nombre': nombre,
                                'precio': precio,
                                'cantidad': cantidad
                            }],
                            'total_venta': total,  # Se agrega el valor total de la venta
                            'totalProductos': cantidad
                        }
                        ventas.append(venta_nueva)
        return ventas


    #usado para agregar nuevo usuario 
    def Agregar_Nuevo_usuario(self, nombreInput, apellidoInput, documentoInput, usuarioInput, passwordInput,tipo):
        empleado=Empleado()
        empleado.SetNombre(nombreInput)
        empleado.SetApellido(apellidoInput)
        empleado.SetDocumento(documentoInput)
        empleado.SetUsuario(usuarioInput)
        empleado.SetPassword(passwordInput)

        with open(self.ruta_usuarios, mode="a") as archivo:
            linea = f"{empleado.GetNombre()}\t{empleado.GetApellido()}\t{empleado.GetDocumento()}\t{empleado.GetUsuario()}\t{empleado.GetPassword()}\t{tipo}\n"
            archivo.write(linea)
        print("USUARIO guardado en la Base De Datos")
    
    #para ver todos los usuarios
    def ver_usuarios(self):
        with open(self.ruta_usuarios, mode="r") as archivo:
            users=[]
            for linea in archivo:
                nombre, apellido, documento, usuario, password, tipo=linea.strip().split('\t')
                users.append({"nombre": nombre, "apellido": apellido, "documento": documento, "usuario":usuario, "password": password, "tipo": tipo})
            print("conección exitosa a la Base De Datos 'USUARIOS'")
            return users


    def modificar_usuario_Base_Datos(self, nuevo_usuario):
        usuarios=self.ver_usuarios()

        for nuevo_usuario in nuevo_usuario:
            usuario = next((p for p in usuarios if p['usuario'] == nuevo_usuario['usuario']), None)
            
            if usuario:
                usuario['nombre'] = nuevo_usuario['nombre']
                usuario['apellido'] = nuevo_usuario['apellido']
                usuario['documento'] = nuevo_usuario['documento']
                usuario['password'] = nuevo_usuario['password']
                usuario['tipo'] = nuevo_usuario['tipo']
                
        with open(self.ruta_usuarios, mode='w') as archivo:
            for usuario in usuarios:
                linea = f"{usuario['nombre']}\t{usuario['apellido']}\t{usuario['documento']}\t{usuario['usuario']}\t{usuario['password']}\t{usuario['tipo']}\n"
                archivo.write(linea)
        print("Usuario modificado con éxito.")

    def eliminar_usuario_Base_Datos(self, indice):
        usuarios = self.ver_usuarios()
        if 0 <= indice < len(usuarios):
            usuario = usuarios.pop(indice)
            # Guardar los cambios en el archivo del usuario
            with open(self.ruta_usuarios, mode='w') as archivo:
                for usuario in usuarios:
                    linea = f"{usuario['nombre']}\t{usuario['apellido']}\t{usuario['documento']}\t{usuario['usuario']}\t{usuario['password']}\t{usuario['tipo']}\n"
                    archivo.write(linea)
            print("Usuario eliminado con éxito.")