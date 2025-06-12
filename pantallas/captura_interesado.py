# ==================================================================
# pantallas/captura_interesado.py - VERSIÓN MÍNIMA QUE FUNCIONA
# ==================================================================

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
import datetime

class PantallaCapturaInteresado(Screen):
    """Pantalla para capturar datos del interesado"""
    
    def __init__(self, **kwargs):
        self.guardar_callback = kwargs.pop('guardar_callback', None)
        self.continuar_callback = kwargs.pop('continuar_callback', None)
        self.idioma_callback = kwargs.pop('idioma_callback', None)
        self.idioma = kwargs.pop('idioma', 'es')
        
        super().__init__(**kwargs)
        self.name = 'captura_interesado'
        
        self.input_nombre = None
        self.input_telefono = None
        
        print(f"👤 Captura Interesado - Idioma: {self.idioma}")
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz simple"""
        layout_principal = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Título
        titulo = Label(
            text='👤 Datos del Interesado' if self.idioma == 'es' else '👤 Interested Person Data',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.4, 0.8, 1),
            bold=True
        )
        layout_principal.add_widget(titulo)
        
        # Nombre
        layout_principal.add_widget(Label(
            text='Nombre / Name *',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30)
        ))
        
        self.input_nombre = TextInput(
            hint_text='Ej: María González',
            multiline=False,
            font_size=dp(14),
            size_hint_y=None,
            height=dp(40)
        )
        layout_principal.add_widget(self.input_nombre)
        
        # Teléfono
        layout_principal.add_widget(Label(
            text='Teléfono / Phone',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30)
        ))
        
        self.input_telefono = TextInput(
            hint_text='+1 555-123-4567',
            multiline=False,
            font_size=dp(14),
            size_hint_y=None,
            height=dp(40)
        )
        layout_principal.add_widget(self.input_telefono)
        
        # Botones
        layout_botones = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        btn_guardar = Button(
            text='Guardar / Save',
            font_size=dp(16),
            background_color=(0.2, 0.7, 0.2, 1)
        )
        btn_guardar.bind(on_press=self.guardar_y_continuar)
        
        btn_omitir = Button(
            text='Omitir / Skip',
            font_size=dp(16),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_omitir.bind(on_press=self.omitir_captura)
        
        layout_botones.add_widget(btn_guardar)
        layout_botones.add_widget(btn_omitir)
        layout_principal.add_widget(layout_botones)
        
        self.add_widget(layout_principal)
    
    def guardar_y_continuar(self, instance):
        """Guardar datos"""
        nombre = self.input_nombre.text.strip()
        
        if not nombre:
            popup = Popup(
                title='Error',
                content=Label(text='El nombre es requerido\nName is required'),
                size_hint=(0.8, 0.3),
                auto_dismiss=True
            )
            popup.open()
            return
        
        datos_interesado = {
            'nombre': nombre,
            'telefono': self.input_telefono.text.strip(),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        print(f"✅ Datos guardados: {nombre}")
        
        if self.guardar_callback:
            self.guardar_callback(datos_interesado)
    
    def omitir_captura(self, instance):
        """Omitir captura"""
        datos_minimos = {
            'nombre': 'Interesado',
            'telefono': '',
            'omitido': True
        }
        
        if self.guardar_callback:
            self.guardar_callback(datos_minimos)
    
    def actualizar_idioma(self, nuevo_idioma):
        """Actualizar idioma"""
        if self.idioma != nuevo_idioma:
            self.idioma = nuevo_idioma
            self.clear_widgets()
            self.crear_interfaz()