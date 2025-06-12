from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
import json
import os

# Función de respaldo SUPER SIMPLE
def obtener_texto(key):
    textos = {
        'crear_usuario': 'Crear Usuario',
        'nombre': 'Nombre',
        'apellido': 'Apellido',
        'telefono': 'Teléfono',
        'correo': 'Correo',
        'usuario': 'Usuario',
        'contrasena': 'Contraseña',
        'aceptar': 'Guardar',
        'volver': 'Volver'
    }
    return textos.get(key, key)

class PantallaCrearUsuario(Screen):
    def __init__(self, **kwargs):
        print("🚀 === INICIO PantallaCrearUsuario ===")
        
        # Extraer callbacks
        self.guardar_callback = kwargs.pop('guardar_callback', None)
        self.volver_callback = kwargs.pop('volver_callback', None)
        
        super().__init__(**kwargs)
        self.name = 'crear_usuario'
        
        print(f"📋 Callbacks configurados:")
        print(f"   - guardar_callback: {type(self.guardar_callback)}")
        print(f"   - volver_callback: {type(self.volver_callback)}")
        
        # Crear interfaz INMEDIATAMENTE
        print("🔧 Llamando crear_interfaz()...")
        self.crear_interfaz()
        print("✅ crear_interfaz() completado")
    
    def crear_interfaz(self):
        print("🔧 === CREANDO INTERFAZ ===")
        
        # Limpiar todo
        self.clear_widgets()
        
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Título SIMPLE
        titulo = Label(
            text='👤 CREAR USUARIO 👤',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(titulo)
        print("✅ Título añadido")
        
        # Campos SUPER SIMPLES
        campos = ['nombre', 'apellido', 'telefono', 'correo', 'usuario', 'contrasena']
        self.inputs = {}
        
        for campo in campos:
            print(f"📝 Creando campo: {campo}")
            
            # Etiqueta
            label = Label(
                text=f"{obtener_texto(campo)}:",
                font_size=dp(16),
                size_hint_y=None,
                height=dp(30),
                color=(1, 1, 1, 1),
                halign='left'
            )
            label.bind(size=label.setter('text_size'))
            main_layout.add_widget(label)
            
            # Input BÁSICO
            input_field = TextInput(
                hint_text=f"Ingresa tu {campo}",
                multiline=False,
                font_size=dp(16),
                size_hint_y=None,
                height=dp(40),
                password=(campo == 'contrasena')
            )
            
            self.inputs[campo] = input_field
            main_layout.add_widget(input_field)
            print(f"   ✅ Campo {campo} creado")
        
        print(f"📋 Total inputs creados: {len(self.inputs)}")
        print(f"🔑 Keys: {list(self.inputs.keys())}")
        
        # Espaciador
        main_layout.add_widget(Label(size_hint_y=None, height=dp(20)))
        
        # BOTÓN GUARDAR - ULTRA SIMPLE
        print("🔧 Creando botón GUARDAR...")
        btn_guardar = Button(
            text='💾 GUARDAR USUARIO',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(50),
            background_color=(0, 0.8, 0, 1)  # Verde sólido
        )
        
        # TEST: Múltiples formas de binding
        print("🔗 Configurando binding del botón...")
        
        def test_click_guardar(instance):
            print("🔥 === BOTÓN GUARDAR CLICKEADO ===")
            print(f"🔥 Instance: {instance}")
            print(f"🔥 Instance.text: {instance.text}")
            self.handle_guardar()
        
        btn_guardar.bind(on_press=test_click_guardar)
        btn_guardar.bind(on_release=lambda x: print("🔥 BOTÓN GUARDAR RELEASED"))
        
        main_layout.add_widget(btn_guardar)
        print("✅ Botón GUARDAR añadido y configurado")
        
        # BOTÓN VOLVER - ULTRA SIMPLE
        print("🔧 Creando botón VOLVER...")
        btn_volver = Button(
            text='⬅️ VOLVER',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.5, 0.5, 0.5, 1)  # Gris sólido
        )
        
        def test_click_volver(instance):
            print("🔥 === BOTÓN VOLVER CLICKEADO ===")
            self.handle_volver()
        
        btn_volver.bind(on_press=test_click_volver)
        main_layout.add_widget(btn_volver)
        print("✅ Botón VOLVER añadido y configurado")
        
        # Añadir layout principal a la pantalla
        self.add_widget(main_layout)
        
        print("✅ === INTERFAZ CREADA COMPLETAMENTE ===")
        print(f"📊 Widgets en pantalla: {len(self.children)}")
        print(f"📊 Widgets en main_layout: {len(main_layout.children)}")
        
        # VERIFICAR que los inputs existen
        print("🔍 === VERIFICACIÓN FINAL ===")
        for campo, input_widget in self.inputs.items():
            print(f"   ✅ {campo}: {type(input_widget)} - {input_widget}")
    
    def handle_guardar(self):
        print("💾 === HANDLE GUARDAR INICIADO ===")
        
        try:
            # Verificar inputs
            if not hasattr(self, 'inputs'):
                print("❌ ERROR: No existe self.inputs")
                return
                
            if not self.inputs:
                print("❌ ERROR: self.inputs está vacío")
                return
                
            print(f"✅ self.inputs existe con {len(self.inputs)} campos")
            
            # Recopilar datos
            datos = {}
            for campo, input_widget in self.inputs.items():
                valor = input_widget.text.strip()
                datos[campo] = valor
                print(f"   📝 {campo}: '{valor}'")
            
            # Verificar datos vacíos
            campos_vacios = [k for k, v in datos.items() if not v]
            if campos_vacios:
                print(f"⚠️ Campos vacíos: {campos_vacios}")
                self.mostrar_popup_simple("⚠️ Error", f"Completa: {', '.join(campos_vacios)}")
                return
            
            print("✅ Todos los campos tienen datos")
            
            # Validaciones básicas
            if '@' not in datos.get('correo', ''):
                print("❌ Email inválido")
                self.mostrar_popup_simple("❌ Error", "Email inválido")
                return
                
            if len(datos.get('contrasena', '')) < 3:  # Reducido para test
                print("❌ Contraseña muy corta")
                self.mostrar_popup_simple("❌ Error", "Contraseña muy corta")
                return
            
            print("✅ Validaciones OK")
            
            # Intentar guardar
            if self.guardar_callback:
                print("🔄 Usando callback...")
                resultado = self.guardar_callback(datos)
                print(f"📤 Resultado callback: {resultado}")
            else:
                print("💾 Guardando localmente...")
                resultado = self.guardar_local(datos)
                
            if resultado:
                print("🎉 GUARDADO EXITOSO")
                self.mostrar_popup_simple("✅ Éxito", "Usuario creado!", self.handle_volver)
            else:
                print("❌ ERROR AL GUARDAR")
                self.mostrar_popup_simple("❌ Error", "No se pudo guardar")
                
        except Exception as e:
            print(f"💥 EXCEPCIÓN en handle_guardar: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_popup_simple("💥 Error", f"Error: {e}")
    
    def handle_volver(self, *args):
        print("🔙 === HANDLE VOLVER INICIADO ===")
        
        if self.volver_callback:
            print("🔄 Usando volver_callback...")
            self.volver_callback()
        else:
            print("🔄 Usando screen manager...")
            if self.manager:
                pantallas = [s.name for s in self.manager.screens]
                print(f"📋 Pantallas disponibles: {pantallas}")
                
                if 'login' in pantallas:
                    print("✅ Navegando a login")
                    self.manager.current = 'login'
                elif 'inicial' in pantallas:
                    print("✅ Navegando a inicial")
                    self.manager.current = 'inicial'
                else:
                    print("❌ No se encontró pantalla destino")
            else:
                print("❌ No hay manager")
    
    def guardar_local(self, datos):
        try:
            archivo = "usuarios_debug.json"
            usuarios = []
            
            if os.path.exists(archivo):
                with open(archivo, 'r') as f:
                    usuarios = json.load(f)
            
            usuarios.append(datos)
            
            with open(archivo, 'w') as f:
                json.dump(usuarios, f, indent=2)
            
            print(f"✅ Guardado en {archivo}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando: {e}")
            return False
    
    def mostrar_popup_simple(self, titulo, mensaje, callback=None):
        print(f"📱 Popup: {titulo} - {mensaje}")
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        label = Label(
            text=mensaje,
            font_size=dp(16),
            text_size=(dp(250), None),
            halign='center'
        )
        content.add_widget(label)
        
        btn = Button(
            text='OK',
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(btn)
        
        popup = Popup(
            title=titulo,
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        def cerrar(instance):
            popup.dismiss()
            if callback:
                callback()
        
        btn.bind(on_press=cerrar)
        popup.open()

# ===== TEST INDEPENDIENTE =====
if __name__ == "__main__":
    print("🧪 === TEST INDEPENDIENTE ===")
    
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager
    
    class DebugApp(App):
        def build(self):
            sm = ScreenManager()
            
            def test_guardar(datos):
                print(f"🧪 CALLBACK GUARDAR: {datos}")
                return True
            
            def test_volver():
                print("🧪 CALLBACK VOLVER")
            
            pantalla = PantallaCrearUsuario(
                guardar_callback=test_guardar,
                volver_callback=test_volver
            )
            
            sm.add_widget(pantalla)
            sm.current = 'crear_usuario'
            
            return sm
    
    DebugApp().run()