import operator
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder
from baseDeDatos import UsarBaseDeDatos
from datetime import datetime, timedelta


Builder.load_file('admin/admin.kv')

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    touch_deselect_last = BooleanProperty(True) 

class SelectableProductoLabel(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_codigo'].text = data['codigo']
		self.ids['_articulo'].text = data['nombre'].capitalize()
		self.ids['_cantidad'].text = str(data['cantidad'])
		self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
		return super(SelectableProductoLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):
		if super(SelectableProductoLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False

class SelectableUsuarioLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
        
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_nombre'].text = data['nombre'].title()
        self.ids['_apellido'].text=data['apellido'].title()
        self.ids['_documento'].text=str(data['documento'])
        self.ids['_username'].text = data['usuario']
        self.ids['_tipo'].text = str(data['tipo'])
        return super(SelectableUsuarioLabel, self).refresh_view_attrs(rv, index, data)
    
    def on_touch_down(self, touch):
        if super(SelectableUsuarioLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
    
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado']=True
        else:
            rv.data[index]['seleccionado']=False
class ItemVentaLabel(RecycleDataViewBehavior, BoxLayout):
    index = None

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_codigo'].text = data['codigo']
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))
        self.ids['_total'].text= str("{:.2f}".format(data['total']))
        return super(ItemVentaLabel, self).refresh_view_attrs(rv, index, data)
    
class SelectableVentaLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_username'].text = data['username']
        self.ids['_CLiente'].text = data['nombreCliente']
        self.ids['_cantidad'].text = str(data['totalProductos'])
        self.ids['_total'].text = '$ '+str("{:.2f}".format(data['total']))
        self.ids['_time'].text = str(data['hora'])
        self.ids['_date'].text = str(data['fecha'])
        return super(SelectableVentaLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableVentaLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado']=True
        else:
            rv.data[index]['seleccionado']=False

class AdminRV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data=[]

    def agregar_datos(self,datos):
        for dato in datos:
            dato['seleccionado']=False
            self.data.append(dato)
        self.refresh_from_data()

    def dato_seleccionado(self):
        indice=-1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice=i
                break
        return indice

class ProductoPopup(Popup):
    def __init__(self, agregar_new, **kwargs):
        super(ProductoPopup, self).__init__(**kwargs)
        self.agregar_new_producto=agregar_new

    def abrir(self, agregar, producto=None):
        if agregar:
            self.ids.producto_info_1.text='Agregar producto nuevo'
            self.ids.producto_codigo.disabled=False
        else:
            self.ids.producto_info_1.text='Modificar producto'
            self.ids.producto_codigo.text=producto['codigo']
            self.ids.producto_codigo.disabled=True
            self.ids.producto_nombre.text=producto['nombre']
            self.ids.producto_cantidad.text=str(producto['cantidad'])
            self.ids.producto_precio.text=str(producto['precio'])
        self.open()
    def verificarInfo(self, productoCodigo, productoNombre, productoCantidad, productoPrecio):
        alerta1='Falta: '
        alerta2=''
        validado={}
        #verificando codigo
        BaseDatos = UsarBaseDeDatos()
        inventario = BaseDatos.ver_inventario()
        codigos_inventario = [producto['codigo'] for producto in inventario]
        if not productoCodigo:
            alerta1+='Codido, '
            validado['codigo']=False
        elif not self.ids.producto_codigo.disabled and productoCodigo in codigos_inventario:
            alerta2 += 'El código ya está en uso. '
            validado['codigo'] = False
        else:
            try:
                numero=int(productoCodigo)
                validado['codigo']=productoCodigo
            except:
                alerta2+='Codigo no valido. '
                validado['codigo']=False
            
        #verificando nombre
        if not productoNombre:
            alerta1+='Nombre, '
            validado['nombre']=False
        else:
            validado['nombre']=productoNombre.lower()
        #verificando cantidad 
        if not productoCantidad:
            alerta1+='cantidad, '
            validado['cantidad']=False
        else:
            try:
                numero=int(productoCantidad)
                validado['cantidad']=productoCantidad
            except:
                alerta2+='cantidad no valido. '
                validado['cantidad']=False
        #verificando precio
        if not productoPrecio:
            alerta1+='Precio. '
            validado['precio']=False
        else:
            try:
                numero=float(productoPrecio)
                validado['precio']=productoPrecio
            except:
                alerta2+='precio no valido. '
                validado['precio']=False

        valores=list(validado.values())
        if False in valores:
            self.ids.no_validado_notif.text=alerta1+alerta2
        else:
            self.ids.no_validado_notif.text='Validado'
            validado['cantidad']=int(validado['cantidad'])
            validado['precio']=float(validado['precio'])
            self.agregar_new_producto(True, validado)
            self.dismiss()

class UsuarioPopup(Popup):
    def __init__(self, _agregar_callback, **kwargs):
        super(UsuarioPopup, self).__init__(**kwargs)
        self.agregar_usuario=_agregar_callback

    def abrir(self, agregar, usuario=None):
        if agregar:
            self.ids.usuario_info_1.text='Agregar Usuario nuevo'
            self.ids.usuario_username.disabled=False
        else:
            self.ids.usuario_info_1.text='Modificar Usuario'
            self.ids.usuario_username.text=usuario['usuario']
            self.ids.usuario_username.disabled=True
            self.ids.usuario_nombre.text=usuario['nombre']
            self.ids.usuario_apellido.text=usuario['apellido']
            self.ids.usuario_documento.text=usuario['documento']
            self.ids.usuario_password.text=usuario['password']
            if usuario['tipo']=='admin':
                self.ids.admin_tipo.state='down'
            else:
                self.ids.trabajador_tipo.state='down'
        self.open()

    def verificar(self, usuario_username, usuario_nombre, usuario_apellido, usuario_documento, usuario_password, admin_tipo, trabajador_tipo):
        alert1 = 'Falta: '
        validado = {}
        if not usuario_username:
            alert1+='Usuario. '
            validado['usuario']=False
        else:
            validado['usuario']=usuario_username

        if not usuario_nombre:
            alert1+='Nombre. '
            validado['nombre']=False
        else:
            validado['nombre']=usuario_nombre.lower()
        
        if not usuario_apellido:
            alert1+='Apellido. '
            validado['apellido']=False
        else:
            validado['apellido']=usuario_apellido.lower()
        
        if not usuario_documento:
            alert1+='Documento. '
            validado['documento']=False
        else:
            validado['documento']=usuario_documento

        if not usuario_password:
            alert1+='Password. '
            validado['password']=False
        else:
            validado['password']=usuario_password

        if admin_tipo=='normal' and trabajador_tipo=='normal':
            alert1+='Tipo. '
            validado['tipo']=False
        else:
            if admin_tipo=='down':
                validado['tipo']='administrador'
            else:
                validado['tipo']='vendedor'

        valores = list(validado.values())

        if False in valores:
            self.ids.no_valid_notif.text=alert1
        else:
            self.ids.no_valid_notif.text=''
            self.agregar_usuario(True, validado)
            self.dismiss()

class VistaProductos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_productos, 1)
    
    def cargar_productos(self, *args):
        baseDatos=UsarBaseDeDatos()
        _productos=baseDatos.ver_inventario()
        self.ids.rv_productos.agregar_datos(_productos)
    def agregar_producto(self, agredar=False, validado=None):
        if agredar:
            lista=list(validado.values())
            BaseDatos=UsarBaseDeDatos()
            BaseDatos.agregar_inventario(lista[0],lista[1],lista[2],lista[3])
            self.ids.rv_productos.data.append(validado)
            self.ids.rv_productos.refresh_from_data()
        else:
            popup=ProductoPopup(self.agregar_producto)
            popup.abrir(True)
    
    def modificar_producto(self,modificar=False, validado=None):
        indice=self.ids.rv_productos.dato_seleccionado()
        if modificar:
            BaseDatos = UsarBaseDeDatos()
            inventario = BaseDatos.ver_inventario()
            producto_existente = next((p for p in inventario if p['codigo'] == validado['codigo']), None)
            if producto_existente:
                producto_existente['nombre'] = validado['nombre']
                producto_existente['precio'] = validado['precio']
                producto_existente['cantidad'] = validado['cantidad']
                BaseDatos.actualizar_productos_en_admin(inventario)
            self.ids.rv_productos.data[indice]['nombre']=validado['nombre']
            self.ids.rv_productos.data[indice]['cantidad']=validado['cantidad']
            self.ids.rv_productos.data[indice]['precio']=validado['precio']
            self.ids.rv_productos.refresh_from_data()
        else:
            if indice>=0:
                producto=self.ids.rv_productos.data[indice]
                popup=ProductoPopup(self.modificar_producto)
                popup.abrir(False, producto)
    
    def eliminar_producto(self):
        indice=self.ids.rv_productos.dato_seleccionado()
        BaseDatos = UsarBaseDeDatos()
        BaseDatos.eliminar_producto_Base_Datos(indice)
        self.ids.rv_productos.data.pop(indice)
        self.ids.rv_productos.refresh_from_data()

    def actualizar_productos(self, productoActualizado):
        for producto_nuevo in productoActualizado:
            for productoViejo in self.ids.rv_productos.data:
                if producto_nuevo['codigo']==productoViejo['codigo']:
                    productoViejo['cantidad']=producto_nuevo['cantidad']
                    break
        self.ids.rv_productos.refresh_from_data()

class VistaUsuarios(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_usuarios, 1)
    
    def cargar_usuarios(self, *args):
        baseDatos=UsarBaseDeDatos()
        _usuarios=baseDatos.ver_usuarios()
        self.ids.rv_usuarios.agregar_datos(_usuarios)

    def agregar_usuario(self, agregar=False, validado=None):
        if agregar:
            lista=list(validado.values())
            BaseDatos=UsarBaseDeDatos()
            BaseDatos.Agregar_Nuevo_usuario(lista[1],lista[2],lista[3],lista[0],lista[4],lista[5])
            self.ids.rv_usuarios.data.append(validado)
            self.ids.rv_usuarios.refresh_from_data()
        else:
            popup=UsuarioPopup(self.agregar_usuario)
            popup.abrir(True)

    def modificar_usuario(self,modificar=False, validado=None):
        indice = self.ids.rv_usuarios.dato_seleccionado()
        if modificar:
            BaseDatos = UsarBaseDeDatos()
            _usuarios = BaseDatos.ver_usuarios()
            usuario_modificado = next((p for p in _usuarios if p['usuario'] == validado['usuario']), None)
            if usuario_modificado:
                usuario_modificado['nombre'] = validado['nombre']
                usuario_modificado['apellido'] = validado['apellido']
                usuario_modificado['documento'] = validado['documento']
                usuario_modificado['password'] = validado['password']
                usuario_modificado['tipo'] = validado['tipo']
                BaseDatos.modificar_usuario_Base_Datos(_usuarios)
            
            self.ids.rv_usuarios.data[indice]['nombre']=validado['nombre']
            self.ids.rv_usuarios.data[indice]['apellido']=validado['apellido']
            self.ids.rv_usuarios.data[indice]['documento']=validado['documento']
            self.ids.rv_usuarios.data[indice]['tipo']=validado['tipo']
            self.ids.rv_usuarios.data[indice]['password']=validado['password']
            self.ids.rv_usuarios.refresh_from_data()
        else:
            if indice>=0:
                usuario = self.ids.rv_usuarios.data[indice]
                popup = UsuarioPopup(self.modificar_usuario)
                popup.abrir(False, usuario)
    
    def eliminar_usuario(self):
        indice=self.ids.rv_usuarios.dato_seleccionado()
        BaseDatos = UsarBaseDeDatos()
        BaseDatos.eliminar_usuario_Base_Datos(indice)
        self.ids.rv_usuarios.data.pop(indice)
        self.ids.rv_usuarios.refresh_from_data()

class InfoVentaPopup(Popup):
    def __init__(self, venta, **kwargs):
        super(InfoVentaPopup, self).__init__(**kwargs)
        self.venta=venta
    
    def mostrar(self):
        self.open()
        total_productos=0
        total_Pagado=0.0
        ventasPorProducto=[]
        for articulo in self.venta:
            total_productos+=articulo['cantidad']
            total_Pagado+=articulo['cantidad']*articulo['precio']
            ventasPorProducto.append({'codigo':articulo['codigo'],'nombre':articulo['nombre'],'cantidad':articulo['cantidad'],'precio':articulo['precio'],'total':articulo['cantidad']*articulo['precio']})
        self.ids.total_items.text=str(total_productos)
        self.ids.total_dinero.text=str(total_Pagado)
        self.ids.info_rv.agregar_datos(ventasPorProducto)

class VistaVentas(Screen):
    productos_actuales=[]
    fecha_i=None
    fecha_f=None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Ahora=datetime.now()

    def reportes(self):
        pop=reportePopup()
        pop.abrir(self.fecha_i, self.fecha_f)

    def mas_info(self):
        indice=self.ids.ventas_rv.dato_seleccionado()
        if indice>=0:
            venta=self.productos_actuales[indice]
            pop=InfoVentaPopup(venta)
            pop.mostrar()

    def cargar_venta(self, choice='Default'):
        self.productos_actuales=[]
        validad_input=True
        fecha_inicio = datetime.strptime('01/01/00','%d/%m/%y')
        fecha_fin = datetime.strptime('31/12/2099','%d/%m/%Y')

        _ventas=[]
        TotalDeLasVentas=0
        self.ids.ventas_rv.data=[]
        self.ids.date_id.text=''
        if choice=='Default':
            fecha_inicio=datetime.today().date()
            fecha_fin=fecha_inicio+timedelta(days=1)
            self.ids.date_id.text=str(fecha_inicio.strftime("%d-%m-%y"))
        
        elif choice=='Date':
            date=self.ids.single_date.text
            try:
                fecha_elegida=datetime.strptime(date, '%d-%m-%y')
            except:
                validad_input=False
            
            if validad_input:
                fecha_inicio=fecha_elegida
                fecha_fin=datetime.strptime(date, '%d-%m-%y')
                self.ids.date_id.text=fecha_elegida.strftime('%d-%m-%y')
        else:
            if self.ids.initial_date.text:
                initial_date=self.ids.initial_date.text
                try:
                    fecha_inicio=datetime.strptime(initial_date, '%d-%m-%y')
                except:
                    validad_input=False
            
            if  self.ids.last_date.text:
                last_date=self.ids.last_date.text
                try:
                    fecha_fin=datetime.strptime(last_date, '%d-%m-%y')
                except:
                    validad_input=False
                    
            if validad_input:
                self.ids.date_id.text = fecha_inicio.strftime('%d-%m-%y') + " - " + fecha_fin.strftime('%d-%m-%y')
            
        if validad_input:
            fecha_inicio_b = fecha_inicio.strftime("%d-%m-%y")
            fecha_fin_b = fecha_fin.strftime("%d-%m-%y")
            self.fecha_i=fecha_inicio.strftime("%d-%m-%y")
            self.fecha_f=fecha_fin.strftime("%d-%m-%y")
            baseDatos=UsarBaseDeDatos()
            ventas=baseDatos.obtener_ventas(fecha_inicio_b, fecha_fin_b)
            if ventas:
                for venta in ventas:
                    TotalDeLasVentas+=venta['total_venta']
                    _ventas.append({
                                    'username': venta['usuario'],
                                    'nombreCliente': venta['nombreCliente'],
                                    'documentoCliente': venta['documentoCliente'],
                                    'totalProductos': venta['totalProductos'],
                                    'total': venta['total_venta'],
                                    'fecha': venta['fecha'],
                                    'hora': venta['hora']
                                    })
                    self.productos_actuales.append(venta['productos'])
                self.ids.ventas_rv.agregar_datos(_ventas)
        self.ids.TotalVentasVendidas.text="$ "+str(TotalDeLasVentas)
        self.ids.single_date.text=''
        self.ids.initial_date.text=''
        self.ids.last_date.text=''       
        
class reportePopup(Popup):
    def __init__(self, **kwargs):
        super(reportePopup, self).__init__(**kwargs)
    
    def abrir(self, fecha_i, fecha_f):
        paso=True
        try:
            fecha_inicio_b = fecha_i
            fecha_fin_b = fecha_f
        except:
            paso=False
        #Promedio de ventas
        if paso:
            baseDatos=UsarBaseDeDatos()
            Ventas=baseDatos.obtener_ventas(fecha_inicio_b,fecha_fin_b)
            promedio=0
            #para vendedor mas ixitoso
            vendedor_exitoso=None
            productosVendidos=None
            ToalVendido=None
            total_ventas = sum(venta['total_venta'] for venta in Ventas)
            cantidad_ventas = sum(venta['totalProductos'] for venta in Ventas)

            if cantidad_ventas > 0:
                promedio = total_ventas / cantidad_ventas
            else:
                promedio=0

            #vendedor mas IXITOSO
            if Ventas:
                vendedores = {}
                for venta in Ventas:
                    vendedor = venta['usuario']
                    total_venta = venta['total_venta']
                    total_productos = venta['totalProductos']
                    if vendedor in vendedores:
                        vendedores[vendedor]['total_venta'] += total_venta
                        vendedores[vendedor]['totalProductos'] += total_productos
                    else:
                        vendedores[vendedor] = {'total_venta': total_venta, 'totalProductos': total_productos}

                try:
                    vendedor_exitoso = max(vendedores.items(), key=operator.itemgetter(1))[0]
                    ToalVendido = vendedores[vendedor_exitoso]['total_venta']
                    productosVendidos = vendedores[vendedor_exitoso]['totalProductos']
                except:
                    vendedor_exitoso = max(vendedores.items(), key=lambda x: x[1]['total_venta'])[0]
                    ToalVendido = vendedores[vendedor_exitoso]['total_venta']
                    productosVendidos = vendedores[vendedor_exitoso]['totalProductos']
                
                if vendedores:
                    vendedor_menos_exitoso = min(vendedores.items(), key=lambda x: x[1]['total_venta'])
                    nombre_vendedor_menos_exitoso = vendedor_menos_exitoso[0]
                    if nombre_vendedor_menos_exitoso != vendedor_exitoso:
                        total_ventas_vendedor_menos_exitoso = vendedor_menos_exitoso[1]['total_venta']
                        total_productos_vendedor_menos_exitoso = vendedor_menos_exitoso[1]['totalProductos']
                    else:
                        nombre_vendedor_menos_exitoso=''
                        total_ventas_vendedor_menos_exitoso=''
                        total_productos_vendedor_menos_exitoso=''
            
            #Cliente mas frecuente en la tienda
            if Ventas:
                clientes = {}
                for venta in Ventas:
                    documento_cliente = venta['documentoCliente']
                    nombre_cliente = venta['nombreCliente']
                    total_venta = venta['total_venta']
                    if documento_cliente in clientes:
                        clientes[documento_cliente]['total_venta'] += total_venta
                        clientes[documento_cliente]['cantidad_compras'] += 1
                    else:
                        clientes[documento_cliente] = {'nombre_cliente': nombre_cliente, 'total_venta': total_venta, 'cantidad_compras': 1}
                try:
                    cliente_mas_compras = max(clientes.items(), key=lambda x: x[1]['cantidad_compras'])
                    documento_cliente = cliente_mas_compras[0]
                    nombre_cliente = cliente_mas_compras[1]['nombre_cliente']
                    cantidad_compras = cliente_mas_compras[1]['cantidad_compras']
                    total_ventas = cliente_mas_compras[1]['total_venta']
                except:
                    cliente_mas_compras = max(clientes.items(), key=lambda x: x[1]['cantidad_compras'])
                    documento_cliente = cliente_mas_compras[0]
                    nombre_cliente = cliente_mas_compras[1]['nombre_cliente']
                    cantidad_compras = cliente_mas_compras[1]['cantidad_compras']
                    total_ventas = cliente_mas_compras[1]['total_venta']
            
            if Ventas:
                productos = {}
                for venta in Ventas:
                    for producto in venta['productos']:
                        nombre_producto = producto['nombre']
                        cantidad_vendida = producto['cantidad']
                        if nombre_producto in productos:
                            productos[nombre_producto] += cantidad_vendida
                        else:
                            productos[nombre_producto] = cantidad_vendida

                if productos:
                    producto_mas_vendido = max(productos.items(), key=lambda x: x[1])
                    nombre_producto_mas_vendido = producto_mas_vendido[0]
                    cantidad_vendida_producto_mas_vendido = producto_mas_vendido[1]

            self.ids._totalVentasPrecio.text=str(total_ventas)
            self.ids._TotalProductos.text=str(cantidad_ventas)
            self.ids._promedioVentas.text="$ "+str("{:.2f}".format(promedio))
            self.ids._vendedorExitoso.text=str(vendedor_exitoso)
            self.ids._totalProductos.text=str(productosVendidos)
            self.ids._totalVenta.text="$ "+str(ToalVendido)
            self.ids._totalProductos.text=str(productosVendidos)
            self.ids._ClienteFrecuente.text=str(nombre_cliente)
            self.ids._documentocliente.text=str(documento_cliente)
            self.ids._totalProductosCliente.text=str(cantidad_compras)
            self.ids._productoMasVEndido.text=str(nombre_producto_mas_vendido)
            self.ids._productoMasVEndidocantidad.text=str(cantidad_vendida_producto_mas_vendido)
            self.ids._vendedorBajoNombre.text=str(nombre_vendedor_menos_exitoso)
            self.ids._vendedorBajoVentas.text=str(total_productos_vendedor_menos_exitoso)
            self.ids._vendedorBajoTotal.text=str(total_ventas_vendedor_menos_exitoso)
            self.ids._totalCompraCliente.text="$ "+str(total_ventas)
        self.open()
            

class CustomDropDown(DropDown):
	def __init__(self, cambiar_callback, **kwargs):
		self._succ_cb = cambiar_callback
		super(CustomDropDown, self).__init__(**kwargs)

	def vista(self, vista):
		if callable(self._succ_cb):
			self._succ_cb(True, vista)

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vista_actual='Productos'
        self.vista_manager=self.ids.vista_manager
        self.dropdown = CustomDropDown(self.cambiar_vista)
        self.ids.cambiar_vista.bind(on_release=self.dropdown.open)

    def cambiar_vista(self, cambio=False, vista=None):
        if cambio:
            self.vista_actual=vista
            self.vista_manager.current=self.vista_actual
            self.dropdown.dismiss()

    def salir(self):
        self.parent.parent.current='scrn_singin'

    def ventas(self):
        self.parent.parent.current='scrn_ventas'
    
    def actualizar_productos(self, NuevaCantidad):
        self.ids.vista_productos.actualizar_productos(NuevaCantidad)


class AdminApp(App):
    def build(self):
        return AdminWindow()
    
if __name__=="__main__":
    AdminApp().run()