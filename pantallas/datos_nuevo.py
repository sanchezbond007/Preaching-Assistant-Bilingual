from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
import json
import datetime

class PantallaDatosNuevo(Screen):
    def __init__(self, volver_callback=None, navegar_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        
        self.volver_callback = volver_callback
        self.navegar_callback = navegar_callback
        self.idioma = idioma
        
        # CONSTRUIR INTERFAZ NUEVA QUE SÍ FUNCIONA
        self.construir_interfaz_nueva()
    
    def construir_interfaz_nueva(self):
        self.clear_widgets()
        
        # LAYOUT BÁSICO QUE FUNCIONA
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Título NUEVO
        titulo = Label(
            text='🎯 CAPTURA DE DATOS - NUEVO',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(titulo)
        
        # Status NUEVO
        self.status = Label(
            text='🚀 VERSIÓN NUEVA - Presiona botones',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status)
        
        # Campo Nombre
        layout.add_widget(Label(
            text='📝 Nombre del Interesado:', 
            size_hint_y=None, 
            height=dp(30),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        ))
        
        self.nombre_input = TextInput(
            hint_text='Escribe el nombre aquí',
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            font_size=dp(16)
        )
        layout.add_widget(self.nombre_input)
        
        # Campo Teléfono
        layout.add_widget(Label(
            text='📞 Teléfono:', 
            size_hint_y=None, 
            height=dp(30),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        ))
        
        self.telefono_input = TextInput(
            hint_text='Escribe el teléfono aquí',
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            font_size=dp(16)
        )
        layout.add_widget(self.telefono_input)
        
        # BOTÓN GUARDAR NUEVO
        btn_guardar = Button(
            text='🔥 GUARDAR DATOS',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(80),
            background_color=(0, 1, 0, 1),  # Verde
            color=(1, 1, 1, 1)
        )
        btn_guardar.bind(on_press=self.nuevo_guardar)
        layout.add_widget(btn_guardar)
        
        # BOTÓN OMITIR NUEVO
        btn_omitir = Button(
            text='⚡ OMITIR DATOS',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(80),
            background_color=(1, 0, 0, 1),  # Rojo
            color=(1, 1, 1, 1)
        )
        btn_omitir.bind(on_press=self.nuevo_omitir)
        layout.add_widget(btn_omitir)
        
        # BOTÓN TEST NUEVO
        btn_test = Button(
            text='🧪 TEST FUNCIONAMIENTO',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(60),
            background_color=(1, 0, 1, 1),  # Magenta
            color=(1, 1, 1, 1)
        )
        btn_test.bind(on_press=self.test_nuevo)
        layout.add_widget(btn_test)
        
        self.add_widget(layout)
    
    def nuevo_guardar(self, instance):
        self.status.text = '🔥 ¡BOTÓN GUARDAR FUNCIONA EN VERSIÓN NUEVA!'
        self.status.color = (1, 1, 0, 1)  # Amarillo
        instance.background_color = (1, 1, 0, 1)  # Amarillo
        
        nombre = self.nombre_input.text.strip() or "Sin nombre"
        telefono = self.telefono_input.text.strip()
        
        datos = {
            'nombre': nombre,
            'telefono': telefono,
            'timestamp': datetime.datetime.now().isoformat(),
            'version': 'nueva_funcionando',
            'archivo': 'datos_nuevo.py'
        }
        
        try:
            with open('datos_version_nueva.json', 'w') as f:
                json.dump(datos, f, indent=2)
            
            self.status.text = f'✅ GUARDADO EXITOSO: {nombre}'
            self.status.color = (0, 1, 0, 1)  # Verde
            
            # NAVEGAR
            self.navegar_nuevo()
            
        except Exception as e:
            self.status.text = f'❌ ERROR AL GUARDAR: {str(e)}'
            self.status.color = (1, 0, 0, 1)  # Rojo
    
    def nuevo_omitir(self, instance):
        self.status.text = '🔥 ¡BOTÓN OMITIR FUNCIONA EN VERSIÓN NUEVA!'
        self.status.color = (0, 0, 1, 1)  # Azul
        instance.background_color = (0, 0, 1, 1)  # Azul
        
        # NAVEGAR
        self.navegar_nuevo()
    
    def test_nuevo(self, instance):
        self.status.text = '🧪 ¡TEST OK! Los botones funcionan perfectamente'
        self.status.color = (1, 0, 1, 1)  # Magenta
        instance.background_color = (0, 1, 1, 1)  # Cian
    
    def navegar_nuevo(self):
        if self.navegar_callback:
            try:
                self.navegar_callback()
                self.status.text = '✅ Navegación exitosa'
                return
            except Exception as e:
                self.status.text = f'⚠️ Error callback: {str(e)}'
        
        if self.manager:
            pantallas = [s.name for s in self.manager.screens]
            self.status.text = f'📋 Pantallas disponibles: {pantallas}'
            
            if 'menu_temporal' in pantallas:
                self.manager.current = 'menu_temporal'
                self.status.text = '✅ Navegación a menu_temporal'
            elif 'menu_principal' in pantallas:
                self.manager.current = 'menu_principal'
                self.status.text = '✅ Navegación a menu_principal'