from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, StringProperty
from kivy.logger import Logger

class PantallaAvisoLegal(Screen):
    # Propiedades personalizadas que Kivy reconocerá
    continuar_callback = ObjectProperty(None)
    idioma = StringProperty('es')
    idioma_callback = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info("🔥 === AVISO LEGAL INICIALIZANDO ===")
        Logger.info(f"📋 Callbacks recibidos:")
        Logger.info(f"   ✅ continuar_callback: {kwargs.get('continuar_callback')}")
        Logger.info(f"   ✅ idioma_callback: {kwargs.get('idioma_callback')}")
        Logger.info(f"   ✅ idioma: {kwargs.get('idioma', 'es')}")
        
        # Crear interfaz DIRECTAMENTE sin Clock.schedule_once
        Logger.info("🎨 Iniciando creación de interfaz...")
        self.crear_interfaz()
        Logger.info("🔥 AVISO LEGAL TERMINÓ DE INICIALIZAR - ESPERANDO INTERACCIÓN DEL USUARIO")
    
    def crear_interfaz(self):
        """Crea la interfaz bilingüe del aviso legal"""
        Logger.info("🎨 === CREANDO INTERFAZ AVISO LEGAL ===")
        
        # Layout principal con fondo blanco
        layout_principal = BoxLayout(
            orientation='vertical', 
            padding=20, 
            spacing=15
        )
        Logger.info("✅ Layout principal creado")
        
        # Fondo blanco para toda la pantalla
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 1, 1, 1)  # Blanco
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        Logger.info("✅ Fondo blanco configurado")
        
        # Título bilingüe
        titulo = Label(
            text='📋 AVISO LEGAL / LEGAL NOTICE',
            font_size='22sp',
            size_hint_y=None,
            height='70dp',
            color=(0, 0, 0, 1),  # Negro
            bold=True
        )
        layout_principal.add_widget(titulo)
        Logger.info("✅ Título añadido")
        
        # Botón para cambiar idioma
        btn_idioma = Button(
            text='🌐 English' if self.idioma == 'es' else '🌐 Español',
            size_hint_y=None,
            height='40dp',
            background_color=(0.9, 0.9, 0.9, 1),
            color=(0, 0, 0, 1)
        )
        btn_idioma.bind(on_press=self.cambiar_idioma)
        layout_principal.add_widget(btn_idioma)
        Logger.info("✅ Botón idioma añadido")
        
        # Contenido del aviso legal en ScrollView
        scroll = ScrollView()
        
        self.contenido_label = Label(
            text=self.obtener_texto_aviso_legal(),
            text_size=(None, None),
            halign='left',
            valign='top',
            font_size='13sp',
            color=(0, 0, 0, 1),  # Negro
            markup=True
        )
        
        def actualizar_text_size(instance, size):
            instance.text_size = (size[0] - 40, None)
        
        self.contenido_label.bind(size=actualizar_text_size)
        scroll.add_widget(self.contenido_label)
        layout_principal.add_widget(scroll)
        Logger.info("✅ Contenido scroll añadido")
        
        # Botones con nuevo diseño
        layout_botones = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height='60dp', 
            spacing=15
        )
        
        btn_aceptar = Button(
            text='✅ Acepto / I Accept',
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        btn_aceptar.bind(on_press=self.aceptar_aviso)
        Logger.info("🔥 BOTÓN ACEPTAR CREADO Y VINCULADO")
        
        btn_rechazar = Button(
            text='❌ No Acepto / I Decline',
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        btn_rechazar.bind(on_press=self.rechazar_aviso)
        Logger.info("🔥 BOTÓN RECHAZAR CREADO Y VINCULADO")
        
        layout_botones.add_widget(btn_aceptar)
        layout_botones.add_widget(btn_rechazar)
        layout_principal.add_widget(layout_botones)
        Logger.info("✅ Botones añadidos al layout")
        
        self.add_widget(layout_principal)
        Logger.info("✅ === INTERFAZ AVISO LEGAL COMPLETADA ===")
    
    def _update_rect(self, instance, value):
        """Actualiza el rectángulo de fondo"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def cambiar_idioma(self, instance):
        """Cambia el idioma del aviso legal"""
        Logger.info(f"🌐 === CAMBIO DE IDIOMA ===")
        Logger.info(f"🌐 Idioma anterior: {self.idioma}")
        
        self.idioma = 'en' if self.idioma == 'es' else 'es'
        
        Logger.info(f"🌐 Nuevo idioma: {self.idioma}")
        
        # Actualizar texto del botón
        instance.text = '🌐 English' if self.idioma == 'es' else '🌐 Español'
        
        # Actualizar contenido
        self.contenido_label.text = self.obtener_texto_aviso_legal()
        
        # Llamar callback si existe
        if self.idioma_callback:
            Logger.info("🌐 Ejecutando idioma_callback...")
            self.idioma_callback(self.idioma)
    
    def obtener_texto_aviso_legal(self):
        """Retorna el texto del aviso legal según el idioma"""
        if self.idioma == 'es':
            return """[size=16][b]TÉRMINOS Y CONDICIONES DE USO[/b][/size]

[b]1. ACEPTACIÓN DE TÉRMINOS[/b]
Al utilizar esta aplicación, usted acepta estar sujeto a estos términos y condiciones.

[b]2. USO DE LA APLICACIÓN[/b]
Esta aplicación está diseñada para asistir en actividades de predicación y estudio bíblico.

[b]3. PRIVACIDAD[/b]
Respetamos su privacidad y protegemos sus datos personales de acuerdo con las leyes aplicables.

[b]4. RESPONSABILIDAD[/b]
El usuario es responsable del uso que haga de la información proporcionada por la aplicación.

[b]5. MODIFICACIONES[/b]
Nos reservamos el derecho de modificar estos términos en cualquier momento.

[b]6. CONTACTO[/b]
Para preguntas sobre estos términos, puede contactarnos a través de los canales oficiales.

[i]Última actualización: Junio 2025[/i]"""
        else:
            return """[size=16][b]TERMS AND CONDITIONS OF USE[/b][/size]

[b]1. ACCEPTANCE OF TERMS[/b]
By using this application, you agree to be bound by these terms and conditions.

[b]2. APPLICATION USE[/b]
This application is designed to assist in preaching activities and biblical study.

[b]3. PRIVACY[/b]
We respect your privacy and protect your personal data in accordance with applicable laws.

[b]4. RESPONSIBILITY[/b]
The user is responsible for the use they make of the information provided by the application.

[b]5. MODIFICATIONS[/b]
We reserve the right to modify these terms at any time.

[b]6. CONTACT[/b]
For questions about these terms, you can contact us through official channels.

[i]Last updated: June 2025[/i]"""
    
    def aceptar_aviso(self, instance):
        """Maneja la aceptación del aviso legal"""
        Logger.info("🔥🔥🔥 === BOTÓN ACEPTAR PRESIONADO MANUALMENTE ===")
        Logger.info(f"📱 Instancia del botón: {instance}")
        Logger.info(f"📱 Tipo de instancia: {type(instance)}")
        Logger.info(f"📱 Texto del botón: {getattr(instance, 'text', 'N/A')}")
        Logger.info(f"📋 Callback configurado: {self.continuar_callback}")
        Logger.info(f"📋 Tipo de callback: {type(self.continuar_callback)}")
        Logger.info("✅ Aviso legal aceptado / Legal notice accepted")
        
        if self.continuar_callback:
            Logger.info("🔄 Ejecutando continuar_callback...")
            try:
                self.continuar_callback()
                Logger.info("✅ continuar_callback ejecutado exitosamente")
            except Exception as e:
                Logger.error(f"❌ Error ejecutando continuar_callback: {e}")
                import traceback
                traceback.print_exc()
        elif hasattr(self.manager, 'current'):
            Logger.info("🔄 Cambiando a pantalla login directamente...")
            self.manager.current = 'login'
        else:
            Logger.error("❌ No hay manera de continuar - ni callback ni manager")
        
        Logger.info("✅ === FIN ACEPTAR AVISO ===")
    
    def rechazar_aviso(self, instance):
        """Maneja el rechazo del aviso legal"""
        Logger.info("🔥🔥🔥 === BOTÓN RECHAZAR PRESIONADO ===")
        Logger.info(f"📱 Instancia del botón: {instance}")
        Logger.info(f"📱 Tipo de instancia: {type(instance)}")
        Logger.info(f"📱 Texto del botón: {getattr(instance, 'text', 'N/A')}")
        Logger.info("❌ Aviso legal rechazado / Legal notice declined")
        Logger.info("🚫 Cerrando aplicación...")
        
        import sys
        sys.exit()
    
    # Métodos de respaldo si no se pasan callbacks
    def on_continuar_callback(self, instance, value):
        Logger.info(f"🔄 on_continuar_callback: {value}")
        if value is None:
            self.continuar_callback = lambda: Logger.info("🔄 Función continuar no implementada")
    
    def on_idioma_callback(self, instance, value):
        Logger.info(f"🌐 on_idioma_callback: {value}")
        if value is None:
            self.idioma_callback = lambda idioma: Logger.info("🌐 Función idioma no implementada")