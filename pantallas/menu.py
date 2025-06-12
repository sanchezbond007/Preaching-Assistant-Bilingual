from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

class MenuTemporal(Screen):
    def __init__(self, **kwargs):
        print("🎯 === CREANDO MENU TEMPORAL ===")
        
        # Extraer callbacks
        self.volver_callback = kwargs.pop('volver_callback', None)
        self.idioma = kwargs.pop('idioma', 'es')
        
        super().__init__(**kwargs)
        self.name = 'menu_temporal'
        
        print("🔧 Creando interfaz del menú...")
        self.crear_interfaz()
        print("✅ MenuTemporal creado exitosamente")
    
    def crear_interfaz(self):
        print("🔧 === CREANDO INTERFAZ MENU ===")
        
        # Limpiar
        self.clear_widgets()
        
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Título del menú
        titulo = Label(
            text='🎯 MENÚ PRINCIPAL',
            font_size=dp(28),
            size_hint_y=None,
            height=dp(80),
            color=(1, 1, 1, 1),
            bold=True
        )
        main_layout.add_widget(titulo)
        
        # Mensaje de bienvenida
        mensaje = Label(
            text='¡Bienvenido al Asistente de Predicación!\nSelecciona una opción:',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(80),
            color=(0.8, 0.8, 0.8, 1),
            halign='center',
            text_size=(None, None)
        )
        mensaje.bind(size=mensaje.setter('text_size'))
        main_layout.add_widget(mensaje)
        
        # Espaciador
        main_layout.add_widget(Label(size_hint_y=None, height=dp(20)))
        
        # Botones del menú
        opciones = [
            ('📋 Capturar Nuevo Interesado', self.ir_a_captura),
            ('📊 Ver Datos Guardados', self.ver_datos),
            ('📖 Revisitas', self.revisitas),
            ('📚 Estudios Bíblicos', self.estudios),
            ('⚙️ Configuración', self.configuracion),
        ]
        
        for texto, callback in opciones:
            btn = Button(
                text=texto,
                font_size=dp(18),
                size_hint_y=None,
                height=dp(60),
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_press=callback)
            main_layout.add_widget(btn)
            print(f"   ✅ Botón creado: {texto}")
        
        # Espaciador
        main_layout.add_widget(Label(size_hint_y=None, height=dp(30)))
        
        # Botón volver
        btn_volver = Button(
            text='⬅️ VOLVER A DATOS',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        btn_volver.bind(on_press=self.handle_volver)
        main_layout.add_widget(btn_volver)
        
        # Añadir layout principal
        self.add_widget(main_layout)
        print("✅ Interfaz del menú completada")
    
    def ir_a_captura(self, instance):
        print("📋 === IR A CAPTURA INTERESADO ===")
        if self.manager:
            if 'captura_interesado' in [s.name for s in self.manager.screens]:
                self.manager.current = 'captura_interesado'
                print("✅ Navegando a captura_interesado")
            else:
                print("❌ No se encontró pantalla captura_interesado")
        else:
            print("❌ No hay manager")
    
    def ver_datos(self, instance):
        print("📊 === VER DATOS GUARDADOS ===")
        # Por ahora solo mostramos mensaje
        print("🔧 Función Ver Datos - Por implementar")
    
    def revisitas(self, instance):
        print("📖 === REVISITAS ===")
        print("🔧 Función Revisitas - Por implementar")
    
    def estudios(self, instance):
        print("📚 === ESTUDIOS BÍBLICOS ===")
        print("🔧 Función Estudios - Por implementar")
    
    def configuracion(self, instance):
        print("⚙️ === CONFIGURACIÓN ===")
        print("🔧 Función Configuración - Por implementar")
    
    def handle_volver(self, instance):
        print("🔙 === VOLVER A DATOS INTERESADO ===")
        
        if self.volver_callback:
            print("🔄 Usando volver_callback...")
            self.volver_callback()
        else:
            print("🔄 Usando screen manager...")
            if self.manager:
                pantallas = [s.name for s in self.manager.screens]
                print(f"📋 Pantallas disponibles: {pantallas}")
                
                if 'datos_interesado' in pantallas:
                    print("✅ Navegando a datos_interesado")
                    self.manager.current = 'datos_interesado'
                else:
                    print("❌ No se encontró pantalla datos_interesado")
            else:
                print("❌ No hay manager")