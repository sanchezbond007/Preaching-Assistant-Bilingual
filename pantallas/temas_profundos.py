# AGREGAR AL INICIO DE temas_profundos.py (después de los imports):

def traducir_texto(texto, idioma_destino):
    """Traducir texto básico español-inglés"""
    if idioma_destino == 'es':
        return texto
    
    # Traducciones básicas español → inglés
    traducciones = {
        # Títulos principales
        'TEMAS PROFUNDOS': 'DEEP TOPICS',
        'Contenido:': 'Content:',
        'Conclusión:': 'Conclusion:',
        'Copiar': 'Copy',
        'Cerrar': 'Close',
        'Volver': 'Back',
        
        # Frases comunes
        'La mayoría de las religiones enseñan que el': 'Most religions teach that the',
        'alma es inmortal y que sigue viviendo después': 'soul is immortal and continues living after',
        'de la muerte. Sin embargo, la Biblia enseña lo': 'death. However, the Bible teaches the',
        'contrario: que el alma puede morir y que el ser': 'opposite: that the soul can die and that the',
        'humano no tiene una parte separada que': 'human being does not have a separate part that',
        'continúe consciente después de la muerte.': 'continues conscious after death.',
        
        'La enseñanza bíblica muestra que el alma no es': 'Biblical teaching shows that the soul is not',
        'inmortal. El alma es la persona completa, que': 'immortal. The soul is the complete person, who',
        'muere al morir el cuerpo. La verdadera': 'dies when the body dies. The true',
        'esperanza para los muertos es la resurrección': 'hope for the dead is the resurrection',
        'que Dios promete mediante Jesús.': 'that God promises through Jesus.',
        
        # Jesucristo
        'Jesucristo es el Hijo de Dios. No es el Dios': 'Jesus Christ is the Son of God. He is not the',
        'Todopoderoso, sino que fue creado por Jehová.': 'Almighty God, but was created by Jehovah.',
        'Fue enviado a la Tierra para enseñar la verdad,': 'He was sent to Earth to teach the truth,',
        'dar su vida por la humanidad y mostrar el': 'give his life for humanity and show the',
        'camino a la vida eterna. Sus enseñanzas y': 'way to eternal life. His teachings and',
        'ejemplo nos ayudan a acercarnos a Dios.': 'example help us draw closer to God.'
    }
    
    # Aplicar traducciones
    texto_traducido = texto
    for esp, eng in traducciones.items():
        texto_traducido = texto_traducido.replace(esp, eng)
    
    return texto_traducido

# BUSCAR LA FUNCIÓN mostrar_detalle_tema_profundo Y MODIFICAR:

def mostrar_detalle_tema_profundo(self, instance, nombre_archivo):
    """Mostrar detalle con traducción"""
    try:
        print(f"📖 Abriendo tema profundo: {nombre_archivo}")
        
        ruta_archivo = f'datos/temas_profundos/{nombre_archivo}'
        if not os.path.exists(ruta_archivo):
            print(f"❌ Archivo no encontrado: {ruta_archivo}")
            return
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # TRADUCIR CONTENIDO SEGÚN IDIOMA
        contenido_traducido = traducir_texto(contenido, self.idioma)
        
        # Crear layout del popup
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        scroll = ScrollView()
        scroll_content = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            padding=[10, 0]
        )
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        # Separar título y contenido
        lineas = contenido_traducido.strip().split('\n')
        if lineas:
            titulo_tema = lineas[0]
            resto_contenido = '\n'.join(lineas[1:]) if len(lineas) > 1 else ""
        else:
            titulo_tema = "Sin título"
            resto_contenido = "Sin contenido"
        
        # Label del contenido con TEXTO BLANCO
        label_contenido = Label(
            text=resto_contenido,
            text_size=(dp(300), None),
            halign='left',
            valign='top',
            markup=False,
            color=(1, 1, 1, 1),  # ✅ TEXTO BLANCO
            font_size='14sp',
            size_hint_y=None
        )
        label_contenido.bind(texture_size=label_contenido.setter('size'))
        scroll_content.add_widget(label_contenido)
        
        scroll.add_widget(scroll_content)
        content.add_widget(scroll)
        
        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=dp(50)
        )
        
        btn_copiar = Button(
            text=traducir_texto('📋 Copiar', self.idioma),
            background_color=(0.2, 0.7, 0.2, 1),
            font_size='16sp'
        )
        btn_copiar.bind(on_press=lambda x: self.copiar_al_portapapeles(contenido_traducido))
        
        btn_cerrar = Button(
            text=traducir_texto('❌ Cerrar', self.idioma),
            background_color=(0.8, 0.3, 0.3, 1),
            font_size='16sp'
        )
        
        botones_layout.add_widget(btn_copiar)
        botones_layout.add_widget(btn_cerrar)
        content.add_widget(botones_layout)
        
        # Crear popup con título traducido
        popup_titulo = traducir_texto(titulo_tema, self.idioma)
        popup = Popup(
            title=f"📚 {popup_titulo}",
            content=content,
            size_hint=(0.95, 0.8),
            auto_dismiss=True,
            separator_color=[0.2, 0.4, 0.6, 1],
            title_color=[1, 1, 1, 1],  # ✅ TÍTULO BLANCO
            title_size='16sp'
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()
        
    except Exception as e:
        print(f"❌ Error abriendo tema profundo: {e}")

# TAMBIÉN MODIFICAR LA FUNCIÓN crear_interfaz PARA TRADUCIR BOTONES:

def crear_interfaz(self):
    # ... código existente ...
    
    # En la parte donde creas btn_volver:
    btn_volver = Button(
        text=traducir_texto('🔙 Volver', self.idioma),
        size_hint_y=None,
        height=dp(60),
        background_color=(0.3, 0.3, 0.3, 1),
        color=(1, 1, 1, 1),
        font_size='18sp',
        bold=True
    )
#!/usr/bin/env python3
"""
pantallas/temas_profundos.py - PARTE 1
Pantalla de Temas Profundos - Estructura Principal y Configuración
"""

import os
import json
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock

class PantallaTemasProfundos(Screen):
    def __init__(self, **kwargs):
        # 🎯 ADAPTACIÓN: Extraer callbacks y configuraciones
        self.volver_callback = kwargs.pop('volver_callback', None)
        self.idioma_inicial = kwargs.pop('idioma', 'es')
        
        super(PantallaTemasProfundos, self).__init__(**kwargs)
        
        # 🆕 INTEGRACIÓN: Variables de estado
        self.usuario_actual = None
        self.idioma_usuario = self.idioma_inicial
        self.todos_los_temas = []
        self.temas_mostrados = []
        self.temas_por_pagina = 10
        self.historial_individual = None
        
        # 🎯 INTEGRACIÓN: Cargar sistema de historial si está disponible
        self.cargar_sistema_historial()
        
        self.build_ui()

    def cargar_sistema_historial(self):
        """🆕 INTEGRACIÓN: Cargar sistema de historial individual"""
        try:
            from pantallas.send_resume_individual import HistorialIndividual
            self.historial_individual = HistorialIndividual()
            print("✅ Sistema de historial integrado en Temas Profundos")
        except ImportError:
            print("⚠️ Sistema de historial no disponible")
            self.historial_individual = None

    def build_ui(self):
        """🎯 ADAPTACIÓN: Interfaz principal con diseño consistente"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # 🎯 TÍTULO DE LA PANTALLA
        titulo = Label(
            text='📚 TEMAS PROFUNDOS\nDEEP TOPICS',
            font_size='20sp',
            size_hint_y=None,
            height=dp(80),
            halign='center',
            bold=True,
            color=(1, 1, 1, 1)
        )
        titulo.bind(size=titulo.setter('text_size'))
        main_layout.add_widget(titulo)
        
        # 🎯 BOTONES DE ACCIÓN
        botones_layout = BoxLayout(
            orientation='horizontal', 
            spacing=dp(10), 
            size_hint_y=None, 
            height=dp(50)
        )
        
        # Botón para nuevos temas
        self.btn_nuevas_sugerencias = Button(
            text='Nuevos Temas',
            background_color=(0.3, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='14sp',
            bold=True
        )
        self.btn_nuevas_sugerencias.bind(on_press=self.generar_nuevos_temas)
        botones_layout.add_widget(self.btn_nuevas_sugerencias)
        
        # Botón para buscar
        self.btn_buscar = Button(
            text='Buscar',
            background_color=(0.6, 0.3, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size='14sp',
            bold=True
        )
        self.btn_buscar.bind(on_press=self.mostrar_busqueda)
        botones_layout.add_widget(self.btn_buscar)
        
        main_layout.add_widget(botones_layout)
        
        # 🎯 SCROLL CON CONTENIDO
        scroll = ScrollView()
        self.content_layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(5), 
            size_hint_y=None,
            padding=[dp(5), 0]
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        scroll.add_widget(self.content_layout)
        main_layout.add_widget(scroll)
        
        # 🎯 BOTÓN VOLVER
        self.btn_volver = Button(
            text='🔙 Volver',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        self.btn_volver.bind(on_press=self.ir_al_menu)
        main_layout.add_widget(self.btn_volver)
        
        self.add_widget(main_layout)

    def on_enter(self):
        """🎯 ADAPTACIÓN: Configuración al entrar a la pantalla"""
        print("📚 Entrando a Temas Profundos...")
        
        # Actualizar idioma
        self.actualizar_idioma()
        
        # Cargar datos
        self.cargar_todos_los_temas()
        self.cargar_temas_iniciales()
        
        # 🆕 INTEGRACIÓN: Actualizar archivo de usuario actual
        self.actualizar_archivo_usuario()

    def actualizar_archivo_usuario(self):
        """🆕 INTEGRACIÓN: Actualizar archivo usuario_actual.json"""
        try:
            usuario_data = {
                'usuario': self.usuario_actual or 'usuario_anonimo',
                'idioma': self.idioma_usuario,
                'pantalla_actual': 'temas_profundos',
                'timestamp': self.obtener_timestamp()
            }
            
            with open('usuario_actual.json', 'w', encoding='utf-8') as f:
                json.dump(usuario_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Archivo usuario_actual.json actualizado - Idioma: {self.idioma_usuario}")
        except Exception as e:
            print(f"⚠️ Error actualizando usuario_actual.json: {e}")

    def obtener_timestamp(self):
        """🛠️ UTILIDAD: Obtener timestamp actual"""
        try:
            import datetime
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "N/A"

    def actualizar_idioma(self, nuevo_idioma=None):
        """🎯 ADAPTACIÓN: Actualizar idioma dinámicamente"""
        if nuevo_idioma:
            self.idioma_usuario = nuevo_idioma
        
        traducciones = {
            'volver': {'es': '🔙 Volver', 'en': '🔙 Back'},
            'nuevos_temas': {'es': '🔄 Nuevos Temas', 'en': '🔄 New Topics'},
            'buscar': {'es': '🔍 Buscar', 'en': '🔍 Search'}
        }
        
        idioma = self.idioma_usuario.lower().strip()
        
        if hasattr(self, 'btn_volver'):
            self.btn_volver.text = traducciones['volver'].get(idioma, '🔙 Volver')
        if hasattr(self, 'btn_nuevas_sugerencias'):
            self.btn_nuevas_sugerencias.text = traducciones['nuevos_temas'].get(idioma, '🔄 Nuevos Temas')
        if hasattr(self, 'btn_buscar'):
            self.btn_buscar.text = traducciones['buscar'].get(idioma, '🔍 Buscar')
        
        print(f"✅ Idioma actualizado en Temas Profundos: {idioma}")

    def cargar_temas_desde_directorio_profundos(self):
        """🎯 ADAPTACIÓN: Cargar temas desde archivos con soporte múltiple"""
        try:
            directorio_temas = os.path.join('datos', 'temas_profundos')
            
            if not os.path.exists(directorio_temas):
                print("📁 Creando directorio de temas profundos...")
                os.makedirs(directorio_temas, exist_ok=True)
                self.crear_archivos_ejemplo_profundos()
            
            todos_los_temas = []
            
            # 🎯 SOPORTE PARA .json Y .txt
            for archivo in os.listdir(directorio_temas):
                if archivo.endswith('.json'):
                    try:
                        ruta_archivo = os.path.join(directorio_temas, archivo)
                        with open(ruta_archivo, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                        
                        if isinstance(data, list):
                            todos_los_temas.extend(data)
                        elif isinstance(data, dict):
                            todos_los_temas.append(data)
                            
                    except Exception as e:
                        print(f"⚠️ Error cargando {archivo}: {e}")
                        continue
                        
                elif archivo.endswith('.txt'):
                    # 🆕 SOPORTE: Archivos .txt convertidos a formato de tema
                    try:
                        ruta_archivo = os.path.join(directorio_temas, archivo)
                        with open(ruta_archivo, 'r', encoding='utf-8') as file:
                            contenido = file.read().strip()
                        
                        if contenido:
                            tema_convertido = self.convertir_txt_a_tema(archivo, contenido)
                            todos_los_temas.append(tema_convertido)
                            
                    except Exception as e:
                        print(f"⚠️ Error cargando archivo .txt {archivo}: {e}")
                        continue
            
            print(f"📚 Temas profundos cargados: {len(todos_los_temas)}")
            return todos_los_temas
            
        except Exception as e:
            print(f"❌ Error cargando temas profundos: {e}")
            return []

    def convertir_txt_a_tema(self, nombre_archivo, contenido):
        """🆕 UTILIDAD: Convertir archivo .txt a formato de tema"""
        titulo_base = nombre_archivo.replace('.txt', '').replace('_', ' ').title()
        
        return {
            'titulo': {
                'es': titulo_base,
                'en': titulo_base  # Para archivos .txt, usar el mismo título
            },
            'contenido': {
                'es': contenido,
                'en': contenido  # Para archivos .txt, usar el mismo contenido
            },
            'conclusion': {
                'es': "Tema para estudio profundo.",
                'en': "Topic for deep study."
            },
            'fuente': nombre_archivo
        }

    def crear_archivos_ejemplo_profundos(self):
        """🎯 ADAPTACIÓN: Crear archivos de ejemplo"""
        try:
            directorio = os.path.join('datos', 'temas_profundos')
            
            # Archivo JSON de ejemplo
            ejemplo_json = [
                {
                    "titulo": {
                        "es": "La Soberanía de Jehová",
                        "en": "Jehovah's Sovereignty"
                    },
                    "contenido": {
                        "es": "Jehová ejerce su soberanía con sabiduría y amor. Su dominio abarca toda la creación y se manifiesta a través de sus leyes y principios eternos.",
                        "en": "Jehovah exercises his sovereignty with wisdom and love. His dominion encompasses all creation and is manifested through his eternal laws and principles."
                    },
                    "conclusion": {
                        "es": "Reconocer la soberanía divina nos ayuda a confiar en el propósito eterno de Dios.",
                        "en": "Recognizing divine sovereignty helps us trust in God's eternal purpose."
                    }
                }
            ]
            
            ruta_json = os.path.join(directorio, 'temas_profundos_ejemplo.json')
            with open(ruta_json, 'w', encoding='utf-8') as f:
                json.dump(ejemplo_json, f, indent=2, ensure_ascii=False)
            
            print("✅ Archivo de ejemplo creado: temas_profundos_ejemplo.json")
            
        except Exception as e:
            print(f"⚠️ Error creando archivos de ejemplo: {e}")

    def cargar_todos_los_temas(self):
        """🎯 FUNCIÓN PRINCIPAL: Cargar todos los temas disponibles"""
        self.todos_los_temas = self.cargar_temas_desde_directorio_profundos()
        
        # Si no hay temas desde archivos, usar predeterminados
        if not self.todos_los_temas:
            self.todos_los_temas = self.obtener_preguntas_predeterminadas()

    def obtener_temas_no_mostrados(self, cantidad):
        """🎯 LÓGICA: Obtener temas que no se han mostrado"""
        if not self.todos_los_temas:
            return []
        
        temas_disponibles = [tema for tema in self.todos_los_temas if tema not in self.temas_mostrados]
        
        if len(temas_disponibles) < cantidad:
            random.shuffle(self.todos_los_temas)
            self.temas_mostrados = []
            temas_disponibles = self.todos_los_temas
        
        temas_seleccionados = temas_disponibles[:cantidad]
        self.temas_mostrados.extend(temas_seleccionados)
        
        return temas_seleccionados

    def obtener_preguntas_predeterminadas(self):
        """🎯 RESPALDO: Temas predeterminados si no hay archivos"""
        return [
            {
                "titulo": {"es": "¿Cómo mantener la esperanza cristiana?", "en": "How to maintain Christian hope?"}, 
                "contenido": {"es": "La esperanza cristiana se basa en las promesas de Dios registradas en su Palabra. A través de la oración constante, el estudio regular de las Escrituras y la asociación con otros creyentes, podemos fortalecer nuestra esperanza.", "en": "Christian hope is based on God's promises recorded in his Word. Through constant prayer, regular study of the Scriptures, and association with other believers, we can strengthen our hope."}, 
                "conclusion": {"es": "La esperanza fortalece nuestra fe y nos ayuda a perseverar en tiempos difíciles.", "en": "Hope strengthens our faith and helps us persevere in difficult times."}
            },
            {
                "titulo": {"es": "¿Qué significa la vida eterna?", "en": "What does eternal life mean?"}, 
                "contenido": {"es": "La vida eterna no es solo vida sin fin, sino vida de calidad suprema bajo el Reino de Dios. Incluye perfecta salud, paz completa y una relación armoniosa con nuestro Creador.", "en": "Eternal life is not just endless life, but life of supreme quality under God's Kingdom. It includes perfect health, complete peace, and a harmonious relationship with our Creator."}, 
                "conclusion": {"es": "La vida eterna es el regalo más grande que Dios ofrece a los que le son fieles.", "en": "Eternal life is the greatest gift God offers to those who are faithful to him."}
            },
            {
                "titulo": {"es": "¿Cómo enfrentar las pruebas con fe?", "en": "How to face trials with faith?"}, 
                "contenido": {"es": "Las pruebas son oportunidades para demostrar nuestra fe en Jehová. Cuando confiamos en su sabiduría y poder, encontramos la fuerza necesaria para superar cualquier dificultad.", "en": "Trials are opportunities to demonstrate our faith in Jehovah. When we trust in his wisdom and power, we find the strength needed to overcome any difficulty."}, 
                "conclusion": {"es": "Las pruebas, aunque difíciles, nos fortalecen y refinan nuestro carácter cristiano.", "en": "Trials, though difficult, strengthen us and refine our Christian character."}
            },
            {
                "titulo": {"es": "El poder del perdón cristiano", "en": "The power of Christian forgiveness"}, 
                "contenido": {"es": "El perdón es una característica fundamental del cristianismo. Seguimos el ejemplo de Jesús al perdonar de corazón, liberándonos del resentimiento y promoviendo la paz.", "en": "Forgiveness is a fundamental characteristic of Christianity. We follow Jesus' example by forgiving from the heart, freeing ourselves from resentment and promoting peace."}, 
                "conclusion": {"es": "El perdón sincero trae sanidad emocional y fortalece nuestras relaciones.", "en": "Sincere forgiveness brings emotional healing and strengthens our relationships."}
            },
            {
                "titulo": {"es": "La importancia de la humildad cristiana", "en": "The importance of Christian humility"}, 
                "contenido": {"es": "La humildad nos ayuda a reconocer nuestra dependencia de Dios y a tratar a otros con respeto y consideración. Es una cualidad que Jehová valora profundamente.", "en": "Humility helps us recognize our dependence on God and treat others with respect and consideration. It is a quality that Jehovah deeply values."}, 
                "conclusion": {"es": "La humildad genuina agrada a Dios y nos acerca más a él.", "en": "Genuine humility pleases God and draws us closer to him."}
            }
        ]
        
    def cargar_temas_iniciales(self):
        """🎯 FUNCIÓN: Cargar temas iniciales en la interfaz"""
        self.content_layout.clear_widgets()
        self.temas_mostrados = []
        
        if not self.todos_los_temas:
            temas_a_mostrar = self.obtener_preguntas_predeterminadas()[:self.temas_por_pagina]
        else:
            temas_a_mostrar = self.obtener_temas_no_mostrados(self.temas_por_pagina)
        
        self.agregar_temas_a_layout(temas_a_mostrar)

    def agregar_temas_a_layout(self, temas):
        """🎯 INTERFAZ: Agregar botones de temas al layout"""
        if not temas:
            # Mostrar mensaje si no hay temas
            label_vacio = Label(
                text='No hay temas disponibles' if self.idioma_usuario == 'es' else 'No topics available',
                size_hint_y=None,
                height=dp(60),
                color=(0.5, 0.5, 0.5, 1),
                font_size='16sp'
            )
            self.content_layout.add_widget(label_vacio)
            return
        
        for tema in temas:
            try:
                titulo = tema.get('titulo', {})
                idioma = self.idioma_usuario.lower().strip()
                
                if isinstance(titulo, dict):
                    texto_boton = titulo.get(idioma, titulo.get('es', 'Sin título'))
                else:
                    texto_boton = str(titulo)
                
                texto_boton_display = f"📚 {texto_boton}"
                
                btn = Button(
                    text=texto_boton_display,
                    size_hint_y=None,
                    height=dp(70),
                    background_color=(0.2, 0.4, 0.6, 1),
                    color=(1, 1, 1, 1),
                    text_size=(dp(280), None),
                    halign='left',
                    valign='middle',
                    font_size='14sp'
                )
                btn.bind(on_press=lambda x, t=tema: self.mostrar_detalle_tema_profundo(t))
                self.content_layout.add_widget(btn)
                
            except Exception as e:
                print(f"⚠️ Error procesando tema: {e}")
                continue

    def mostrar_detalle_tema_profundo(self, tema):
        """🎯 FUNCIÓN PRINCIPAL: Mostrar detalle del tema en popup"""
        print(f"📖 Mostrando tema profundo...")
        
        # 🆕 INTEGRACIÓN: Registrar consulta en historial
        self.registrar_consulta_tema(tema)
        
        idioma = self.idioma_usuario.lower().strip()
        
        # Extraer información del tema
        titulo = tema.get('titulo', {})
        if isinstance(titulo, dict):
            titulo_texto = titulo.get(idioma, titulo.get('es', 'Sin título'))
        else:
            titulo_texto = str(titulo)
        
        contenido = tema.get('contenido', {})
        if isinstance(contenido, dict):
            contenido_texto = contenido.get(idioma, contenido.get('es', 'Sin contenido'))
        else:
            contenido_texto = str(contenido)
        
        conclusion = tema.get('conclusion', {})
        if isinstance(conclusion, dict):
            conclusion_texto = conclusion.get(idioma, conclusion.get('es', ''))
        else:
            conclusion_texto = str(conclusion) if conclusion else ''
        
        # Construir texto completo
        lineas = [f"📚 {titulo_texto}", ""]
        
        if contenido_texto:
            intro_label = "📖 Contenido:" if idioma == 'es' else "📖 Content:"
            lineas.extend([intro_label, "", contenido_texto, ""])
        
        if conclusion_texto:
            concl_label = "✨ Conclusión:" if idioma == 'es' else "✨ Conclusion:"
            lineas.extend([concl_label, "", conclusion_texto])
        
        texto_completo = "\n".join(lineas)
        
        # Crear popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        container.bind(minimum_height=container.setter('height'))
        
        label_contenido = Label(
            text=texto_completo,
            text_size=(dp(300), None),
            halign='left',
            valign='top',
            markup=False,
            color=(1, 1, 1, 1),  # Texto blanco para mejor legibilidad
            font_size='14sp',
            size_hint_y=None
        )
        label_contenido.bind(texture_size=label_contenido.setter('size'))
        
        container.add_widget(label_contenido)
        
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        scroll.add_widget(container)
        content.add_widget(scroll)
        
        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal', 
            spacing=dp(10), 
            size_hint_y=None, 
            height=dp(50)
        )
        
        btn_copiar = Button(
            text='📋 Copiar' if idioma == 'es' else '📋 Copy',
            background_color=(0.3, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='14sp'
        )
        btn_copiar.bind(on_press=lambda x: self.copiar_tema(texto_completo))
        botones_layout.add_widget(btn_copiar)
        
        btn_cerrar = Button(
            text='❌ Cerrar' if idioma == 'es' else '❌ Close',
            background_color=(0.6, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='14sp'
        )
        botones_layout.add_widget(btn_cerrar)
        
        content.add_widget(botones_layout)
        
        popup_titulo = titulo_texto if len(titulo_texto) < 25 else titulo_texto[:22] + "..."
        popup = Popup(
            title=f"📚 {popup_titulo}",
            content=content,
            size_hint=(0.95, 0.8),
            auto_dismiss=True,
            separator_color=[0.2, 0.4, 0.6, 1],
            title_color=[1, 1, 1, 1],
            title_size='16sp'
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        
        def scroll_al_tope(*args):
            scroll.scroll_y = 1
        
        popup.bind(on_open=lambda *args: Clock.schedule_once(scroll_al_tope, 0.1))
        popup.open()

    def registrar_consulta_tema(self, tema):
        """🆕 INTEGRACIÓN: Registrar consulta en el historial"""
        try:
            if self.historial_individual:
                titulo = tema.get('titulo', {})
                idioma = self.idioma_usuario.lower().strip()
                
                if isinstance(titulo, dict):
                    titulo_texto = titulo.get(idioma, titulo.get('es', 'Tema sin título'))
                else:
                    titulo_texto = str(titulo)
                
                # Registrar la consulta
                self.historial_individual.registrar_consulta(
                    consulta=f"Tema Profundo: {titulo_texto}",
                    respuesta="Tema consultado en Temas Profundos",
                    categoria="temas_profundos"
                )
                print(f"📝 Consulta registrada: {titulo_texto}")
        except Exception as e:
            print(f"⚠️ Error registrando consulta: {e}")

    def generar_nuevos_temas(self, instance):
        """🎯 FUNCIÓN: Generar nuevos temas aleatorios"""
        print("🔄 Generando nuevos temas...")
        
        if self.todos_los_temas:
            random.shuffle(self.todos_los_temas)
        
        self.temas_mostrados = []
        self.cargar_temas_iniciales()

    def mostrar_busqueda(self, instance):
        """🎯 FUNCIÓN: Mostrar popup de búsqueda"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        idioma = self.idioma_usuario.lower().strip()
        instrucciones = {
            'es': '🔍 Escriba una palabra clave para buscar en temas profundos:',
            'en': '🔍 Enter a keyword to search in deep topics:'
        }
        texto_instrucciones = instrucciones.get(idioma, instrucciones['es'])
        
        label_instrucciones = Label(
            text=texto_instrucciones,
            size_hint_y=None,
            height=dp(60),
            text_size=(dp(300), None),
            halign='center',
            color=(0, 0, 0, 1),
            font_size='14sp'
        )
        content.add_widget(label_instrucciones)
        
        self.input_busqueda = TextInput(
            hint_text='Palabra clave...' if idioma == 'es' else 'Keyword...',
            size_hint_y=None,
            height=dp(40),
            multiline=False,
            foreground_color=(0, 0, 0, 1),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        content.add_widget(self.input_busqueda)
        
        botones_layout = BoxLayout(
            orientation='horizontal', 
            spacing=dp(10), 
            size_hint_y=None, 
            height=dp(50)
        )
        
        btn_buscar_popup = Button(
            text='🔍 Buscar' if idioma == 'es' else '🔍 Search',
            background_color=(0.3, 0.6, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        btn_buscar_popup.bind(on_press=self.ejecutar_busqueda_profundos)
        botones_layout.add_widget(btn_buscar_popup)
        
        btn_cancelar = Button(
            text='❌ Cancelar' if idioma == 'es' else '❌ Cancel',
            background_color=(0.6, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        btn_cancelar.bind(on_press=self.cerrar_popup_busqueda)
        botones_layout.add_widget(btn_cancelar)
        
        content.add_widget(botones_layout)
        
        titulo_popup = '🔍 Buscar Temas Profundos' if idioma == 'es' else '🔍 Search Deep Topics'
        self.popup_busqueda = Popup(
            title=titulo_popup,
            content=content,
            size_hint=(0.9, 0.5),
            auto_dismiss=False
        )
        self.popup_busqueda.open()

    def ejecutar_busqueda_profundos(self, instance):
        """🎯 FUNCIÓN: Ejecutar búsqueda en temas profundos"""
        palabra_clave = self.input_busqueda.text.strip().lower()
        
        if not palabra_clave:
            return
        
        self.popup_busqueda.dismiss()
        
        print(f"🔍 Buscando: {palabra_clave}")
        
        # 🆕 INTEGRACIÓN: Registrar búsqueda en historial
        self.registrar_busqueda(palabra_clave)
        
        resultados = self.buscar_en_temas(palabra_clave)
        self.mostrar_resultados_busqueda(resultados, palabra_clave)

    def cerrar_popup_busqueda(self, instance):
        """🎯 FUNCIÓN: Cerrar popup de búsqueda"""
        self.popup_busqueda.dismiss()

    def buscar_en_temas(self, palabra_clave):
        """🎯 FUNCIÓN: Buscar palabra clave en todos los temas"""
        resultados = []
        palabra_clave = palabra_clave.lower()
        
        todos_los_temas = self.todos_los_temas if self.todos_los_temas else self.obtener_preguntas_predeterminadas()
        
        for tema in todos_los_temas:
            # Buscar en título
            titulo = tema.get('titulo', {})
            if isinstance(titulo, dict):
                for idioma, texto in titulo.items():
                    if palabra_clave in texto.lower():
                        resultados.append(tema)
                        break
            else:
                if palabra_clave in str(titulo).lower():
                    resultados.append(tema)
                    continue
            
            # Buscar en contenido
            contenido = tema.get('contenido', {})
            if isinstance(contenido, dict):
                for idioma, texto in contenido.items():
                    if palabra_clave in texto.lower():
                        if tema not in resultados:
                            resultados.append(tema)
                        break
            else:
                if palabra_clave in str(contenido).lower():
                    if tema not in resultados:
                        resultados.append(tema)
        
        return resultados

    def mostrar_resultados_busqueda(self, resultados, palabra_clave):
        """🎯 FUNCIÓN: Mostrar resultados de búsqueda"""
        self.content_layout.clear_widgets()
        
        # Título de resultados
        idioma = self.idioma_usuario.lower().strip()
        if resultados:
            texto_titulo = f"🔍 Resultados para '{palabra_clave}': {len(resultados)}" if idioma == 'es' else f"🔍 Results for '{palabra_clave}': {len(resultados)}"
        else:
            texto_titulo = f"🔍 Sin resultados para '{palabra_clave}'" if idioma == 'es' else f"🔍 No results for '{palabra_clave}'"
        
        titulo_resultados = Label(
            text=texto_titulo,
            size_hint_y=None,
            height=dp(50),
            color=(0, 0, 0, 1),
            font_size='16sp',
            bold=True
        )
        self.content_layout.add_widget(titulo_resultados)
        
        if resultados:
            self.agregar_temas_a_layout(resultados)
        else:
            # Mostrar mensaje de no resultados
            mensaje_vacio = Label(
                text='No se encontraron temas que coincidan con la búsqueda.' if idioma == 'es' else 'No topics found matching the search.',
                size_hint_y=None,
                height=dp(60),
                color=(0.5, 0.5, 0.5, 1),
                font_size='14sp',
                text_size=(dp(280), None),
                halign='center'
            )
            self.content_layout.add_widget(mensaje_vacio)
        
        # Botón para volver a todos los temas
        btn_ver_todos = Button(
            text='📚 Ver Todos los Temas' if idioma == 'es' else '📚 View All Topics',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size='14sp'
        )
        btn_ver_todos.bind(on_press=lambda x: self.cargar_temas_iniciales())
        self.content_layout.add_widget(btn_ver_todos)

    def registrar_busqueda(self, palabra_clave):
        """🆕 INTEGRACIÓN: Registrar búsqueda en historial"""
        try:
            if self.historial_individual:
                self.historial_individual.registrar_consulta(
                    consulta=f"Búsqueda en Temas Profundos: {palabra_clave}",
                    respuesta="Búsqueda realizada en la sección de Temas Profundos",
                    categoria="busqueda_temas_profundos"
                )
                print(f"📝 Búsqueda registrada: {palabra_clave}")
        except Exception as e:
            print(f"⚠️ Error registrando búsqueda: {e}")

    def copiar_tema(self, texto):
        """🎯 FUNCIÓN: Copiar tema al portapapeles"""
        try:
            # Intentar copiar al portapapeles (funcionalidad básica)
            print("📋 Tema preparado para copiar")
            print(f"Contenido: {texto[:100]}...")  # Mostrar preview
        except Exception as e:
            print(f"⚠️ Error copiando tema: {e}")

    def ir_al_menu(self, instance=None):
        """🎯 NAVEGACIÓN: Volver al menú"""
        try:
            if self.volver_callback:
                self.volver_callback()
                print("🔙 Volviendo al menú con callback")
            else:
                print("🔙 Callback no disponible")
        except Exception as e:
            print(f"❌ Error volviendo al menú: {e}")

# FIN DE LA CLASE PantallaTemasProfundos