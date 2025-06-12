# ==================================================================
# PARTE 1: IMPORTACIONES Y CONFIGURACIÓN INICIAL
# Archivo: pantallas/buscar.py
# ==================================================================

import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

# Asegura acceso a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.temas_handler import cargar_todos_los_bloques
from utils.temas_handler2 import cargar_temas_profundos
from utils.traducciones import traducir as t

# INTEGRACIÓN CON HISTORIAL
try:
    from pantallas.send_resume import agregar_consulta_al_historial
    HISTORIAL_DISPONIBLE = True
    print("✅ Integración con historial disponible")
except ImportError:
    HISTORIAL_DISPONIBLE = False
    print("⚠️ Historial no disponible")

class PantallaBuscar(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        
        # Variables para resultados
        self.resultados_actuales = []

        # Layout principal
        self.layout_principal = BoxLayout(
            orientation='vertical', 
            spacing=dp(5), 
            padding=dp(15)
        )
        
        # Crear componentes
        self.crear_header()
        self.crear_area_scroll()
        self.crear_footer()
        
        self.add_widget(self.layout_principal)