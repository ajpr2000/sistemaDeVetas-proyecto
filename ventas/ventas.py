from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.lang import Builder
from baseDeDatos import UsarBaseDeDatos

Builder.load_file('ventas/ventas.kv')

baseDatos=UsarBaseDeDatos()
inventario=baseDatos.ver_inventario()
"""inventario=[
 	{'codigo': '111', 'nombre': 'leche 1L', 'precio': 20.0, 'cantidad': 20},
 	{'codigo': '222', 'nombre': 'cereal 500g', 'precio': 50.5, 'cantidad': 15}, 
 	{'codigo': '333', 'nombre': 'yogurt 1L', 'precio': 25.0, 'cantidad': 10},
 	{'codigo': '444', 'nombre': 'helado 2L', 'precio': 80.0, 'cantidad': 20},
 	{'codigo': '555', 'nombre': 'alimento para perro 20kg', 'precio': 750.0, 'cantidad': 5},
 	{'codigo': '666', 'nombre': 'shampoo', 'precio': 100.0, 'cantidad': 25},
 	{'codigo': '777', 'nombre': 'papel higiénico 4 rollos', 'precio': 35.5, 'cantidad': 30},
 	{'codigo': '888', 'nombre': 'jabón para trastes', 'precio': 65.0, 'cantidad': 5},
 	{'codigo': '999', 'nombre': 'refresco 600ml', 'precio': 15.0, 'cantidad': 10}
 ]
"""
#CODIGO SACADO DE LA PAGINA DE KIVY PARA PORDER MOSTRAS LOS PRODUCTOS EN PANTALLA
#link: https://kivy.org/doc/stable/api-kivy.uix.recycleview.html

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last=BooleanProperty(True)

class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad_carrito'])
        self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))
        self.ids['_precio'].text = str("{:.2f}".format(data['precio_total']))
        
        return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado']=True
        else:
            rv.data[index]['seleccionado']=False

class SelectableBoxLayoutPopup(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['_codigo'].text=data['codigo']
        self.ids['_articulo'].text=data['nombre'].capitalize()
        self.ids['_cantidad'].text=str(data['cantidad'])
        self.ids['_precio'].text=str("{:.2f}").format(data['precio'])
        
        return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado']=True
        else:
            rv.data[index]['seleccionado']=False
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.cambiar_producto=None
        
    def agregar_articulo(self, articulo):
        articulo['seleccionado']=False
        indice=-1
        if self.data:
            for i in range(len(self.data)):
                if articulo['codigo']==self.data[i]['codigo']:
                    indice=i
            if indice>=0:
                self.data[indice]['cantidad_carrito']+=1
                self.data[indice]['precio_total']=self.data[indice]['precio']*self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                self.data.append(articulo)
        else:
            self.data.append(articulo)
    def eliminar_articulo(self):
        indice=self.articulo_seleccionado()
        precio=0
        if indice>=0:
            self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            precio=self.data[indice]['precio_total']
            self.data.pop(indice)
            self.refresh_from_data()
        return precio
    
    def modificar_articulo(self):
        indice=self.articulo_seleccionado()
        if indice>=0:
            popup=CambiarCantidadPopup(self.data[indice],self.actualizar_articulo)
            popup.open()

    def actualizar_articulo(self, valor):
        indice=self.articulo_seleccionado()
        if indice>=0:
            if valor==0:
                self.data.pop(indice)
                self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            else:
                self.data[indice]['cantidad_carrito']=valor
                self.data[indice]['precio_total']=self.data[indice]['precio']*valor
            self.refresh_from_data()
            nuevo_total=0
            for data in self.data:
                nuevo_total+=data['precio_total']
            self.cambiar_producto(False, nuevo_total) #

    def articulo_seleccionado(self):
        indice=-1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice=i
                break
        return indice

class ProductoPorNombrePopup(Popup):
    def __init__(self, input_nombre, agregar_producto_Popup, **kwargs):
        super(ProductoPorNombrePopup, self).__init__(**kwargs)
        self.input_nombre=input_nombre
        self.agregar_producto=agregar_producto_Popup
    def mostar_articulo(self):
        for nombre in inventario:
            self.open()
            if nombre['nombre'].lower().find(self.input_nombre)>=0:
                producto={'codigo': nombre['codigo'], 'nombre': nombre['nombre'], 'precio': nombre['precio'], 'cantidad': nombre['cantidad']}
                self.ids.rvs.agregar_articulo(producto)
    
    def selecionar_articulo(self):
        indice=self.ids.rvs.articulo_seleccionado()
        if indice>=0:
            _articulo=self.ids.rvs.data[indice]
            articulo={}
            articulo['codigo']=_articulo['codigo']
            articulo['nombre']=_articulo['nombre']
            articulo['precio']=_articulo['precio']
            articulo['cantidad_carrito']=1
            articulo['cantidad_inventario']=_articulo['cantidad']
            articulo['precio_total']=_articulo['precio']
            if callable(self.agregar_producto):
                self.agregar_producto(articulo)
            self.dismiss()

class CambiarCantidadPopup(Popup):
    def __init__(self, data, actualizar_articulo_popup, **kwargs):
        super(CambiarCantidadPopup, self).__init__(**kwargs)
        self.data=data
        self.actualizar_articulo=actualizar_articulo_popup
        self.ids.info_nueva_cant_one.text="Producto: "+self.data['nombre'].capitalize()
        self.ids.info_nueva_cant_two.text="Cantidad: "+str(self.data['cantidad_carrito'])
    
    def validar_info(self, texto_input):
        try:
            nueva_cantidad=int(texto_input)
            self.ids.notificacion_no_valida.text=''
            self.actualizar_articulo(nueva_cantidad)
            self.dismiss()
        except:
            self.ids.notificacion_no_valida.text='Cantidad no validad'

class PagarPopup(Popup):
    def __init__(self, valor, pagadoPopup, mostrar_vueltoPopup, datos_clientes_popup, **kwargs):
        super(PagarPopup, self).__init__(**kwargs)
        self.total=valor
        self.cambio=0.0
        self.nombreDelCliente=""
        self.documentoDelCliente=""
        self.pagado=pagadoPopup
        self.mostrar_vuelto=mostrar_vueltoPopup
        self.datos_clientes=datos_clientes_popup
        self.ids.total.text="{:.2f}".format(self.total)
        self.ids.boton_pagar.bind(on_release=self.dismiss)
        
    def mostrar_cambios(self):
        valorVuelto=self.ids.recibido.text
        try:
            self.cambio=float(valorVuelto)-float(self.total)
            if self.cambio>=0:
                self.ids.cambio.text="{:.2f}".format(self.cambio)
                self.ids.boton_pagar.disabled=False
            else:
                self.ids.cambio.text="PAGO MENOR A TOTAL A PAGAR"
        except:
            self.ids.cambio.text="VALOR NO VALIDO"
    def datosCliente(self):
        self.nombreDelCliente=self.ids.nombreCliente.text
        self.documentoDelCliente=self.ids.documentoCliente.text

    def terminar_pago(self):
        self.datos_clientes(self.nombreDelCliente,self.documentoDelCliente)
        self.pagado()
        self.mostrar_vuelto(self.cambio)
        

class NuevaCompraPopup(Popup):
    def __init__(self, nueva_compra_popup, **kwargs):
        super(NuevaCompraPopup, self).__init__(**kwargs)
        self.nueva_compra=nueva_compra_popup
        self.ids.nueva_compra.bind(on_release=self.dismiss)


class Ventaswindow(BoxLayout):
    usuario=None
    nombreCliente=""
    documentoCliente=""
    def __init__(self, actualizar_productos_,**kwargs):
        super().__init__(**kwargs)
        self.total=0.0
        self.ids.rvs.cambiar_producto=self.cambiar_producto
        self.actualizar_productos=actualizar_productos_
        #PARA VER EL TIEMPO Y FECHA
        self.Ahora=datetime.now()
        self.ids.fecha.text=self.Ahora.strftime("%d/%m/%y")
        Clock.schedule_interval(self.actualizar_tiempo, 1)
        self.ids.hora.text=self.Ahora.strftime("%H:%M:%S")
    
    def agregar_producto_codigo(self, codigo):
        self.ids.notificacion_falla.text=' '
        for producto in inventario:
            if codigo==producto['codigo']:
                print("encontrado: ", producto)
                articulo={}
                articulo['codigo']=producto['codigo']
                articulo['nombre']=producto['nombre']
                articulo['precio']=producto['precio']
                articulo['cantidad_carrito']=1
                articulo['cantidad_inventario']=producto['cantidad']
                articulo['precio_total']=producto['precio']
                self.agregar_producto(articulo)
                self.ids.buscar_codigo.text=''       
                break

    def agregar_producto_nombre(self, nombre):
        self.ids.buscar_nombre.text=''
        self.ids.notificacion_falla.text=' '
        popup=ProductoPorNombrePopup(nombre, self.agregar_producto)
        popup.mostar_articulo()

    def agregar_producto(self,articulo):
        self.total+=articulo['precio']
        self.ids.sub_total.text='$ '+ "{:.2f}".format(self.total)
        self.ids.rvs.agregar_articulo(articulo)
    
    def eliminer_producto(self):
        menos_precio=self.ids.rvs.eliminar_articulo()
        self.total-=menos_precio
        self.ids.sub_total.text='$ '+ "{:.2f}".format(self.total)
    
    def cambiar_producto(self, cambio=True, Nuevo_total=None):
        if cambio:
            self.ids.rvs.modificar_articulo()
        else:
            self.total=Nuevo_total
            self.ids.sub_total.text='$ '+ "{:.2f}".format(self.total)

    def actualizar_tiempo(self, *args):
        self.Ahora=self.Ahora+timedelta(seconds=1)
        self.ids.hora.text=self.Ahora.strftime("%H:%M:%S")

    def pagar(self):
        if self.ids.rvs.data:
            popup=PagarPopup(self.total, self.pagado, self.mostrar_vuelto, self.datos_clientes)
            popup.open()
        else:
            self.ids.notificacion_falla.text='AGREGE ALGO AL CARRITO'

    def pagado(self):
        self.ids.notificacion_exito.text='Pago realizado exitosamente'
        self.ids.notificacion_falla.text=' '
        self.ids.total.text='$ '+ "{:.2f}".format(self.total)
        self.ids.buscar_codigo.disabled=True
        self.ids.buscar_nombre.disabled=True
        self.ids.pagar.disabled=True
        nueva_cantidad=[]
        guardar_venta=[]
        actualizar_admin=None
        for producto in self.ids.rvs.data:
            cantidad=int(producto['cantidad_inventario'])-producto['cantidad_carrito']
            if cantidad>=0:
                nueva_cantidad.append({'codigo': producto['codigo'], 'cantidad':cantidad})
            else:
                nueva_cantidad.append({'codigo': producto['codigo'], 'cantidad': 0})
            actualizar_admin=nueva_cantidad
            guardar_venta.append({
            'codigo': producto['codigo'],
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': producto['cantidad_carrito']
        })

        baseDatos.guardar_ventas(guardar_venta, self.total ,self.nombreCliente, self.documentoCliente, self.usuario, self.Ahora.strftime("%d-%m-%y"), self.Ahora.strftime("%H:%M:%S"))
        #actualizar base de datos con la nueva cantidad
        baseDatos.actualizar_cantidades(nueva_cantidad)
        self.actualizar_productos(actualizar_admin)
        

    def mostrar_vuelto(self, valor):
        vueltoR=float(valor)
        self.ids.vuelto.text='$ '+ "{:.2f}".format(vueltoR)

    def datos_clientes(self, nombre, documento):
        self.nombreCliente=nombre
        self.documentoCliente=documento
        print(self.nombreCliente, self.documentoCliente)

    
    def nueva_compra(self, llamada_popup=False):
        if llamada_popup:
            self.ids.rvs.data=[]
            self.total=0.0
            self.ids.sub_total.text='$ 0.0'
            self.ids.vuelto.text='$ 0.0'
            self.ids.total.text='$ 0.0'
            self.ids.notificacion_exito.text=' '
            self.ids.notificacion_falla.text=' '
            self.ids.buscar_codigo.disabled=False
            self.ids.buscar_nombre.disabled=False
            self.ids.pagar.disabled=False
            self.ids.rvs.refresh_from_data()
        elif len(self.ids.rvs.data):
            popup=NuevaCompraPopup(self.nueva_compra)
            popup.open()
        else:
            self.ids.notificacion_falla.text='EL SISTEMA YA VACIO'

    def admin(self):
        self.parent.parent.current='scrn_admin'
        
    def signout(self):
        if self.ids.rvs.data:
            print("DEBE CERRAR LA VENTA")
            self.ids.notificacion_falla.text="Pago pendiente"
        else:
            self.parent.parent.current='scrn_singin'
        print("salir presionado")

    def poner_usuario(self, usuario):
        self.ids.usuario_label.text="Usuario: "+str(usuario['nombre'])+" "+str(usuario['apellido'])
        self.ids.tipo_label.text=str(usuario['tipo']).upper()
        self.usuario=usuario['username']
        if usuario['tipo']=='vendedor':
            self.ids.admin_boton.disabled=True
            self.ids.admin_boton.text=''
            self.ids.admin_boton.opacity=0
        else: 
            self.ids.admin_boton.disabled=False
            self.ids.admin_boton.text='Admin'
            self.ids.admin_boton.opacity=1
class VentasApp(App):
    def build(self):
        return Ventaswindow()
      
if __name__=='__main__':
    VentasApp().run()