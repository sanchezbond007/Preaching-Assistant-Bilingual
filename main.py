import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
import webbrowser
import urllib.parse

CARPETA_TEMAS = '/storage/emulated/0/prueba_asistente_predicacion_bilingue/datos/temas/'
CARPETA_TEMAS_PROFUNDOS = '/storage/emulated/0/prueba_asistente_predicacion_bilingue/datos/temas_profundos/'

TEXTOS = {
    "es": {
        "app_title": "Explora la Verdad",
        "legal_title": "Aviso Legal",
        "legal_text": "Esta aplicación no es parte ni está afiliada a ninguna entidad oficial. Todos los derechos de los textos, imágenes y enlaces pertenecen a sus respectivos autores y propietarios. El contenido es solo para fines educativos y de consulta personal. Para información oficial, visite jw.org.\n\nAl pulsar 'Aceptar' usted reconoce haber leído y comprendido este aviso.",
        "accept": "Aceptar",
        "reject": "Rechazar",
        "menu_subtitle": "Encuentra respuestas bíblicas claras y fieles.",
        "search": "Buscar Tema",
        "fundamental_topics": "Temas Fundamentales",
        "deep_topics": "Profundicemos en el Tema",
        "update": "Actualizar Temas",
        "update_success": "Actualización completada.",
        "back_menu": "Volver al menú",
        "send_summary": "Enviar Resumen",
        "search_title": "Buscar Tema",
        "search_hint": "Escribe una palabra clave (ej: alma, fe, 1914, Jesucristo)...",
        "search_btn": "Buscar",
        "no_results": "No se encontraron temas con esa palabra.",
        "no_topics": "No hay temas para mostrar.",
        "close": "Cerrar",
        "conclusion": "Conclusión:",
        "summary_ready": "Resumen listo para compartir:"
    },
    "en": {
        "app_title": "Explore the Truth",
        "legal_title": "Legal Notice",
        "legal_text": "This app is not part of nor affiliated with any official entity. All rights to texts, images, and links belong to their respective authors and owners. Content is for educational and personal consultation only. For official information, visit jw.org.\n\nBy pressing 'Accept' you acknowledge you have read and understood this notice.",
        "accept": "Accept",
        "reject": "Reject",
        "menu_subtitle": "Find clear and faithful Bible answers.",
        "search": "Search Topic",
        "fundamental_topics": "Fundamental Topics",
        "deep_topics": "Deep Topics",
        "update": "Update Topics",
        "update_success": "Update completed.",
        "back_menu": "Back to menu",
        "send_summary": "Send Summary",
        "search_title": "Search Topic",
        "search_hint": "Type a keyword (e.g.: soul, faith, 1914, Jesus Christ)...",
        "search_btn": "Search",
        "no_results": "No topics found for that word.",
        "no_topics": "No topics to display.",
        "close": "Close",
        "conclusion": "Conclusion:",
        "summary_ready": "Summary ready to share:"
    }
}

def cargar_todos_los_temas():
    temas = []
    if not os.path.exists(CARPETA_TEMAS):
        return temas
    archivos = [f for f in os.listdir(CARPETA_TEMAS) if f.endswith('.json')]
    for archivo in archivos:
        ruta = os.path.join(CARPETA_TEMAS, archivo)
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and 'temas' in data:
                for tema in data['temas']:
                    temas.append(tema)
            elif isinstance(data, dict) and 'titulo' in data:
                temas.append(data)
        except Exception as e:
            print(f"Error al leer {archivo}: {e}")
    return temas

def cargar_temas_profundos():
    temas = []
    if not os.path.exists(CARPETA_TEMAS_PROFUNDOS):
        return temas
    archivos = [f for f in os.listdir(CARPETA_TEMAS_PROFUNDOS) if f.endswith('.json')]
    for archivo in archivos:
        ruta = os.path.join(CARPETA_TEMAS_PROFUNDOS, archivo)
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            temas.append(data)
        except Exception as e:
            print(f"Error al leer {archivo}: {e}")
    return temas

def crear_label(texto, font_size=15, bold=False):
    lbl = Label(
        text=f"[b]{texto}[/b]" if bold else texto,
        markup=True,
        font_size=dp(font_size),
        size_hint_y=None,
        halign='left',
        valign='top'
    )
    def update_text_size(instance, value):
        instance.text_size = (value, None)
    def update_height(instance, value):
        instance.height = value[1]
    lbl.bind(width=update_text_size, texture_size=update_height)
    return lbl

def crear_boton_multilinea(texto, color, on_press_fn):
    btn = Button(
        text=texto,
        size_hint_y=None,
        background_color=color,
        color=(1, 1, 1, 1),
        font_size=dp(15),
        halign="left",
        valign="middle",
        markup=True,
        padding=(dp(10), dp(10))
    )
    def update_text_size(instance, value):
        instance.text_size = (instance.width - dp(20), None)
    def update_height(instance, value):
        instance.height = max(dp(48), instance.texture_size[1] + dp(14))
    btn.bind(width=update_text_size, texture_size=update_height)
    btn.bind(on_press=on_press_fn)
    return btn

class PantallaIdioma(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'idioma'
        self.app = app
        self.construir()

    def construir(self):
        layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(30))
        layout.add_widget(Label(text="Seleccione idioma / Select language", font_size=dp(22), size_hint_y=None, height=dp(60)))
        btn_es = Button(text="Español", font_size=dp(18), background_color=(0.1, 0.6, 0.1, 1), size_hint_y=None, height=dp(60))
        btn_en = Button(text="English", font_size=dp(18), background_color=(0.1, 0.3, 0.7, 1), size_hint_y=None, height=dp(60))
        btn_es.bind(on_press=lambda x: self.seleccionar_idioma('es'))
        btn_en.bind(on_press=lambda x: self.seleccionar_idioma('en'))
        layout.add_widget(btn_es)
        layout.add_widget(btn_en)
        self.add_widget(layout)

    def seleccionar_idioma(self, idioma):
        self.app.idioma = idioma
        self.app.cargar_pantallas()
        self.manager.current = 'aviso_legal'

class PantallaAvisoLegal(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'aviso_legal'
        self.app = app
        self.construir_interfaz()

    def construir_interfaz(self):
        tr = TEXTOS[self.app.idioma]
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        layout.add_widget(Label(text=tr["app_title"], font_size=dp(28), size_hint_y=None, height=dp(60), color=(1,1,1,1), bold=True))
        layout.add_widget(Label(text=tr["legal_title"], font_size=dp(18), size_hint_y=None, height=dp(30), color=(1,1,1,1)))
        texto_legal = Label(
            text=tr["legal_text"], font_size=dp(14), halign='center', valign='middle',
            color=(0.9, 0.9, 0.9, 1), size_hint_y=None, height=dp(180)
        )
        texto_legal.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
        layout.add_widget(texto_legal)
        botones_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), spacing=dp(20))
        btn_aceptar = Button(text=tr["accept"], font_size=dp(20), background_color=(0.1, 0.6, 0.1, 1), color=(1, 1, 1, 1))
        btn_aceptar.bind(on_press=self.aceptar)
        btn_rechazar = Button(text=tr["reject"], font_size=dp(20), background_color=(0.6, 0.1, 0.1, 1), color=(1, 1, 1, 1))
        btn_rechazar.bind(on_press=self.rechazar)
        botones_layout.add_widget(btn_aceptar)
        botones_layout.add_widget(btn_rechazar)
        layout.add_widget(botones_layout)
        self.add_widget(layout)

    def aceptar(self, instance):
        self.manager.current = 'menu_principal'

    def rechazar(self, instance):
        App.get_running_app().stop()

class PantallaMenuPrincipal(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu_principal'
        self.app = app
        self.construir_menu()

    def construir_menu(self):
        tr = TEXTOS[self.app.idioma]
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        layout.add_widget(Label(text=tr["app_title"], font_size=dp(28), size_hint_y=None, height=dp(60), color=(1,1,1,1), bold=True))
        layout.add_widget(Label(text=tr["menu_subtitle"], font_size=dp(15), size_hint_y=None, height=dp(30), color=(0.8,0.8,0.8,1)))
        btn_actualizar = Button(
            text=tr["update"], font_size=dp(16), size_hint_y=None, height=dp(45),
            background_color=(0.8, 0.5, 0.1, 1), color=(1, 1, 1, 1)
        )
        btn_actualizar.bind(on_press=self.actualizar_temas)
        layout.add_widget(btn_actualizar)
        btn_buscar = Button(
            text=tr["search"], font_size=dp(18), size_hint_y=None, height=dp(50),
            background_color=(0.3, 0.6, 0.3, 1), color=(1, 1, 1, 1)
        )
        btn_buscar.bind(on_press=self.ir_busqueda)
        layout.add_widget(btn_buscar)
        btn_temas_fund = Button(
            text=tr["fundamental_topics"], font_size=dp(18), size_hint_y=None, height=dp(50),
            background_color=(0.2, 0.4, 0.6, 1), color=(1, 1, 1, 1)
        )
        btn_temas_fund.bind(on_press=self.ir_temas_fundamentales)
        layout.add_widget(btn_temas_fund)
        btn_temas_prof = Button(
            text=tr["deep_topics"], font_size=dp(18), size_hint_y=None, height=dp(50),
            background_color=(0.5, 0.2, 0.4, 1), color=(1, 1, 1, 1)
        )
        btn_temas_prof.bind(on_press=self.ir_temas_profundos)
        layout.add_widget(btn_temas_prof)
        layout.add_widget(Label(size_hint_y=1))
        self.add_widget(layout)

    def actualizar_temas(self, instance):
        tr = TEXTOS[self.app.idioma]
        Popup(title=tr["update"], content=Label(text=tr["update_success"]), size_hint=(0.7, 0.3)).open()

    def ir_busqueda(self, instance):
        self.manager.current = 'busqueda'

    def ir_temas_fundamentales(self, instance):
        self.manager.current = 'temas_fundamentales'

    def ir_temas_profundos(self, instance):
        self.manager.current = 'temas_profundos'

class PantallaTemasFundamentales(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'temas_fundamentales'
        self.app = app
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.add_widget(self.layout)
        self.pagina = 0
        self.temas_por_pagina = 20

    def on_pre_enter(self):
        self.pagina = 0
        self.temas = cargar_todos_los_temas()
        self.mostrar_pagina()

    def mostrar_pagina(self):
        self.layout.clear_widgets()
        tr = TEXTOS[self.app.idioma]
        total = len(self.temas)
        inicio = self.pagina * self.temas_por_pagina
        fin = min(inicio + self.temas_por_pagina, total)
        self.layout.add_widget(Label(text=tr["fundamental_topics"], font_size=dp(22), bold=True, size_hint_y=None, height=dp(40)))
        if total:
            scroll = ScrollView()
            temas_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
            temas_layout.bind(minimum_height=temas_layout.setter('height'))
            for tema in self.temas[inicio:fin]:
                btn = crear_boton_multilinea(
                    tema['titulo'][self.app.idioma],
                    (0.2, 0.4, 0.6, 1),
                    lambda inst, t=tema: self.mostrar_detalle_tema(t, 'fundamental')
                )
                temas_layout.add_widget(btn)
            scroll.add_widget(temas_layout)
            self.layout.add_widget(scroll)
            nav = BoxLayout(size_hint_y=None, height=dp(48))
            btn_prev = Button(text="Anterior", disabled=self.pagina==0)
            btn_next = Button(text="Siguiente", disabled=fin>=total)
            btn_prev.bind(on_press=lambda x: self.cambiar_pagina(-1))
            btn_next.bind(on_press=lambda x: self.cambiar_pagina(1))
            nav.add_widget(btn_prev)
            nav.add_widget(btn_next)
            self.layout.add_widget(nav)
        else:
            self.layout.add_widget(Label(text=tr["no_topics"], font_size=dp(15)))
        btn_volver = Button(text=tr["back_menu"], size_hint_y=None, height=dp(45))
        btn_volver.bind(on_press=self.volver_menu)
        self.layout.add_widget(btn_volver)

    def cambiar_pagina(self, delta):
        self.pagina += delta
        self.mostrar_pagina()

    def mostrar_detalle_tema(self, tema, tipo):
        PantallaBusqueda(self.app).mostrar_detalle_tema(tema, tipo)

    def volver_menu(self, instance):
        self.manager.current = 'menu_principal'

class PantallaTemasProfundos(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'temas_profundos'
        self.app = app
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.add_widget(self.layout)
        self.pagina = 0
        self.temas_por_pagina = 20

    def on_pre_enter(self):
        self.pagina = 0
        self.temas = cargar_temas_profundos()
        self.mostrar_pagina()

    def mostrar_pagina(self):
        self.layout.clear_widgets()
        tr = TEXTOS[self.app.idioma]
        total = len(self.temas)
        inicio = self.pagina * self.temas_por_pagina
        fin = min(inicio + self.temas_por_pagina, total)
        self.layout.add_widget(Label(text=tr["deep_topics"], font_size=dp(22), bold=True, size_hint_y=None, height=dp(40)))
        if total:
            scroll = ScrollView()
            temas_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
            temas_layout.bind(minimum_height=temas_layout.setter('height'))
            for tema in self.temas[inicio:fin]:
                btn = crear_boton_multilinea(
                    tema['titulo'][self.app.idioma],
                    (0.5, 0.2, 0.4, 1),
                    lambda inst, t=tema: self.mostrar_detalle_tema(t, 'profundo')
                )
                temas_layout.add_widget(btn)
            scroll.add_widget(temas_layout)
            self.layout.add_widget(scroll)
            nav = BoxLayout(size_hint_y=None, height=dp(48))
            btn_prev = Button(text="Anterior", disabled=self.pagina==0)
            btn_next = Button(text="Siguiente", disabled=fin>=total)
            btn_prev.bind(on_press=lambda x: self.cambiar_pagina(-1))
            btn_next.bind(on_press=lambda x: self.cambiar_pagina(1))
            nav.add_widget(btn_prev)
            nav.add_widget(btn_next)
            self.layout.add_widget(nav)
        else:
            self.layout.add_widget(Label(text=tr["no_topics"], font_size=dp(15)))
        btn_volver = Button(text=tr["back_menu"], size_hint_y=None, height=dp(45))
        btn_volver.bind(on_press=self.volver_menu)
        self.layout.add_widget(btn_volver)

    def cambiar_pagina(self, delta):
        self.pagina += delta
        self.mostrar_pagina()

    def mostrar_detalle_tema(self, tema, tipo):
        PantallaBusqueda(self.app).mostrar_detalle_tema(tema, tipo)

    def volver_menu(self, instance):
        self.manager.current = 'menu_principal'

class PantallaBusqueda(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'busqueda'
        self.app = app
        self.resultados_actuales = []
        self.construir_interfaz()

    def construir_interfaz(self):
        tr = TEXTOS[self.app.idioma]
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=tr["search_title"], font_size=dp(22), bold=True, size_hint_y=None, height=dp(40)))
        self.textinput = TextInput(
            hint_text=tr["search_hint"],
            size_hint_y=None,
            height=dp(45),
            multiline=False,
            font_size=dp(16)
        )
        self.textinput.bind(on_text_validate=self.buscar)
        layout.add_widget(self.textinput)
        btn_buscar = Button(text=tr["search_btn"], size_hint_y=None, height=dp(45))
        btn_buscar.bind(on_press=self.buscar)
        layout.add_widget(btn_buscar)
        self.scroll = ScrollView()
        self.resultados_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.resultados_layout.bind(minimum_height=self.resultados_layout.setter('height'))
        self.scroll.add_widget(self.resultados_layout)
        layout.add_widget(self.scroll)
        self.btn_enviar = Button(
            text=tr["send_summary"],
            size_hint_y=None,
            height=dp(45),
            background_color=(0.1, 0.6, 0.1, 1),
            color=(1, 1, 1, 1),
            opacity=0,
            disabled=True
        )
        self.btn_enviar.bind(on_press=self.enviar_resumen)
        layout.add_widget(self.btn_enviar)
        btn_volver = Button(text=tr["back_menu"], size_hint_y=None, height=dp(45))
        btn_volver.bind(on_press=self.volver_menu)
        layout.add_widget(btn_volver)
        self.add_widget(layout)

    def buscar(self, instance):
        palabra = self.textinput.text.strip().lower()
        self.resultados_layout.clear_widgets()
        self.resultados_actuales = []
        self.btn_enviar.opacity = 0
        self.btn_enviar.disabled = True
        if not palabra:
            self.resultados_layout.add_widget(Label(text=TEXTOS[self.app.idioma]["search_hint"], font_size=dp(15)))
            return
        resultados = []
        resultados += [{"tipo": "fundamental", "titulo": tema['titulo'][self.app.idioma], "detalle": tema}
                       for tema in cargar_todos_los_temas()
                       if palabra in tema['titulo'][self.app.idioma].lower() or palabra in tema.get('contenido', {}).get(self.app.idioma, '').lower()]
        resultados += [{"tipo": "profundo", "titulo": tema['titulo'][self.app.idioma], "detalle": tema}
                       for tema in cargar_temas_profundos()
                       if palabra in tema['titulo'][self.app.idioma].lower() or palabra in tema.get('contenido', {}).get(self.app.idioma, '').lower()]
        self.resultados_actuales = resultados
        if resultados:
            for res in resultados:
                color = (0.2, 0.4, 0.6, 1) if res['tipo'] == 'fundamental' else (0.5, 0.2, 0.4, 1)
                btn = crear_boton_multilinea(
                    res['titulo'],
                    color,
                    lambda inst, t=res['detalle'], tipo=res['tipo']: self.mostrar_detalle_tema(t, tipo)
                )
                self.resultados_layout.add_widget(btn)
            self.btn_enviar.opacity = 1
            self.btn_enviar.disabled = False
        else:
            self.resultados_layout.add_widget(Label(text=TEXTOS[self.app.idioma]["no_results"], font_size=dp(15)))
            self.btn_enviar.opacity = 0
            self.btn_enviar.disabled = True

    def enviar_resumen(self, instance):
        resumen = self.generar_resumen()
        self.mostrar_popup_resumen(resumen)

    def generar_resumen(self):
        idioma = self.app.idioma
        resumen = ""
        for res in self.resultados_actuales:
            tema = res['detalle']
            resumen += f"\n• {tema['titulo'][idioma]}\n"
            if 'contenido' in tema:
                resumen += f"{tema['contenido'][idioma]}\n"
            if 'respuesta' in tema:
                resumen += f"{tema['respuesta'][idioma]}\n"
            if 'conclusion' in tema:
                resumen += f"{tema['conclusion'][idioma]}\n"
        return resumen.strip()

    def mostrar_popup_resumen(self, resumen):
        tr = TEXTOS[self.app.idioma]
        box = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        box.add_widget(Label(text=tr["summary_ready"], font_size=dp(16), bold=True, size_hint_y=None, height=dp(30)))
        resumen_label = TextInput(text=resumen, readonly=True, size_hint_y=None, height=dp(220), font_size=dp(13))
        box.add_widget(resumen_label)
        btn_copiar = Button(text="Copiar al portapapeles", size_hint_y=None, height=dp(40))
        btn_copiar.bind(on_press=lambda x: Clipboard.copy(resumen))
        box.add_widget(btn_copiar)
        btn_whatsapp = Button(text="Compartir por WhatsApp", size_hint_y=None, height=dp(40))
        btn_whatsapp.bind(on_press=lambda x: webbrowser.open("https://wa.me/?text=" + urllib.parse.quote(resumen)))
        box.add_widget(btn_whatsapp)
        btn_email = Button(text="Enviar por Email", size_hint_y=None, height=dp(40))
        btn_email.bind(on_press=lambda x: webbrowser.open("mailto:?subject=Temas%20bíblicos&body=" + urllib.parse.quote(resumen)))
        box.add_widget(btn_email)
        btn_cerrar = Button(text=tr["close"], size_hint_y=None, height=dp(40))
        popup = Popup(title=tr["summary_ready"], content=box, size_hint=(0.98, 0.85))
        btn_cerrar.bind(on_press=popup.dismiss)
        box.add_widget(btn_cerrar)
        popup.open()

    def mostrar_detalle_tema(self, tema, tipo):
        tr = TEXTOS[self.app.idioma]
        idioma = self.app.idioma
        contenido = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(8))
        contenido.bind(minimum_height=contenido.setter('height'))

        # Título
        contenido.add_widget(crear_label(tema['titulo'][idioma], font_size=17, bold=True))

        # Contenido principal o respuesta
        if 'contenido' in tema:
            contenido.add_widget(crear_label(tema['contenido'][idioma], font_size=15))
        elif 'respuesta' in tema:
            contenido.add_widget(crear_label(tema['respuesta'][idioma], font_size=15))

        # Cita y link
        if 'cita' in tema:
            contenido.add_widget(crear_label(f"Cita: {tema['cita']}", font_size=13))
        if 'link' in tema:
            btn_jw = Button(text="JW.ORG", size_hint_y=None, height=dp(35))
            btn_jw.bind(on_press=lambda x: self.abrir_link(tema['link']))
            contenido.add_widget(btn_jw)

        # Argumentos, secciones, versículos, enlaces (si existen)
        if 'argumentos' in tema:
            if 'argumentos_biblicos' in tema['argumentos']:
                contenido.add_widget(crear_label("Argumentos bíblicos:", font_size=14, bold=True))
                for arg in tema['argumentos']['argumentos_biblicos']:
                    contenido.add_widget(crear_label(f"- {arg['titulo'][idioma]} ({arg.get('cita','')})", font_size=13, bold=True))
                    contenido.add_widget(crear_label(arg['texto'][idioma], font_size=12))
            if 'argumentos_logicos' in tema['argumentos']:
                contenido.add_widget(crear_label("Argumentos lógicos:", font_size=14, bold=True))
                for arg in tema['argumentos']['argumentos_logicos']:
                    contenido.add_widget(crear_label(f"- {arg['titulo'][idioma]}", font_size=13, bold=True))
                    contenido.add_widget(crear_label(arg['explicacion'][idioma], font_size=12))
            if 'argumentos_historicos' in tema['argumentos']:
                contenido.add_widget(crear_label("Argumentos históricos:", font_size=14, bold=True))
                for arg in tema['argumentos']['argumentos_historicos']:
                    contenido.add_widget(crear_label(f"- {arg['titulo'][idioma]}", font_size=13, bold=True))
                    contenido.add_widget(crear_label(arg['descripcion'][idioma], font_size=12))
            if 'fuentes_recomendadas' in tema['argumentos']:
                contenido.add_widget(crear_label("Fuentes recomendadas:", font_size=14, bold=True))
                for fuente in tema['argumentos']['fuentes_recomendadas']:
                    btn_f = Button(text=fuente, size_hint_y=None, height=dp(30), font_size=dp(12))
                    btn_f.bind(on_press=lambda x, url=fuente: self.abrir_link(url))
                    contenido.add_widget(btn_f)

        if 'secciones' in tema:
            for seccion in tema['secciones']:
                contenido.add_widget(crear_label(seccion['subtitulo'][idioma], font_size=13, bold=True))
                for parrafo in seccion['parrafos']:
                    texto = parrafo.get(idioma, str(parrafo)) if isinstance(parrafo, dict) else str(parrafo)
                    contenido.add_widget(crear_label(texto, font_size=12))

        if 'versiculos' in tema:
            contenido.add_widget(crear_label("Versículos:", font_size=14, bold=True))
            for vers in tema['versiculos']:
                contenido.add_widget(crear_label(vers, font_size=12))

        if 'enlaces' in tema:
            contenido.add_widget(crear_label("Enlaces recomendados:", font_size=14, bold=True))
            for link in tema['enlaces']:
                btn_link = Button(text=link, size_hint_y=None, height=dp(30), font_size=dp(12))
                btn_link.bind(on_press=lambda x, url=link: self.abrir_link(url))
                contenido.add_widget(btn_link)

        if 'conclusion' in tema:
            contenido.add_widget(crear_label(tr["conclusion"], font_size=14, bold=True))
            contenido.add_widget(crear_label(tema['conclusion'][idioma], font_size=13))

        if 'copyright' in tema:
            contenido.add_widget(crear_label(tema['copyright'][idioma], font_size=10))

        # --- Botón Copiar ---
        texto_a_copiar = ""
        for widget in contenido.children[::-1]:
            if isinstance(widget, Label):
                texto_a_copiar += widget.text.replace('[b]', '').replace('[/b]', '') + "\n"
        btn_copiar = Button(text="Copiar", size_hint_y=None, height=dp(40))
        btn_copiar.bind(on_press=lambda x: Clipboard.copy(texto_a_copiar.strip()))
        # --------------------

        btn_cerrar = Button(text=tr["close"], size_hint_y=None, height=dp(40))
        popup_layout = BoxLayout(orientation='vertical')
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(contenido)
        popup_layout.add_widget(scroll)
        popup_layout.add_widget(btn_copiar)
        popup_layout.add_widget(btn_cerrar)
        popup = Popup(title=tema['titulo'][idioma], content=popup_layout, size_hint=(0.98, 0.98))
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def abrir_link(self, url):
        webbrowser.open(url)

    def volver_menu(self, instance):
        self.manager.current = 'menu_principal'

class ExploraLaVerdadApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idioma = "es"
        self.sm = ScreenManager()

    def build(self):
        self.sm.add_widget(PantallaIdioma(self))
        self.sm.current = 'idioma'
        return self.sm

    def cargar_pantallas(self):
        for s in list(self.sm.screen_names):
            if s != "idioma":
                self.sm.remove_widget(self.sm.get_screen(s))
        self.sm.add_widget(PantallaAvisoLegal(self))
        self.sm.add_widget(PantallaMenuPrincipal(self))
        self.sm.add_widget(PantallaBusqueda(self))
        self.sm.add_widget(PantallaTemasFundamentales(self))
        self.sm.add_widget(PantallaTemasProfundos(self))

if __name__ == '__main__':
    ExploraLaVerdadApp().run()
