from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from baseDeDatos import UsarBaseDeDatos

Builder.load_file('signin/signin.kv')

class SigninWindow(BoxLayout):
    def __init__(self, poner_usuario_en_ventas,**kwargs):
        super().__init__(**kwargs)
        self.poner_usuario=poner_usuario_en_ventas
    def verificar_usuario(self, username, password):
        baseDatos=UsarBaseDeDatos()
        users=baseDatos.ver_usuarios()
        if username=='' or password=='':
            self.ids.signin_notificacion.text='Falta Usuario o Contraseña '
        else:
            usuario={}
            for user in users:
                if user['usuario']==username:
                    usuario['nombre']=user['nombre']
                    usuario['apellido']=user['apellido']
                    usuario['username']=user['usuario']
                    usuario['password']=user['password']
                    usuario['tipo']=user['tipo']
                    break
            if usuario:
                if usuario['password']==password:
                    self.ids.username.text=''
                    self.ids.password.text=''
                    self.ids.signin_notificacion.text=''
                    if usuario['tipo']=='vendedor':
                        self.parent.parent.current='scrn_ventas'
                    else:
                        self.parent.parent.current='scrn_admin'
                    self.poner_usuario(usuario)
                else:
                    self.ids.signin_notificacion.text='contraseña incorrecta'
            else:
                self.ids.signin_notificacion.text='Usuario o contraseña incorrecta'

class SigninApp(App):
    def build(self):
        return SigninWindow()
    
if __name__=="__main__":
    SigninApp().run()