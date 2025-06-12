from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock
import json
import datetime

class PantallaDatosCallbacksSeguro(Screen):
    def __init__(self, volver_callback=None, navegar_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        
        # GUARDAR CALLBACKS DE FORMA SEGURA
        self.volver_callback = volver_callback
        self.navegar_callback = navegar_callback
        self.idioma = idioma
        
        # CONSTRUIR INTERFAZ IGUAL QUE LA VERSIÓN QUE FUNCIONA
        self.construir_interfaz_segura()
    
    def construir_interfaz_segura(self):
        self.clear_widgets()
        
        # LAYOUT EXACTAMENTE IGUAL QUE LA VERSIÓN QUE FUNCIONA
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Título
        titulo = Label(
            text='🎯 CAPTURA DE DATOS - CALLBACKS SEGUROS',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(titulo)
        
        # Status
        self.status = Label(
            text='🛡️ VERSIÓN CON CALLBACKS SEGUROS',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            color=(0, 1, 1, 1)  # Cian
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
            hint_text='Nombre del interesado',
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
            hint_text='Teléfono del interesado',
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            font_size=dp(16)
        )
        layout.add_widget(self.telefono_input)
        
        # BOTÓN GUARDAR SEGURO
        btn_guardar = Button(
            text='🔥 GUARDAR SEGURO',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(80),
            background_color=(0, 1, 0, 1),
            color=(1, 1, 1, 1)
        )
        btn_guardar.bind(on_press=self.guardar_seguro)
        layout.add_widget(btn_guardar)
        
        # BOTÓN OMITIR SEGURO
        btn_omitir = Button(
            text='⚡ OMITIR SEGURO',
            font_size=dp(20),
            size_hint_y=None,
            height=dp(80),
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        btn_omitir.bind(on_press=self.omitir_seguro)
        layout.add_widget(btn_omitir)
        
        # BOTÓN TEST
        btn_test = Button(
            text='🧪 TEST CALLBACKS',
            font_size=dp(18),
            size_hint_y=None,
            height=dp(60),
            background_color=(1, 0, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_test.bind(on_press=self.test_callbacks)
        layout.add_widget(btn_test)
        
        self.add_widget(layout)
    
    def guardar_seguro(self, instance):
        # FEEDBACK INMEDIATO IGUAL QUE LA VERSIÓN QUE FUNCIONA
        self.status.text = '🔥 ¡GUARDAR FUNCIONA CON CALLBACKS SEGUROS!'
        self.status.color = (0, 1, 0, 1)
        instance.background_color = (1, 1, 0, 1)
        
        nombre = self.nombre_input.text.strip() or "Sin nombre"
        telefono = self.telefono_input.text.strip()
        
        datos = {
            'nombre': nombre,
            'telefono': telefono,
            'timestamp': datetime.datetime.now().isoformat(),
            'version': 'callbacks_seguros'
        }
        
        try:
            with open('datos_callbacks_seguros.json', 'w') as f:
                json.dump(datos, f, indent=2)
            
            self.status.text = f'✅ GUARDADO SEGURO: {nombre}'
            
            # NAVEGAR DE FORMA SEGURA CON DELAY
            Clock.schedule_once(lambda dt: self.navegar_con_seguridad(), 1.0)
            
        except Exception as e:
            self.status.text = f'❌ ERROR: {str(e)}'
    
    def omitir_seguro(self, instance):
        # FEEDBACK INMEDIATO
        self.status.text = '🔥 ¡OMITIR FUNCIONA CON CALLBACKS SEGUROS!'
        self.status.color = (0, 0, 1, 1)
        instance.background_color = (0, 0, 1, 1)
        
        # NAVEGAR DE FORMA SEGURA CON DELAY
        Clock.schedule_once(lambda dt: self.navegar_con_seguridad(), 1.0)
    
    def test_callbacks(self, instance):
        self.status.text = '🧪 ¡TEST CALLBACKS OK!'
        self.status.color = (1, 0, 1, 1)
        instance.background_color = (0, 1, 1, 1)
        
        # MOSTRAR INFO DE CALLBACKS
        volver_existe = "SÍ" if self.volver_callback else "NO"
        navegar_existe = "SÍ" if self.navegar_callback else "NO"
        
        self.status.text = f'Volver: {volver_existe} | Navegar: {navegar_existe}'
    
    def navegar_con_seguridad(self):
        """Navegar de forma segura sin romper los botones"""
        try:
            # INTENTAR CALLBACK DE NAVEGACIÓN
            if self.navegar_callback:
                self.status.text = '🔄 Ejecutando navegar_callback...'
                self.navegar_callback()
                self.status.text = '✅ Navegación exitosa'
                return
        except Exception as e:
            self.status.text = f'⚠️ Error callback: {str(e)}'
        
        try:
            # NAVEGACIÓN DIRECTA COMO BACKUP
            if self.manager:
                pantallas = [s.name for s in self.manager.screens]
                
                if 'menu_temporal' in pantallas:
                    self.manager.current = 'menu_temporal'
                    self.status.text = '✅ Navegación a menu_temporal'
                elif 'menu_principal' in pantallas:
                    self.manager.current = 'menu_principal'
                    self.status.text = '✅ Navegación a menu_principal'
                elif 'captura_interesado' in pantallas:
                    self.manager.current = 'captura_interesado'
                    self.status.text = '✅ Navegación a captura_interesado'
                else:
                    self.status.text = f'📋 Pantallas: {pantallas}'
        except Exception as e:
            self.status.text = f'❌ Error navegación: {str(e)}'