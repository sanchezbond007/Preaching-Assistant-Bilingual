# ===== SEND_RESUME.PY - PARTE 1: CONFIGURACIÓN E IMPORTS =====
# Guarda esto como: pantallas/send_resume.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.app import App
import json
import os
import webbrowser
import urllib.parse
from datetime import datetime

# === CONFIGURACIÓN DE LINKS JW SEGÚN IDIOMA ===
LINKS_JW = {
    'es': {
        'jw_library': 'https://www.jw.org/es/biblioteca-en-linea/libros/',
        'solicitar_estudio': 'https://www.jw.org/es/testigos-de-jehova/solicitar-visita/',
        'jw_org': 'https://www.jw.org/es/',
        'watchtower': 'https://www.jw.org/es/biblioteca-en-linea/revistas/torre-del-vigia/',
        'bible': 'https://www.jw.org/es/biblioteca-en-linea/biblia/'
    },
    'en': {
        'jw_library': 'https://www.jw.org/en/library/books/',
        'solicitar_estudio': 'https://www.jw.org/en/jehovahs-witnesses/request-a-visit/',
        'jw_org': 'https://www.jw.org/en/',
        'watchtower': 'https://www.jw.org/en/library/magazines/watchtower/',
        'bible': 'https://www.jw.org/en/library/bible/'
    }
}

# === PLANTILLAS DE MENSAJES ===
PLANTILLAS_SALUDO = {
    'es': {
        'formal': 'Estimado/a',
        'amigable': 'Querido/a',
        'hermano': 'Hermano/a',
        'amigo': 'Estimado/a amigo/a'
    },
    'en': {
        'formal': 'Dear',
        'amigable': 'Dear friend',
        'hermano': 'Dear brother/sister',
        'amigo': 'Dear friend'
    }
}

PLANTILLAS_DESPEDIDA = {
    'es': {
        'esperanza': '¡Esperamos que esta información le sea útil en su búsqueda espiritual!',
        'bendicion': '¡Que Jehová bendiga su búsqueda de la verdad!',
        'crecimiento': '¡Esperamos seguir creciendo juntos en conocimiento bíblico!'
    },
    'en': {
        'esperanza': 'We hope this information will be useful in your spiritual search!',
        'bendicion': 'May Jehovah bless your search for truth!',
        'crecimiento': 'We hope to continue growing together in biblical knowledge!'
    }
}

PLANTILLAS_FIRMA = {
    'es': {
        'cristiano': 'Con cariño cristiano',
        'hermano': 'Su hermano/a en la fe',
        'amigo': 'Su amigo/a sincero/a',
        'servidor': 'Su servidor en Cristo'
    },
    'en': {
        'cristiano': 'With Christian love',
        'hermano': 'Your brother/sister in faith',
        'amigo': 'Your sincere friend',
        'servidor': 'Your servant in Christ'
    }
}

print("✅ SEND_RESUME PARTE 1 - Configuración cargada")

# ===== SEND_RESUME.PY - PARTE 2: CLASE PRINCIPAL Y TEXTOS =====

class PantallaSendResume(Screen):
    """Pantalla para enviar resumen personalizado de temas al interesado"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'send_resume'
        self.idioma_actual = 'es'
        self.volver_callback = None
        
        # === DATOS DEL INTERESADO ===
        self.interesado_actual = "Interesado"
        self.temas_mostrados = []           # Lista de temas específicos del interesado
        self.temas_sesion_actual = []       # Temas de la sesión actual
        
        # === CONFIGURACIÓN DE MENSAJE ===
        self.tipo_saludo = 'formal'         # formal, amigable, hermano, amigo
        self.tipo_despedida = 'esperanza'   # esperanza, bendicion, crecimiento
        self.tipo_firma = 'cristiano'       # cristiano, hermano, amigo, servidor
        
        # === TEXTOS MULTIIDIOMA ===
        self.textos = {
            'es': {
                'titulo': '📤 Enviar Resumen al Interesado',
                'subtitulo': 'Comparte los temas bíblicos estudiados',
                'nombre_titulo': 'Nombre del interesado:',
                'nombre_placeholder': 'Escribe el nombre del interesado...',
                'contenido_titulo': 'Resumen personalizado que se enviará:',
                'btn_email': '📧 Enviar por Email',
                'btn_whatsapp': '💬 Enviar por WhatsApp',
                'btn_sms': '📱 Enviar por SMS',
                'btn_volver': '🔙 Volver al Menú',
                'btn_actualizar': '🔄 Actualizar Resumen',
                'sin_datos': 'No hay temas registrados para este interesado.',
                'cargando': 'Cargando temas del interesado...',
                'temas_encontrados': 'temas encontrados',
                'tema_unico': 'tema encontrado',
                'sin_interesado': 'Por favor, ingresa el nombre del interesado.',
                'resumen_actualizado': 'Resumen actualizado exitosamente',
                'error_actualizacion': 'Error actualizando el resumen'
            },
            'en': {
                'titulo': '📤 Send Resume to Interested Person',
                'subtitulo': 'Share the studied biblical topics',
                'nombre_titulo': 'Interested person name:',
                'nombre_placeholder': 'Enter the interested person name...',
                'contenido_titulo': 'Personalized resume to be sent:',
                'btn_email': '📧 Send via Email',
                'btn_whatsapp': '💬 Send via WhatsApp',
                'btn_sms': '📱 Send via SMS',
                'btn_volver': '🔙 Back to Menu',
                'btn_actualizar': '🔄 Update Resume',
                'sin_datos': 'No topics recorded for this interested person.',
                'cargando': 'Loading interested person topics...',
                'temas_encontrados': 'topics found',
                'tema_unico': 'topic found',
                'sin_interesado': 'Please enter the interested person name.',
                'resumen_actualizado': 'Resume updated successfully',
                'error_actualizacion': 'Error updating resume'
            }
        }
        
        # === INICIALIZACIÓN ===
        print("🏗️ Inicializando PantallaSendResume...")
        self.construir_interfaz()
        self.cargar_datos_automaticos()
        
    def obtener_texto(self, clave):
        """Obtener texto en el idioma actual"""
        return self.textos[self.idioma_actual].get(clave, f'[{clave}]')
    
    # === MÉTODOS DE CONFIGURACIÓN ===
    def establecer_interesado(self, nombre):
        """Establecer el interesado actual y cargar sus datos"""
        try:
            if nombre and nombre.strip():
                self.interesado_actual = nombre.strip().title()
                print(f"👥 Interesado establecido: {self.interesado_actual}")
                
                # Actualizar campo de texto si existe
                if hasattr(self, 'input_nombre'):
                    self.input_nombre.text = self.interesado_actual
                
                # Cargar datos del interesado
                self.cargar_datos_interesado()
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error estableciendo interesado: {e}")
            return False
    
    def actualizar_temas(self, lista_temas):
        """Actualizar la lista de temas del interesado"""
        try:
            self.temas_mostrados = lista_temas or []
            print(f"📚 Temas actualizados: {len(self.temas_mostrados)} temas")
            
            # Regenerar resumen
            self.generar_resumen_personalizado()
            
        except Exception as e:
            print(f"❌ Error actualizando temas: {e}")
    
    def configurar_estilo_mensaje(self, saludo='formal', despedida='esperanza', firma='cristiano'):
        """Configurar el estilo del mensaje"""
        try:
            self.tipo_saludo = saludo
            self.tipo_despedida = despedida
            self.tipo_firma = firma
            
            print(f"✅ Estilo configurado: {saludo}/{despedida}/{firma}")
            
            # Regenerar resumen con nuevo estilo
            self.generar_resumen_personalizado()
            
        except Exception as e:
            print(f"❌ Error configurando estilo: {e}")

print("✅ SEND_RESUME PARTE 2 - Clase principal y textos completada")

	# ===== SEND_RESUME.PY - PARTE 3: CONSTRUCCIÓN DE INTERFAZ =====

    def construir_interfaz(self):
        """Construir la interfaz completa de la pantalla"""
        try:
            print("🏗️ Construyendo interfaz de envío de resumen...")
            
            # Layout principal
            layout_principal = BoxLayout(
                orientation='vertical',
                padding=dp(20),
                spacing=dp(15)
            )
            
            # Agregar fondo
            self.agregar_fondo()
            
            # Construir secciones
            self.agregar_header(layout_principal)
            self.agregar_seccion_interesado(layout_principal)
            self.agregar_seccion_resumen(layout_principal)
            self.agregar_botones_envio(layout_principal)
            self.agregar_botones_control(layout_principal)
            
            # Agregar layout principal a la pantalla
            self.add_widget(layout_principal)
            
            print("✅ Interfaz de envío de resumen construida")
            
        except Exception as e:
            print(f"❌ Error construyendo interfaz: {e}")
    
    def agregar_fondo(self):
        """Agregar fondo coloreado"""
        try:
            with self.canvas.before:
                Color(0.95, 0.95, 0.95, 1)  # Gris claro
                self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._actualizar_rect, pos=self._actualizar_rect)
            
        except Exception as e:
            print(f"⚠️ Error agregando fondo: {e}")
    
    def _actualizar_rect(self, *args):
        """Actualizar rectángulo de fondo"""
        try:
            if hasattr(self, 'rect'):
                self.rect.pos = self.pos
                self.rect.size = self.size
        except:
            pass
    
    def agregar_header(self, layout_principal):
        """Agregar sección de encabezado"""
        try:
            # Layout del header
            header_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(100),
                spacing=dp(5)
            )
            
            # Título principal
            self.lbl_titulo = Label(
                text=self.obtener_texto('titulo'),
                font_size='22sp',
                size_hint_y=None,
                height=dp(50),
                color=(0.1, 0.1, 0.1, 1),
                bold=True,
                halign='center'
            )
            
            # Subtítulo
            self.lbl_subtitulo = Label(
                text=self.obtener_texto('subtitulo'),
                font_size='16sp',
                size_hint_y=None,
                height=dp(35),
                color=(0.3, 0.3, 0.3, 1),
                halign='center'
            )
            
            header_layout.add_widget(self.lbl_titulo)
            header_layout.add_widget(self.lbl_subtitulo)
            layout_principal.add_widget(header_layout)
            
            print("  ✓ Header agregado")
            
        except Exception as e:
            print(f"❌ Error agregando header: {e}")
    
    def agregar_seccion_interesado(self, layout_principal):
        """Agregar sección para nombre del interesado"""
        try:
            # Label para nombre
            self.lbl_nombre_titulo = Label(
                text=self.obtener_texto('nombre_titulo'),
                font_size='16sp',
                size_hint_y=None,
                height=dp(30),
                color=(0.1, 0.1, 0.1, 1),
                bold=True,
                halign='left'
            )
            self.lbl_nombre_titulo.text_size = (None, None)
            layout_principal.add_widget(self.lbl_nombre_titulo)
            
            # Layout horizontal para input y botón actualizar
            input_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(40),
                spacing=dp(10)
            )
            
            # Campo de texto para nombre
            self.input_nombre = TextInput(
                text=self.interesado_actual,
                hint_text=self.obtener_texto('nombre_placeholder'),
                multiline=False,
                font_size='16sp',
                size_hint_x=0.7
            )
            self.input_nombre.bind(text=self.on_nombre_cambiado)
            
            # Botón actualizar
            self.btn_actualizar = Button(
                text=self.obtener_texto('btn_actualizar'),
                background_color=(0.3, 0.6, 0.9, 1),
                size_hint_x=0.3,
                font_size='14sp'
            )
            self.btn_actualizar.bind(on_press=self.actualizar_resumen_manual)
            
            input_layout.add_widget(self.input_nombre)
            input_layout.add_widget(self.btn_actualizar)
            layout_principal.add_widget(input_layout)
            
            print("  ✓ Sección interesado agregada")
            
        except Exception as e:
            print(f"❌ Error agregando sección interesado: {e}")
    
    def agregar_seccion_resumen(self, layout_principal):
        """Agregar sección del resumen"""
        try:
            # Label título del resumen
            self.lbl_contenido_titulo = Label(
                text=self.obtener_texto('contenido_titulo'),
                font_size='16sp',
                size_hint_y=None,
                height=dp(30),
                color=(0.1, 0.1, 0.1, 1),
                bold=True,
                halign='left'
            )
            self.lbl_contenido_titulo.text_size = (None, None)
            layout_principal.add_widget(self.lbl_contenido_titulo)
            
            # ScrollView para el resumen
            scroll = ScrollView()
            
            self.lbl_resumen = Label(
                text=self.obtener_texto('cargando'),
                font_size='14sp',
                text_size=(None, None),
                halign='left',
                valign='top',
                color=(0.2, 0.2, 0.2, 1),
                markup=True  # Permitir formato básico
            )
            
            scroll.add_widget(self.lbl_resumen)
            layout_principal.add_widget(scroll)
            
            print("  ✓ Sección resumen agregada")
            
        except Exception as e:
            print(f"❌ Error agregando sección resumen: {e}")
    
    def agregar_botones_envio(self, layout_principal):
        """Agregar botones de envío (email, WhatsApp, SMS)"""
        try:
            # Layout para botones de envío
            botones_layout = BoxLayout(
                orientation='vertical',
                spacing=dp(10),
                size_hint_y=None,
                height=dp(180)
            )
            
            # Botón Email
            self.btn_email = Button(
                text=self.obtener_texto('btn_email'),
                background_color=(0.2, 0.6, 0.9, 1),  # Azul
                size_hint_y=None,
                height=dp(50),
                font_size='16sp',
                bold=True
            )
            self.btn_email.bind(on_press=self.enviar_por_email)
            
            # Botón WhatsApp
            self.btn_whatsapp = Button(
                text=self.obtener_texto('btn_whatsapp'),
                background_color=(0.1, 0.7, 0.3, 1),  # Verde
                size_hint_y=None,
                height=dp(50),
                font_size='16sp',
                bold=True
            )
            self.btn_whatsapp.bind(on_press=self.enviar_por_whatsapp)
            
            # Botón SMS
            self.btn_sms = Button(
                text=self.obtener_texto('btn_sms'),
                background_color=(0.9, 0.5, 0.1, 1),  # Naranja
                size_hint_y=None,
                height=dp(50),
                font_size='16sp',
                bold=True
            )
            self.btn_sms.bind(on_press=self.enviar_por_sms)
            
            # Agregar botones
            botones_layout.add_widget(self.btn_email)
            botones_layout.add_widget(self.btn_whatsapp)
            botones_layout.add_widget(self.btn_sms)
            
            layout_principal.add_widget(botones_layout)
            
            print("  ✓ Botones de envío agregados")
            
        except Exception as e:
            print(f"❌ Error agregando botones de envío: {e}")
    
    def agregar_botones_control(self, layout_principal):
        """Agregar botones de control (volver)"""
        try:
            # Espaciador
            layout_principal.add_widget(
                Label(size_hint_y=None, height=dp(10), text="")
            )
            
            # Botón volver
            self.btn_volver = Button(
                text=self.obtener_texto('btn_volver'),
                background_color=(0.6, 0.3, 0.3, 1),  # Rojo suave
                size_hint_y=None,
                height=dp(50),
                font_size='16sp',
                bold=True
            )
            self.btn_volver.bind(on_press=self.volver_menu)
            
            layout_principal.add_widget(self.btn_volver)
            
            print("  ✓ Botones de control agregados")
            
        except Exception as e:
            print(f"❌ Error agregando botones de control: {e}")

print("✅ SEND_RESUME PARTE 3 - Construcción de interfaz completada")

	# ===== SEND_RESUME.PY - PARTE 4: CARGA DE DATOS Y GENERACIÓN DE RESUMEN =====

    # === MÉTODOS DE CARGA DE DATOS ===
    def cargar_datos_automaticos(self):
        """Cargar datos automáticamente al inicializar"""
        try:
            print("📂 Cargando datos automáticos...")
            
            # Obtener interesado actual de la app
            self.obtener_interesado_desde_app()
            
            # Cargar datos del interesado
            self.cargar_datos_interesado()
            
        except Exception as e:
            print(f"❌ Error cargando datos automáticos: {e}")
    
    def obtener_interesado_desde_app(self):
        """Obtener el interesado actual desde la aplicación"""
        try:
            app = App.get_running_app()
            
            # Intentar obtener desde la app
            if hasattr(app, 'interesado_actual') and app.interesado_actual:
                self.interesado_actual = app.interesado_actual
                print(f"👥 Interesado obtenido desde app: {self.interesado_actual}")
                return
            
            # Buscar en archivos de historial
            self.buscar_interesado_en_historial()
            
        except Exception as e:
            print(f"⚠️ Error obteniendo interesado desde app: {e}")
    
    def buscar_interesado_en_historial(self):
        """Buscar el último interesado en el historial"""
        try:
            # Buscar en historial de interesados
            if os.path.exists('historial_interesados.json'):
                with open('historial_interesados.json', 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    historial_completo = datos.get('historial_completo', [])
                    
                    if historial_completo:
                        # Obtener el más reciente
                        ultimo_registro = historial_completo[-1]
                        interesado = ultimo_registro.get('interesado', 'Interesado')
                        self.interesado_actual = interesado
                        print(f"👥 Último interesado encontrado: {interesado}")
                        return
            
            # Fallback: buscar en estudiantes.json
            self.buscar_en_estudiantes_json()
            
        except Exception as e:
            print(f"⚠️ Error buscando en historial: {e}")
            self.interesado_actual = "Interesado"
    
    def buscar_en_estudiantes_json(self):
        """Buscar interesado en archivo estudiantes.json (fallback)"""
        try:
            if os.path.exists('estudiantes.json'):
                with open('estudiantes.json', 'r', encoding='utf-8') as f:
                    estudiantes = json.load(f)
                    
                    if estudiantes and len(estudiantes) > 0:
                        # Tomar el primer estudiante como fallback
                        primer_estudiante = estudiantes[0]
                        nombre = primer_estudiante.get('nombre', 'Interesado')
                        self.interesado_actual = nombre
                        print(f"👥 Interesado desde estudiantes.json: {nombre}")
            
        except Exception as e:
            print(f"⚠️ Error buscando en estudiantes.json: {e}")
    
    def cargar_datos_interesado(self):
        """Cargar todos los temas del interesado actual"""
        try:
            print(f"📚 Cargando datos para: {self.interesado_actual}")
            
            # Limpiar datos anteriores
            self.temas_mostrados = []
            
            # Cargar desde historial de interesados
            self.cargar_desde_historial_interesados()
            
            # Cargar desde estudiantes.json (fallback)
            if not self.temas_mostrados:
                self.cargar_desde_estudiantes_json()
            
            # Generar resumen
            self.generar_resumen_personalizado()
            
            print(f"✅ Datos cargados: {len(self.temas_mostrados)} temas encontrados")
            
        except Exception as e:
            print(f"❌ Error cargando datos del interesado: {e}")
            self.generar_resumen_sin_datos()
    
    def cargar_desde_historial_interesados(self):
        """Cargar temas desde historial_interesados.json"""
        try:
            if not os.path.exists('historial_interesados.json'):
                return
            
            with open('historial_interesados.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)
                temas_por_interesado = datos.get('temas_por_interesado', {})
                
                # Buscar temas del interesado actual
                nombre_normalizado = self.interesado_actual.strip().title()
                
                for nombre, temas in temas_por_interesado.items():
                    if nombre.lower() == nombre_normalizado.lower():
                        self.temas_mostrados = temas
                        print(f"📖 Temas cargados desde historial: {len(temas)} temas")
                        break
                
        except Exception as e:
            print(f"⚠️ Error cargando desde historial de interesados: {e}")
    
    def cargar_desde_estudiantes_json(self):
        """Cargar temas desde estudiantes.json (fallback)"""
        try:
            if not os.path.exists('estudiantes.json'):
                return
            
            with open('estudiantes.json', 'r', encoding='utf-8') as f:
                estudiantes = json.load(f)
                
                # Buscar estudiante que coincida
                for estudiante in estudiantes:
                    nombre = estudiante.get('nombre', '')
                    if nombre.lower() == self.interesado_actual.lower():
                        historial = estudiante.get('historial', [])
                        
                        # Convertir formato si es necesario
                        self.temas_mostrados = []
                        for item in historial:
                            tema_formateado = {
                                'termino': item.get('termino', ''),
                                'timestamp': item.get('timestamp', ''),
                                'resultado': item.get('resultado', 'Tema estudiado'),
                                'interesado': self.interesado_actual
                            }
                            self.temas_mostrados.append(tema_formateado)
                        
                        print(f"📖 Temas cargados desde estudiantes.json: {len(self.temas_mostrados)} temas")
                        break
                
        except Exception as e:
            print(f"⚠️ Error cargando desde estudiantes.json: {e}")
    
    # === MÉTODOS DE GENERACIÓN DE RESUMEN ===
    def generar_resumen_personalizado(self):
        """Generar resumen personalizado con los temas del interesado"""
        try:
            print(f"📝 Generando resumen para {self.interesado_actual}...")
            
            if not self.temas_mostrados:
                self.generar_resumen_sin_datos()
                return
            
            # Obtener plantillas según idioma
            saludos = PLANTILLAS_SALUDO[self.idioma_actual]
            despedidas = PLANTILLAS_DESPEDIDA[self.idioma_actual]
            firmas = PLANTILLAS_FIRMA[self.idioma_actual]
            links = LINKS_JW[self.idioma_actual]
            
            # Construir saludo
            saludo = saludos.get(self.tipo_saludo, saludos['formal'])
            nombre = self.interesado_actual if self.interesado_actual != "Interesado" else ""
            
            # Encabezado del mensaje
            if self.idioma_actual == 'es':
                resumen = f"""🌟 {saludo} {nombre},

Esperamos que se encuentre bien. Nos complace compartir con usted un resumen de los temas bíblicos que hemos estado considerando juntos:

📚 TEMAS ESTUDIADOS:
"""
            else:
                resumen = f"""🌟 {saludo} {nombre},

We hope you are well. We are pleased to share with you a summary of the biblical topics we have been considering together:

📚 STUDIED TOPICS:
"""
            
            # Agregar temas únicos
            temas_unicos = self.obtener_temas_unicos()
            
            for i, tema in enumerate(temas_unicos[:15], 1):  # Máximo 15 temas
                resumen += f"{i}. {tema}\n"
            
            # Agregar información adicional si hay muchos temas
            if len(self.temas_mostrados) > 15:
                diferencia = len(self.temas_mostrados) - 15
                if self.idioma_actual == 'es':
                    resumen += f"... y {diferencia} temas más que hemos explorado juntos.\n"
                else:
                    resumen += f"... and {diferencia} more topics we have explored together.\n"
            
            # Agregar recursos JW
            if self.idioma_actual == 'es':
                resumen += f"""
📖 RECURSOS ÚTILES PARA CONTINUAR ESTUDIANDO:
• JW Library (Biblioteca bíblica): {links['jw_library']}
• Solicitar un estudio bíblico gratuito: {links['solicitar_estudio']}

{despedidas.get(self.tipo_despedida, despedidas['esperanza'])}

{firmas.get(self.tipo_firma, firmas['cristiano'])},
Su hermano/a en la fe
"""
            else:
                resumen += f"""
📖 USEFUL RESOURCES TO CONTINUE STUDYING:
• JW Library (Biblical library): {links['jw_library']}
• Request a free Bible study: {links['solicitar_estudio']}

{despedidas.get(self.tipo_despedida, despedidas['esperanza'])}

{firmas.get(self.tipo_firma, firmas['cristiano'])},
Your brother/sister in faith
"""
            
            # Actualizar label del resumen
            self.lbl_resumen.text = resumen
            self.lbl_resumen.text_size = (None, None)
            
            print(f"✅ Resumen generado: {len(temas_unicos)} temas únicos")
            
        except Exception as e:
            print(f"❌ Error generando resumen: {e}")
            self.generar_resumen_sin_datos()
    
    def obtener_temas_unicos(self):
        """Obtener lista de temas únicos del interesado"""
        try:
            temas_set = set()
            
            for tema_obj in self.temas_mostrados:
                termino = tema_obj.get('termino', '').strip()
                if termino and len(termino) > 1:
                    # Limpiar y normalizar el término
                    termino_limpio = termino.title()
                    temas_set.add(termino_limpio)
            
            # Convertir a lista y ordenar
            temas_unicos = sorted(list(temas_set))
            
            return temas_unicos
            
        except Exception as e:
            print(f"❌ Error obteniendo temas únicos: {e}")
            return []
    
    def generar_resumen_sin_datos(self):
        """Generar resumen cuando no hay datos del interesado"""
        try:
            links = LINKS_JW[self.idioma_actual]
            
            if self.idioma_actual == 'es':
                resumen = f"""🌟 Estimado/a {self.interesado_actual},

Esperamos que se encuentre bien. Aunque aún no hemos registrado temas específicos en nuestro sistema, nos gustaría invitarle a explorar estos recursos bíblicos:

📖 RECURSOS RECOMENDADOS:
• JW Library (Biblioteca bíblica): {links['jw_library']}
• Solicitar un estudio bíblico gratuito: {links['solicitar_estudio']}
• Sitio web oficial: {links['jw_org']}

¡Estaremos encantados de estudiar la Biblia juntos!

Con cariño cristiano,
Su hermano/a en la fe
"""
            else:
                resumen = f"""🌟 Dear {self.interesado_actual},

We hope you are well. Although we haven't recorded specific topics in our system yet, we would like to invite you to explore these biblical resources:

📖 RECOMMENDED RESOURCES:
• JW Library (Biblical library): {links['jw_library']}
• Request a free Bible study: {links['solicitar_estudio']}
• Official website: {links['jw_org']}

We would be delighted to study the Bible together!

With Christian love,
Your brother/sister in faith
"""
            
            self.lbl_resumen.text = resumen
            self.lbl_resumen.text_size = (None, None)
            
        except Exception as e:
            print(f"❌ Error generando resumen sin datos: {e}")
            self.lbl_resumen.text = self.obtener_texto('sin_datos')
    
    # === CALLBACKS DE EVENTOS DE INTERFAZ ===
    def on_nombre_cambiado(self, instance, value):
        """Callback cuando cambia el nombre del interesado"""
        try:
            nombre_anterior = self.interesado_actual
            nuevo_nombre = value.strip().title()
            
            if nuevo_nombre != nombre_anterior and len(nuevo_nombre) > 0:
                print(f"👥 Nombre cambiado: {nombre_anterior} → {nuevo_nombre}")
                self.interesado_actual = nuevo_nombre
                
                # Recargar datos del nuevo interesado
                self.cargar_datos_interesado()
            
        except Exception as e:
            print(f"❌ Error al cambiar nombre: {e}")
    
    def actualizar_resumen_manual(self, instance):
        """Callback para el botón de actualizar resumen"""
        try:
            print("🔄 Actualizando resumen manualmente...")
            
            # Validar nombre del interesado
            nombre = self.input_nombre.text.strip()
            if not nombre:
                print("⚠️ Nombre vacío")
                return
            
            # Establecer nuevo interesado
            self.interesado_actual = nombre.title()
            
            # Recargar datos
            self.cargar_datos_interesado()
            
            print(f"✅ Resumen actualizado para: {self.interesado_actual}")
            
        except Exception as e:
            print(f"❌ Error actualizando resumen manual: {e}")

print("✅ SEND_RESUME PARTE 4 - Carga de datos y generación completada")

	# ===== SEND_RESUME.PY - PARTE 5: CALLBACKS Y ENVÍO DE MENSAJES =====

    # === MÉTODOS DE ENVÍO ===
    def enviar_por_email(self, instance):
        """Enviar resumen por email usando mailto"""
        try:
            print(f"📧 Enviando por email para {self.interesado_actual}...")
            
            # Validar que hay contenido
            if not self.lbl_resumen.text or self.lbl_resumen.text.strip() == "":
                print("⚠️ No hay contenido para enviar")
                return
            
            # Crear asunto del email
            if self.idioma_actual == 'es':
                asunto = f"Temas bíblicos para {self.interesado_actual}"
            else:
                asunto = f"Biblical topics for {self.interesado_actual}"
            
            # Obtener contenido del resumen
            cuerpo = self.lbl_resumen.text
            
            # Crear URL mailto
            url = f"mailto:?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
            
            # Abrir cliente de email
            webbrowser.open(url)
            
            print(f"✅ Cliente de email abierto para {self.interesado_actual}")
            
            # Registrar envío
            self.registrar_envio('email')
            
        except Exception as e:
            print(f"❌ Error enviando por email: {e}")
    
    def enviar_por_whatsapp(self, instance):
        """Enviar resumen por WhatsApp"""
        try:
            print(f"💬 Enviando por WhatsApp para {self.interesado_actual}...")
            
            # Validar que hay contenido
            if not self.lbl_resumen.text or self.lbl_resumen.text.strip() == "":
                print("⚠️ No hay contenido para enviar")
                return
            
            # Obtener contenido del resumen
            mensaje = self.lbl_resumen.text
            
            # Crear URL de WhatsApp
            url = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
            
            # Abrir WhatsApp
            webbrowser.open(url)
            
            print(f"✅ WhatsApp abierto para {self.interesado_actual}")
            
            # Registrar envío
            self.registrar_envio('whatsapp')
            
        except Exception as e:
            print(f"❌ Error enviando por WhatsApp: {e}")
    
    def enviar_por_sms(self, instance):
        """Enviar resumen por SMS (versión corta)"""
        try:
            print(f"📱 Enviando por SMS para {self.interesado_actual}...")
            
            # Crear versión corta para SMS
            links = LINKS_JW[self.idioma_actual]
            
            if self.idioma_actual == 'es':
                mensaje_corto = f"""Hola {self.interesado_actual}, aquí tienes información sobre los temas bíblicos que hemos estudiado. 

Para más recursos: {links['jw_org']}

Para solicitar estudio: {links['solicitar_estudio']}

¡Bendiciones!"""
            else:
                mensaje_corto = f"""Hello {self.interesado_actual}, here is information about the biblical topics we have studied.

For more resources: {links['jw_org']}

To request study: {links['solicitar_estudio']}

Blessings!"""
            
            # Crear URL SMS
            url = f"sms:?body={urllib.parse.quote(mensaje_corto)}"
            
            # Abrir aplicación SMS
            webbrowser.open(url)
            
            print(f"✅ Aplicación SMS abierta para {self.interesado_actual}")
            
            # Registrar envío
            self.registrar_envio('sms')
            
        except Exception as e:
            print(f"❌ Error enviando por SMS: {e}")
    
    def volver_menu(self, instance):
        """Volver al menú principal"""
        try:
            print("🔙 Volviendo al menú principal...")
            
            if self.volver_callback:
                self.volver_callback()
            else:
                # Fallback: usar manager
                if hasattr(self, 'manager') and self.manager:
                    self.manager.current = 'menu'
                else:
                    # Último recurso: usar app
                    app = App.get_running_app()
                    if hasattr(app, 'sm'):
                        app.sm.current = 'menu'
            
        except Exception as e:
            print(f"❌ Error volviendo al menú: {e}")
    
    # === MÉTODOS DE REGISTRO DE ENVÍOS ===
    def registrar_envio(self, metodo_envio):
        """Registrar que se envió un resumen"""
        try:
            # Crear registro del envío
            registro_envio = {
                'interesado': self.interesado_actual,
                'metodo': metodo_envio,
                'timestamp': datetime.now().isoformat(),
                'temas_enviados': len(self.temas_mostrados),
                'idioma': self.idioma_actual,
                'temas_lista': [tema.get('termino', '') for tema in self.temas_mostrados[:10]]  # Primeros 10 temas
            }
            
            # Guardar en archivo de envíos
            self.guardar_registro_envio(registro_envio)
            
            # También registrar en la app principal si está disponible
            self.registrar_envio_en_app(registro_envio)
            
            print(f"📝 Envío registrado: {metodo_envio} para {self.interesado_actual}")
            
        except Exception as e:
            print(f"⚠️ Error registrando envío: {e}")
    
    def guardar_registro_envio(self, registro):
        """Guardar registro de envío en archivo"""
        try:
            archivo_envios = 'historial_envios.json'
            
            # Cargar envíos existentes
            envios = []
            if os.path.exists(archivo_envios):
                with open(archivo_envios, 'r', encoding='utf-8') as f:
                    envios = json.load(f)
            
            # Agregar nuevo envío
            envios.append(registro)
            
            # Mantener solo los últimos 100 envíos para no saturar el archivo
            if len(envios) > 100:
                envios = envios[-100:]
            
            # Guardar archivo actualizado
            with open(archivo_envios, 'w', encoding='utf-8') as f:
                json.dump(envios, f, indent=2, ensure_ascii=False)
            
            print("💾 Registro de envío guardado")
            
        except Exception as e:
            print(f"⚠️ Error guardando registro de envío: {e}")
    
    def registrar_envio_en_app(self, registro):
        """Registrar envío en la aplicación principal"""
        try:
            app = App.get_running_app()
            
            # Si la app tiene método para registrar envíos, usarlo
            if hasattr(app, 'registrar_envio_resumen'):
                app.registrar_envio_resumen(registro)
                print("📝 Envío registrado en app principal")
            
        except Exception as e:
            print(f"⚠️ Error registrando envío en app: {e}")
    
    # === MÉTODOS DE ACTUALIZACIÓN DE IDIOMA ===
    def actualizar_idioma(self, nuevo_idioma):
        """Actualizar idioma de la pantalla"""
        try:
            if nuevo_idioma in ['es', 'en'] and nuevo_idioma != self.idioma_actual:
                print(f"🌍 Cambiando idioma: {self.idioma_actual} → {nuevo_idioma}")
                
                self.idioma_actual = nuevo_idioma
                
                # Actualizar textos de la interfaz
                self.actualizar_textos_interfaz()
                
                # Regenerar resumen en nuevo idioma
                self.generar_resumen_personalizado()
                
                print(f"✅ Idioma actualizado a: {nuevo_idioma}")
            
        except Exception as e:
            print(f"❌ Error actualizando idioma: {e}")
    
    def actualizar_textos_interfaz(self):
        """Actualizar todos los textos de la interfaz"""
        try:
            # Actualizar labels
            if hasattr(self, 'lbl_titulo'):
                self.lbl_titulo.text = self.obtener_texto('titulo')
            
            if hasattr(self, 'lbl_subtitulo'):
                self.lbl_subtitulo.text = self.obtener_texto('subtitulo')
            
            if hasattr(self, 'lbl_nombre_titulo'):
                self.lbl_nombre_titulo.text = self.obtener_texto('nombre_titulo')
            
            if hasattr(self, 'lbl_contenido_titulo'):
                self.lbl_contenido_titulo.text = self.obtener_texto('contenido_titulo')
            
            # Actualizar placeholders
            if hasattr(self, 'input_nombre'):
                self.input_nombre.hint_text = self.obtener_texto('nombre_placeholder')
            
            # Actualizar botones
            if hasattr(self, 'btn_actualizar'):
                self.btn_actualizar.text = self.obtener_texto('btn_actualizar')
            
            if hasattr(self, 'btn_email'):
                self.btn_email.text = self.obtener_texto('btn_email')
            
            if hasattr(self, 'btn_whatsapp'):
                self.btn_whatsapp.text = self.obtener_texto('btn_whatsapp')
            
            if hasattr(self, 'btn_sms'):
                self.btn_sms.text = self.obtener_texto('btn_sms')
            
            if hasattr(self, 'btn_volver'):
                self.btn_volver.text = self.obtener_texto('btn_volver')
            
            print("✅ Textos de interfaz actualizados")
            
        except Exception as e:
            print(f"❌ Error actualizando textos de interfaz: {e}")
    
    # === MÉTODOS DE UTILIDAD ===
    def obtener_estadisticas_envios(self):
        """Obtener estadísticas de envíos realizados"""
        try:
            archivo_envios = 'historial_envios.json'
            
            if not os.path.exists(archivo_envios):
                return {'total': 0, 'por_metodo': {}, 'por_interesado': {}}
            
            with open(archivo_envios, 'r', encoding='utf-8') as f:
                envios = json.load(f)
            
            # Calcular estadísticas
            total = len(envios)
            por_metodo = {}
            por_interesado = {}
            
            for envio in envios:
                metodo = envio.get('metodo', 'desconocido')
                interesado = envio.get('interesado', 'Desconocido')
                
                por_metodo[metodo] = por_metodo.get(metodo, 0) + 1
                por_interesado[interesado] = por_interesado.get(interesado, 0) + 1
            
            estadisticas = {
                'total': total,
                'por_metodo': por_metodo,
                'por_interesado': por_interesado
            }
            
            print(f"📊 Estadísticas: {total} envíos totales")
            return estadisticas
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {'total': 0, 'por_metodo': {}, 'por_interesado': {}}
    
    def limpiar_cache_datos(self):
        """Limpiar cache de datos del interesado"""
        try:
            self.temas_mostrados = []
            self.temas_sesion_actual = []
            print("🧹 Cache de datos limpiado")
            
        except Exception as e:
            print(f"❌ Error limpiando cache: {e}")
    
    def validar_datos_interesado(self):
        """Validar que los datos del interesado son correctos"""
        try:
            if not self.interesado_actual or self.interesado_actual.strip() == "":
                return False, "Nombre del interesado vacío"
            
            if len(self.interesado_actual.strip()) < 2:
                return False, "Nombre del interesado muy corto"
            
            if not self.temas_mostrados:
                return True, "Sin temas registrados (se enviará mensaje genérico)"
            
            return True, "Datos válidos"
            
        except Exception as e:
            print(f"❌ Error validando datos: {e}")
            return False, f"Error de validación: {e}"

print("✅ SEND_RESUME PARTE 5 - Callbacks y envío de mensajes completada")

	# ===== SEND_RESUME.PY - PARTE 6: INTEGRACIÓN FINAL Y CIERRE DE CLASE =====

    # === EVENTOS DEL CICLO DE VIDA ===
    def on_enter(self):
        """Evento cuando se entra a la pantalla"""
        try:
            print("📱 Entrando a pantalla Send Resume")
            
            # Recargar datos del interesado actual
            self.cargar_datos_automaticos()
            
            # Sincronizar idioma con la app
            self.sincronizar_idioma_con_app()
            
            # Actualizar campo de nombre si está disponible
            if hasattr(self, 'input_nombre') and self.interesado_actual:
                self.input_nombre.text = self.interesado_actual
            
            print("✅ Pantalla Send Resume lista")
            
        except Exception as e:
            print(f"⚠️ Error al entrar a Send Resume: {e}")
    
    def on_leave(self):
        """Evento cuando se sale de la pantalla"""
        try:
            print("📱 Saliendo de pantalla Send Resume")
            
        except Exception as e:
            print(f"⚠️ Error al salir de Send Resume: {e}")
    
    def sincronizar_idioma_con_app(self):
        """Sincronizar idioma con la aplicación principal"""
        try:
            app = App.get_running_app()
            
            if hasattr(app, 'idioma_global') and app.idioma_global:
                if app.idioma_global != self.idioma_actual:
                    print(f"🔄 Sincronizando idioma: {self.idioma_actual} → {app.idioma_global}")
                    self.actualizar_idioma(app.idioma_global)
            
        except Exception as e:
            print(f"⚠️ Error sincronizando idioma: {e}")
    
    # === MÉTODOS DE INTEGRACIÓN CON LA APP ===
    def conectar_con_app(self):
        """Conectar automáticamente con la aplicación principal"""
        try:
            app = App.get_running_app()
            
            # Obtener interesado actual
            if hasattr(app, 'interesado_actual') and app.interesado_actual:
                self.establecer_interesado(app.interesado_actual)
            
            # Obtener temas del interesado
            if hasattr(app, 'obtener_temas_interesado'):
                temas = app.obtener_temas_interesado(self.interesado_actual)
                if temas:
                    self.actualizar_temas(temas)
            
            # Configurar callback de volver
            if hasattr(app, 'volver_al_menu'):
                self.volver_callback = app.volver_al_menu
            
            print("🔗 Conectado con la aplicación principal")
            
        except Exception as e:
            print(f"⚠️ Error conectando con app: {e}")
    
    def actualizar_desde_app(self, datos_app):
        """Actualizar datos desde la aplicación principal"""
        try:
            # Actualizar interesado
            if 'interesado' in datos_app:
                self.establecer_interesado(datos_app['interesado'])
            
            # Actualizar temas
            if 'temas' in datos_app:
                self.actualizar_temas(datos_app['temas'])
            
            # Actualizar idioma
            if 'idioma' in datos_app:
                self.actualizar_idioma(datos_app['idioma'])
            
            print("✅ Datos actualizados desde app")
            
        except Exception as e:
            print(f"❌ Error actualizando desde app: {e}")
    
    # === MÉTODOS DE CONFIGURACIÓN AVANZADA ===
    def configurar_estilo_avanzado(self, configuracion):
        """Configurar estilo avanzado del mensaje"""
        try:
            # Configurar tipos de mensaje
            if 'saludo' in configuracion:
                self.tipo_saludo = configuracion['saludo']
            
            if 'despedida' in configuracion:
                self.tipo_despedida = configuracion['despedida']
            
            if 'firma' in configuracion:
                self.tipo_firma = configuracion['firma']
            
            # Regenerar resumen con nueva configuración
            self.generar_resumen_personalizado()
            
            print("✅ Estilo avanzado configurado")
            
        except Exception as e:
            print(f"❌ Error configurando estilo avanzado: {e}")
    
    def personalizar_links_jw(self, links_personalizados):
        """Personalizar links JW para casos especiales"""
        try:
            # Actualizar links temporalmente
            if self.idioma_actual in links_personalizados:
                LINKS_JW[self.idioma_actual].update(links_personalizados[self.idioma_actual])
                
                # Regenerar resumen con nuevos links
                self.generar_resumen_personalizado()
                
                print("✅ Links JW personalizados")
            
        except Exception as e:
            print(f"❌ Error personalizando links: {e}")
    
    # === MÉTODOS DE DEBUG Y TESTING ===
    def debug_mostrar_datos(self):
        """Mostrar datos actuales para debugging"""
        try:
            print("🔍 === DEBUG - DATOS ACTUALES ===")
            print(f"   Interesado: {self.interesado_actual}")
            print(f"   Idioma: {self.idioma_actual}")
            print(f"   Temas cargados: {len(self.temas_mostrados)}")
            print(f"   Estilo: {self.tipo_saludo}/{self.tipo_despedida}/{self.tipo_firma}")
            
            if self.temas_mostrados:
                print("   Primeros 5 temas:")
                for i, tema in enumerate(self.temas_mostrados[:5], 1):
                    termino = tema.get('termino', 'Sin término')
                    print(f"     {i}. {termino}")
            
            print("🔍 === FIN DEBUG ===")
            
        except Exception as e:
            print(f"❌ Error en debug: {e}")
    
    def test_generacion_resumen(self):
        """Probar generación de resumen con datos de prueba"""
        try:
            print("🧪 Probando generación de resumen...")
            
            # Datos de prueba
            self.interesado_actual = "Juan Pérez"
            self.temas_mostrados = [
                {'termino': 'Reino de Dios', 'timestamp': '2024-01-01', 'resultado': 'Tema estudiado'},
                {'termino': 'Esperanza de resurrección', 'timestamp': '2024-01-02', 'resultado': 'Tema estudiado'},
                {'termino': 'Vida eterna', 'timestamp': '2024-01-03', 'resultado': 'Tema estudiado'}
            ]
            
            # Generar resumen de prueba
            self.generar_resumen_personalizado()
            
            print("✅ Resumen de prueba generado")
            print("📄 Vista previa:")
            print(self.lbl_resumen.text[:200] + "...")
            
        except Exception as e:
            print(f"❌ Error en test: {e}")

# === CIERRE DE CLASE Y FUNCIONES DE UTILIDAD ===

# Función para crear la pantalla fácilmente
def crear_pantalla_send_resume(idioma='es', interesado=None):
    """Función helper para crear la pantalla Send Resume"""
    try:
        pantalla = PantallaSendResume()
        
        if idioma != 'es':
            pantalla.actualizar_idioma(idioma)
        
        if interesado:
            pantalla.establecer_interesado(interesado)
        
        return pantalla
        
    except Exception as e:
        print(f"❌ Error creando pantalla Send Resume: {e}")
        return None

# Función para testing independiente
def test_pantalla_send_resume():
    """Función para probar la pantalla independientemente"""
    try:
        from kivy.app import App
        from kivy.uix.screenmanager import ScreenManager
        
        class TestSendResumeApp(App):
            def build(self):
                sm = ScreenManager()
                
                # Crear pantalla de prueba
                pantalla = crear_pantalla_send_resume('es', 'María González')
                sm.add_widget(pantalla)
                
                return sm
        
        print("🧪 Iniciando prueba de Send Resume...")
        TestSendResumeApp().run()
        
    except Exception as e:
        print(f"❌ Error en test: {e}")

# === DOCUMENTACIÓN DE USO ===
"""
=== CÓMO USAR SEND_RESUME.PY ===

1. IMPORTAR:
   from pantallas.send_resume import PantallaSendResume

2. CREAR INSTANCIA:
   send_resume = PantallaSendResume()

3. CONFIGURAR INTERESADO:
   send_resume.establecer_interesado("Juan Pérez")

4. ACTUALIZAR IDIOMA:
   send_resume.actualizar_idioma('en')

5. CONFIGURAR CALLBACK:
   send_resume.volver_callback = app.volver_al_menu

6. AGREGAR AL SCREEN MANAGER:
   app.sm.add_widget(send_resume)

=== INTEGRACIÓN CON MAIN.PY ===

En tu main.py, agrega estos métodos:

def ir_enviar_resumen(self):
    if self.sm.has_screen('send_resume'):
        send_resume_screen = self.sm.get_screen('send_resume')
        
        # Actualizar datos
        if hasattr(self, 'interesado_actual'):
            send_resume_screen.establecer_interesado(self.interesado_actual)
        
        # Actualizar idioma
        send_resume_screen.actualizar_idioma(self.idioma_global)
        
        self.sm.current = 'send_resume'

def registrar_envio_resumen(self, registro):
    # Procesar registro de envío en tu app
    pass
"""

print("✅ SEND_RESUME PARTE 6 - Integración final completada")
print("✅ send_resume.py COMPLETAMENTE FUNCIONAL")

# Si se ejecuta directamente, correr test
if __name__ == '__main__':
    test_pantalla_send_resume()