import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window

from utils.traducciones import traducir
from utils.temas_handler2 import cargar_temas_profundos


class PantallaTemasProfundos(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        self.temas = cargar_temas_profundos()
        self.botones_temas = []

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.titulo_label = Label(
            text=traducir("titulo_temas_profundos", self.idioma),
            font_size=36,
            size_hint_y=None,
            height=60,
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.titulo_label)

        scroll = ScrollView(size_hint=(1, 1))
        temas_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        temas_layout.bind(minimum_height=temas_layout.setter('height'))

        for tema in self.temas:
            titulo = tema.get('titulo', '')
            if isinstance(titulo, dict):
                texto_boton = titulo.get(self.idioma, '')
            else:
                texto_boton = titulo

            btn = Button(
                text=texto_boton,
                size_hint_y=None,
                height=80,
                on_press=lambda instancia, t=tema: self.mostrar_detalle(t)
            )
            temas_layout.add_widget(btn)
            self.botones_temas.append((btn, tema))

        scroll.add_widget(temas_layout)
        self.layout.add_widget(scroll)

        self.btn_volver = Button(
            text=traducir("volver", self.idioma),
            size_hint_y=None,
            height=60,
            on_press=self.volver_callback,
            background_color=(0.1, 0.1, 0.1, 1)
        )
        self.layout.add_widget(self.btn_volver)

        self.add_widget(self.layout)

    def mostrar_detalle(self, tema):
        contenido = BoxLayout(orientation='vertical', spacing=10, padding=10)

        titulo = tema.get('titulo', '')
        contenido_raw = tema.get('contenido', '')

        titulo_texto = titulo.get(self.idioma, '') if isinstance(titulo, dict) else titulo
        contenido_texto = contenido_raw.get(self.idioma, '') if isinstance(contenido_raw, dict) else contenido_raw

        contenido.add_widget(Label(text=titulo_texto, font_size=24, bold=True, size_hint_y=None, height=40))
        contenido.add_widget(Label(text=contenido_texto, font_size=20))
        btn_cerrar = Button(text=traducir("cerrar", self.idioma), size_hint_y=None, height=50)
        contenido.add_widget(btn_cerrar)

        popup = Popup(title=titulo_texto, content=contenido, size_hint=(0.9, 0.9))
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def actualizar_idioma(self, nuevo_idioma=None):
        if nuevo_idioma:
            self.idioma = nuevo_idioma
        self.titulo_label.text = traducir("titulo_temas_profundos", self.idioma)
        self.btn_volver.text = traducir("volver", self.idioma)

        for btn, tema in self.botones_temas:
            titulo = tema.get('titulo', '')
            if isinstance(titulo, dict):
                btn.text = titulo.get(self.idioma, '')
            else:
                btn.text = titulo