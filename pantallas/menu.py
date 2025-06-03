from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
# NO USAR traducciones.py para evitar conflictos
# from utils.traducciones import obtener_texto

class PantallaMenu(Screen):
    def __init__(self, **kwargs):
        # Extraer callbacks y parámetros personalizados
        self.sugerencias_callback = kwargs.pop('sugerencias_callback', None)
        self.buscar_callback = kwargs.pop('buscar_callback', None)
        self.temas_categoria_callback = kwargs.pop('temas_categoria_callback', None)
        self.programar_recordatorio_callback = kwargs.pop('programar_recordatorio_callback', None)
        self.editar_contacto_callback = kwargs.pop('editar_contacto_callback', None)
        self.enviar_resumen_callback = kwargs.pop('enviar_resumen_callback', None)
        self.salir_callback = kwargs.pop('salir_callback', None)
        self.volver_callback = kwargs.pop('volver_callback', None)
        self.profundos_callback = kwargs.pop('profundos_callback', None)
        self.idioma = kwargs.pop('idioma', 'es')
        
        # Debug del idioma al inicializar
        print(f"🎯 MENÚ INICIALIZADO CON IDIOMA: '{self.idioma}' (tipo: {type(self.idioma)})")
        
        super().__init__(**kwargs)
        self.name = 'menu'
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Debug mejorado: Verificar qué idioma está llegando
        print(f"🔍 DEBUG DETALLADO - Idioma recibido en menú:")
        print(f"   - Valor: '{self.idioma}'")
        print(f"   - Tipo: {type(self.idioma)}")
        print(f"   - Longitud: {len(str(self.idioma))}")
        print(f"   - Repr: {repr(self.idioma)}")
        
        # Layout principal
        layout_principal = BoxLayout(
            orientation='vertical',
            padding=dp(0),
            spacing=dp(0)
        )
        
        # Header con título
        header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=[dp(20), dp(20), dp(20), dp(10)]
        )
        
        # Fondo negro para el header
        with header.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 1)  # Negro
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
            header.bind(size=self._update_header_rect, pos=self._update_header_rect)
        
        # Verificación MEJORADA del idioma con múltiples condiciones
        idioma_str = str(self.idioma).lower().strip()
        
        # Condiciones más específicas para detectar inglés
        es_ingles = (
            idioma_str == 'en' or 
            idioma_str == 'english' or 
            idioma_str.startswith('en') or
            'en' in idioma_str or
            'english' in idioma_str
        )
        
        print(f"🔍 Análisis de idioma:")
        print(f"   - String procesado: '{idioma_str}'")
        print(f"   - ¿Es inglés?: {es_ingles}")
        
        # Obtener título y opciones según idioma
        if es_ingles:
            titulo_texto = '===== Preaching Assistant ====='
            print("✅ APLICANDO TEXTOS EN INGLÉS")
            
            opciones_menu = [
                ('sugerencias', 'Suggestions'),
                ('buscar', 'Search'),
                ('temas_profundos', 'Deep Themes'),
                ('programar_recordatorio', 'Schedule Reminder'),
                ('editar_contacto', 'Edit Contact'),
                ('enviar_resumen', 'Send Summary'),
                ('salir', 'Exit'),
                ('volver', 'Back')
            ]
        else:
            titulo_texto = '===== Asistente de Predicación ====='
            print("✅ APLICANDO TEXTOS EN ESPAÑOL")
            
            opciones_menu = [
                ('sugerencias', 'Sugerencias'),
                ('buscar', 'Buscar'),
                ('temas_profundos', 'Temas Profundos'),
                ('programar_recordatorio', 'Programar Recordatorio'),
                ('editar_contacto', 'Editar Contacto'),
                ('enviar_resumen', 'Enviar Resumen'),
                ('salir', 'Salir'),
                ('volver', 'Volver')
            ]
        
        # Crear título
        titulo = Label(
            text=titulo_texto,
            font_size=dp(20),
            bold=True,
            color=(1, 1, 1, 1),  # Blanco
            text_size=(None, None),
            halign='center'
        )
        header.add_widget(titulo)
        layout_principal.add_widget(header)
        
        # Contenedor de botones
        contenedor_botones = BoxLayout(
            orientation='vertical',
            spacing=dp(0),
            padding=dp(0)
        )
        
        # 🌟 CREAR BOTONES DEL MENÚ CON AZUL CIELO 🌟
        for clave, texto_mostrar in opciones_menu:
            boton = Button(
                text=texto_mostrar,
                size_hint_y=None,
                height=dp(80),
                font_size=dp(18),
                bold=True,  # Texto en negrita
                background_color=(0.3, 0.7, 1, 1),  # ✨ AZUL CIELO VIBRANTE ✨
                color=(1, 1, 1, 1),  # Texto blanco
                border=(1, 1, 1, 1)
            )
            
            # Asignar callback según la opción
            if clave == 'sugerencias':
                boton.bind(on_press=self.ir_sugerencias)
            elif clave == 'buscar':
                boton.bind(on_press=self.ir_buscar)
            elif clave == 'temas_profundos':
                boton.bind(on_press=self.ir_temas_profundos)
            elif clave == 'programar_recordatorio':
                boton.bind(on_press=self.ir_programar_recordatorio)
            elif clave == 'editar_contacto':
                boton.bind(on_press=self.ir_editar_contacto)
            elif clave == 'enviar_resumen':
                boton.bind(on_press=self.ir_enviar_resumen)
            elif clave == 'salir':
                boton.bind(on_press=self.salir_aplicacion)
            elif clave == 'volver':
                boton.bind(on_press=self.volver_login)
            
            contenedor_botones.add_widget(boton)
            print(f"✅ Botón '{texto_mostrar}' creado con color azul cielo")
        
        layout_principal.add_widget(contenedor_botones)
        self.add_widget(layout_principal)
        print(f"🎨 Menú creado con idioma {'INGLÉS' if es_ingles else 'ESPAÑOL'} - todos los botones en azul cielo")
    
    def _update_header_rect(self, instance, value):
        """Actualizar el rectángulo del header"""
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size
    
    def actualizar_textos(self):
        """Actualiza todos los textos de la interfaz cuando cambia el idioma"""
        print(f"🔄 Actualizando textos del menú para idioma: {self.idioma}")
        self.clear_widgets()
        self.crear_interfaz()
    
    def cambiar_idioma(self, nuevo_idioma):
        """Método para cambiar el idioma y actualizar la interfaz"""
        print(f"🌍 === CAMBIO DE IDIOMA SOLICITADO ===")
        print(f"🌍 De: '{self.idioma}' a '{nuevo_idioma}'")
        print(f"🌍 Tipo del nuevo idioma: {type(nuevo_idioma)}")
        
        self.idioma = nuevo_idioma
        print(f"🌍 Idioma actualizado en self.idioma: '{self.idioma}'")
        
        self.actualizar_textos()
        print(f"🌍 === CAMBIO DE IDIOMA COMPLETADO ===")
    
    def forzar_idioma(self, idioma):
        """Método para forzar un idioma específico"""
        print(f"🔧 FORZANDO IDIOMA: '{idioma}'")
        self.idioma = idioma
        self.clear_widgets()
        self.crear_interfaz()
        print(f"🔧 IDIOMA FORZADO Y APLICADO: '{idioma}'")
    
    # Métodos de navegación
    def ir_sugerencias(self, instance):
        """Navegar a la pantalla de sugerencias"""
        print("📋 Navegando a Sugerencias...")
        if self.sugerencias_callback:
            self.sugerencias_callback()
        else:
            if self.manager and self.manager.has_screen('sugerencias'):
                self.manager.current = 'sugerencias'
    
    def ir_buscar(self, instance):
        """Navegar a la pantalla de búsqueda"""
        print("🔍 Navegando a Buscar...")
        if self.buscar_callback:
            self.buscar_callback()
        else:
            if self.manager and self.manager.has_screen('buscar'):
                self.manager.current = 'buscar'
    
    def ir_temas_profundos(self, instance):
        """Navegar a temas profundos"""
        print("📚 Navegando a Temas Profundos...")
        if self.profundos_callback:
            self.profundos_callback()
        else:
            if self.manager and self.manager.has_screen('temas_profundos'):
                self.manager.current = 'temas_profundos'
    
    def ir_programar_recordatorio(self, instance):
        """Navegar a programar recordatorio"""
        print("⏰ Navegando a Programar Recordatorio...")
        if self.programar_recordatorio_callback:
            self.programar_recordatorio_callback()
        else:
            print("⚠️ Función de recordatorio no implementada")
    
    def ir_editar_contacto(self, instance):
        """Navegar a editar contacto"""
        print("👤 Navegando a Editar Contacto...")
        if self.editar_contacto_callback:
            self.editar_contacto_callback()
        else:
            print("⚠️ Función de editar contacto no implementada")
    
    def ir_enviar_resumen(self, instance):
        """Navegar a enviar resumen"""
        print("📧 Navegando a Enviar Resumen...")
        if self.enviar_resumen_callback:
            self.enviar_resumen_callback()
        else:
            print("⚠️ Función de enviar resumen no implementada")
    
    def salir_aplicacion(self, instance):
        """Salir de la aplicación"""
        print("🚪 Saliendo de la aplicación...")
        if self.salir_callback:
            self.salir_callback()
        else:
            from kivy.app import App
            App.get_running_app().stop()
    
    def volver_login(self, instance):
        """Volver a la pantalla de login"""
        print("🔙 Volviendo al login...")
        if self.volver_callback:
            self.volver_callback()
        else:
            if self.manager and self.manager.has_screen('login'):
                self.manager.current = 'login'# Actualizado Mon Jun  2 22:59:23 EDT 2025
# Actualizado Mon Jun  2 23:00:39 EDT 2025
