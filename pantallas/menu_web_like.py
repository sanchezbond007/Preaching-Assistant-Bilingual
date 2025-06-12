# pantallas/menu_web_like.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock


class PantallaMenuWebLike(Screen):
    def __init__(self, **kwargs):
        self.sugerencias_callback = kwargs.pop('sugerencias_callback', None)
        self.temas_profundos_callback = kwargs.pop('temas_profundos_callback', None)
        self.buscador_callback = kwargs.pop('buscador_callback', None)
        self.recordatorios_callback = kwargs.pop('recordatorios_callback', None)
        self.resumen_callback = kwargs.pop('resumen_callback', None)
        self.configuracion_callback = kwargs.pop('configuracion_callback', None)
        super().__init__(**kwargs)
        Clock.schedule_once(self.construir_interfaz)

    def construir_interfaz(self, *args):
        layout_principal = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(30))
        layout_principal.add_widget(Label(text='Asistente de Predicación', font_size=28, size_hint_y=None, height=dp(60), color=[0.2, 0.2, 0.2, 1]))

        botones = [
            ("📋 Sugerencias", self.sugerencias_callback),
            ("📖 Temas Profundos", self.temas_profundos_callback),
            ("🔍 Buscar Tema", self.buscador_callback),
            ("⏰ Mis Recordatorios", self.recordatorios_callback),
            ("📤 Enviar Resumen", self.resumen_callback),
            ("⚙️ Configuración", self.configuracion_callback),
        ]

        for texto, accion in botones:
            btn = Button(
                text=texto,
                size_hint_y=None,
                height=dp(50),
                font_size=18,
                background_normal='',
                background_color=(0.26, 0.6, 0.36, 1),
                color=(1, 1, 1, 1),
                on_release=accion if accion else lambda x: print("⚠️ Acción no definida")
            )
            layout_principal.add_widget(btn)

        self.add_widget(layout_principal)