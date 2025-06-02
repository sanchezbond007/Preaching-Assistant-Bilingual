import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

# Acceso a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.temas_handler import obtener_sugerencias
# NO USAR traducciones.py para evitar conflictos
# from utils.traducciones import traducir as t

class PantallaSugerencias(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        self.layout_principal = None
        
        # Debug del idioma al inicializar
        print(f"🎯 SUGERENCIAS INICIALIZADA CON IDIOMA: '{self.idioma}' (tipo: {type(self.idioma)})")
        
        self.actualizar_idioma()  # Inicializa la interfaz

    def _obtener_texto(self, clave):
        """Sistema de traducciones propio independiente"""
        # Verificación del idioma
        idioma_str = str(self.idioma).lower().strip()
        es_ingles = (
            idioma_str == 'en' or 
            idioma_str == 'english' or 
            idioma_str.startswith('en') or
            'en' in idioma_str or
            'english' in idioma_str
        )
        
        if es_ingles:
            traducciones = {
                'sugerencias_titulo': 'Suggestions',
                'volver': 'Back',
                'cargando': 'Loading suggestions...',
                'sin_sugerencias': 'No suggestions available'
            }
            print(f"✅ Usando textos en INGLÉS para: '{clave}'")
        else:
            traducciones = {
                'sugerencias_titulo': 'Sugerencias',
                'volver': 'Volver',
                'cargando': 'Cargando sugerencias...',
                'sin_sugerencias': 'No hay sugerencias disponibles'
            }
            print(f"✅ Usando textos en ESPAÑOL para: '{clave}'")
        
        return traducciones.get(clave, clave.replace('_', ' ').title())

    def actualizar_idioma(self):
        """Actualiza la interfaz con el idioma actual"""
        print(f"🔄 Actualizando sugerencias para idioma: '{self.idioma}'")
        self.construir_interfaz()

    def forzar_idioma(self, idioma):
        """Método para forzar un idioma específico"""
        print(f"🔧 FORZANDO IDIOMA EN SUGERENCIAS: '{idioma}'")
        self.idioma = idioma
        self.clear_widgets()
        self.construir_interfaz()
        print(f"🔧 IDIOMA FORZADO EN SUGERENCIAS: '{idioma}'")

    def construir_interfaz(self):
        """Construye la interfaz completa"""
        print(f"🏗️ Construyendo interfaz de sugerencias con idioma: '{self.idioma}'")
        
        self.clear_widgets()

        self.layout_principal = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Título dinámico según idioma
        titulo_texto = self._obtener_texto('sugerencias_titulo')
        titulo = Label(
            text=titulo_texto,
            font_size=40,
            size_hint_y=None,
            height=60,
            color=(0, 0, 0, 1)
        )
        self.layout_principal.add_widget(titulo)
        print(f"✅ Título creado: '{titulo_texto}'")

        # Scroll con sugerencias
        scroll = ScrollView()
        layout_scroll = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        layout_scroll.bind(minimum_height=layout_scroll.setter('height'))

        try:
            # Obtener sugerencias (usar idioma en formato correcto para el handler)
            idioma_para_handler = 'en' if self._es_ingles() else 'es'
            sugerencias = obtener_sugerencias(idioma=idioma_para_handler, limite=10)
            print(f"📋 Obtenidas {len(sugerencias)} sugerencias para idioma: {idioma_para_handler}")
        except Exception as e:
            print(f"⚠️ Error al obtener sugerencias: {e}")
            sugerencias = []

        if sugerencias:
            for i, sugerencia in enumerate(sugerencias):
                texto = f"• {sugerencia.get('titulo', f'Sugerencia {i+1}')}"
                btn = Button(
                    text=texto,
                    size_hint_y=None,
                    height=80,
                    font_size=26,
                    color=(1, 1, 1, 1),
                    background_color=(0.3, 0.7, 1, 1),  # ✨ AZUL CIELO CONSISTENTE ✨
                    text_size=(None, None)
                )
                layout_scroll.add_widget(btn)
                print(f"✅ Botón sugerencia creado: '{texto[:50]}...'")
        else:
            # Mensaje cuando no hay sugerencias
            sin_sugerencias = Label(
                text=self._obtener_texto('sin_sugerencias'),
                font_size=24,
                size_hint_y=None,
                height=100,
                color=(0.5, 0.5, 0.5, 1)
            )
            layout_scroll.add_widget(sin_sugerencias)

        scroll.add_widget(layout_scroll)
        self.layout_principal.add_widget(scroll)

        # Botón volver con texto dinámico
        btn_volver_texto = self._obtener_texto('volver')
        btn_volver = Button(
            text=btn_volver_texto,
            size_hint_y=None,
            height=80,
            font_size=24,
            background_color=(0.3, 0.7, 1, 1),  # ✨ AZUL CIELO CONSISTENTE ✨
            color=(1, 1, 1, 1)
        )
        btn_volver.bind(on_press=self._manejar_volver)
        self.layout_principal.add_widget(btn_volver)
        print(f"✅ Botón volver creado: '{btn_volver_texto}'")

        self.add_widget(self.layout_principal)
        print(f"🎨 Interfaz de sugerencias construida con idioma: {'INGLÉS' if self._es_ingles() else 'ESPAÑOL'}")

    def _es_ingles(self):
        """Determina si el idioma actual es inglés"""
        idioma_str = str(self.idioma).lower().strip()
        return (
            idioma_str == 'en' or 
            idioma_str == 'english' or 
            idioma_str.startswith('en') or
            'en' in idioma_str or
            'english' in idioma_str
        )

    def _manejar_volver(self, instance):
        """Maneja el botón volver"""
        print("🔙 Volviendo desde sugerencias...")
        if self.volver_callback:
            self.volver_callback()
        else:
            # Fallback navigation
            if self.manager and self.manager.has_screen('menu'):
                self.manager.current = 'menu'

    def cambiar_idioma(self, nuevo_idioma):
        """Método para cambiar el idioma externamente"""
        print(f"🌍 Cambiando idioma en sugerencias de '{self.idioma}' a '{nuevo_idioma}'")
        self.idioma = nuevo_idioma
        self.actualizar_idioma()