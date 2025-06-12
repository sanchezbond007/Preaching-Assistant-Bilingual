# popup_estudiante.py
# POPUP PARA CAPTURAR NOMBRE DEL ESTUDIANTE DESPUÉS DEL LOGIN

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

class PopupEstudiante:
    """Clase para manejar el popup de captura de estudiante"""
    
    def __init__(self, main_app, idioma='es'):
        self.main_app = main_app
        self.idioma = idioma
        self.popup = None
        
        # Textos en español e inglés
        self.textos = {
            'es': {
                'titulo': '👤 ¡Bienvenido!',
                'pregunta': '¿Con quién vamos a estudiar hoy?',
                'placeholder': 'Nombre del interesado...',
                'ejemplo': 'Ej: María González',
                'btn_continuar': 'Continuar',
                'btn_skip': 'Solo Estudiar',
                'info_skip': '(Sin registrar nombre)',
                'validacion': 'Por favor ingresa un nombre válido'
            },
            'en': {
                'titulo': '👤 Welcome!',
                'pregunta': 'Who are we studying with today?',
                'placeholder': 'Name of the student...',
                'ejemplo': 'Ex: Maria Gonzalez',
                'btn_continuar': 'Continue',
                'btn_skip': 'Just Study',
                'info_skip': '(Without registering name)',
                'validacion': 'Please enter a valid name'
            }
        }
    
    def mostrar_popup(self):
        """Mostrar el popup de captura de estudiante"""
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )
        
        # Pregunta principal
        pregunta_label = Label(
            text=self.textos[self.idioma]['pregunta'],
            font_size=dp(16),
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.6, 0.9, 1),
            halign='center'
        )
        pregunta_label.bind(size=pregunta_label.setter('text_size'))
        content.add_widget(pregunta_label)
        
        # Campo de entrada
        self.nombre_input = TextInput(
            hint_text=self.textos[self.idioma]['placeholder'],
            size_hint_y=None,
            height=dp(45),
            font_size=dp(14),
            multiline=False,
            background_color=(1, 1, 1, 0.9)
        )
        content.add_widget(self.nombre_input)
        
        # Ejemplo
        ejemplo_label = Label(
            text=self.textos[self.idioma]['ejemplo'],
            font_size=dp(11),
            size_hint_y=None,
            height=dp(25),
            color=(0.7, 0.7, 0.7, 1),
            italic=True
        )
        content.add_widget(ejemplo_label)
        
        # Espaciador
        content.add_widget(Label(size_hint_y=None, height=dp(10)))
        
        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Botón Continuar
        btn_continuar = Button(
            text=self.textos[self.idioma]['btn_continuar'],
            background_color=(0.2, 0.7, 0.2, 1),
            font_size=dp(14)
        )
        btn_continuar.bind(on_press=self.continuar_con_nombre)
        botones_layout.add_widget(btn_continuar)
        
        # Botón Skip
        btn_skip = Button(
            text=self.textos[self.idioma]['btn_skip'],
            background_color=(0.6, 0.6, 0.6, 1),
            font_size=dp(14)
        )
        btn_skip.bind(on_press=self.continuar_sin_nombre)
        botones_layout.add_widget(btn_skip)
        
        content.add_widget(botones_layout)
        
        # Info del skip
        skip_info = Label(
            text=self.textos[self.idioma]['info_skip'],
            font_size=dp(10),
            size_hint_y=None,
            height=dp(20),
            color=(0.6, 0.6, 0.6, 1),
            italic=True
        )
        content.add_widget(skip_info)
        
        # Crear popup
        self.popup = Popup(
            title=self.textos[self.idioma]['titulo'],
            content=content,
            size_hint=(0.85, 0.6),
            auto_dismiss=False  # No se puede cerrar sin elegir
        )
        
        # Focus en el campo de texto
        self.popup.bind(on_open=self.on_popup_open)
        
        # Enter para continuar
        self.nombre_input.bind(on_text_validate=self.continuar_con_nombre)
        
        self.popup.open()
    
    def on_popup_open(self, instance):
        """Cuando se abre el popup, hacer focus en el input"""
        self.nombre_input.focus = True
    
    def continuar_con_nombre(self, instance):
        """Continuar con el nombre ingresado"""
        nombre = self.nombre_input.text.strip()
        
        if len(nombre) >= 2:  # Validación mínima
            # Importar y usar TU historial individual existente
            from pantallas.send_resume_individual import HistorialIndividual
            
            historial = HistorialIndividual()
            
            # Crear o seleccionar estudiante usando TU lógica
            exito, estudiante_id = historial.crear_estudiante(nombre)
            
            if not exito:
                # Si ya existe, seleccionarlo por nombre
                estudiantes = historial.obtener_estudiantes()
                for est_id, est_nombre in estudiantes.items():
                    if est_nombre.lower() == nombre.lower():
                        historial.seleccionar_estudiante(est_id)
                        print(f"📚 Estudiante existente seleccionado: {nombre}")
                        break
            else:
                # Si es nuevo, seleccionarlo
                historial.seleccionar_estudiante(estudiante_id)
                print(f"🆕 Nuevo estudiante creado: {nombre}")
            
            # Iniciar nueva sesión usando TU método
            historial.iniciar_nueva_sesion()
            
            print(f"✅ Estudiante activo: {nombre}")
            print(f"🎯 Sesión iniciada - Listo para registrar consultas")
            
            # Cerrar popup y continuar al menú
            self.popup.dismiss()
            self.main_app.ir_al_menu()
            
        else:
            # Mostrar error de validación
            self.mostrar_error_validacion()
    
    def continuar_sin_nombre(self, instance):
        """Continuar sin registrar nombre"""
        print("⚠️ Continuando sin registrar estudiante")
        
        # Cerrar popup y continuar al menú
        self.popup.dismiss()
        self.main_app.ir_al_menu()
    
    def mostrar_error_validacion(self):
        """Mostrar error de validación"""
        # Cambiar color del input temporalmente
        self.nombre_input.background_color = (1, 0.8, 0.8, 1)
        
        # Crear label de error
        if not hasattr(self, 'error_label'):
            self.error_label = Label(
                text=self.textos[self.idioma]['validacion'],
                font_size=dp(11),
                size_hint_y=None,
                height=dp(25),
                color=(1, 0.3, 0.3, 1)
            )
            # Insertar antes de los botones
            self.popup.content.add_widget(self.error_label, index=4)
        
        # Restaurar color después de 2 segundos
        from kivy.clock import Clock
        Clock.schedule_once(self.restaurar_color_input, 2)
    
    def restaurar_color_input(self, dt):
        """Restaurar color normal del input"""
        self.nombre_input.background_color = (1, 1, 1, 0.9)
        if hasattr(self, 'error_label'):
            self.popup.content.remove_widget(self.error_label)
            delattr(self, 'error_label')


# FUNCIÓN AUXILIAR PARA INTEGRAR EN main.py
def mostrar_popup_estudiante(main_app, idioma='es'):
    """
    Función para mostrar el popup desde main.py
    
    Usar después del login exitoso:
    
    def iniciar_sesion(self, instance):
        # ... validación de login ...
        if login_exitoso:
            from popup_estudiante import mostrar_popup_estudiante
            mostrar_popup_estudiante(self, self.idioma)
    """
    popup = PopupEstudiante(main_app, idioma)
    popup.mostrar_popup()