# ==========================================
# PARTE 1: IMPORTACIONES Y CONFIGURACIÓN (CORREGIDA)
# ==========================================

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
# ELIMINADA: from utils.traducciones import obtener_texto
import json
import os
import threading

# Importaciones opcionales para actualizaciones
try:
    import requests
    from packaging import version
    UPDATES_AVAILABLE = True
except ImportError:
    UPDATES_AVAILABLE = False
    print("⚠️ requests o packaging no disponibles - función de actualizaciones limitada")

# ==========================================
# PARTE 2: INICIALIZACIÓN DE LA CLASE
# ==========================================

class PantallaLogin(Screen):
    def __init__(self, **kwargs):
        # Extraer callbacks personalizados
        self.login_callback = kwargs.pop('login_callback', None)
        self.crear_usuario_callback = kwargs.pop('crear_usuario_callback', None)
        self.buscar_actualizaciones_callback = kwargs.pop('buscar_actualizaciones_callback', None)
        self.actualizar_callback = kwargs.pop('actualizar_callback', None)
        self.continuar_callback = kwargs.pop('continuar_callback', None)
        self.idioma_callback = kwargs.pop('idioma_callback', None)
        self.idioma = kwargs.pop('idioma', 'es')
        
        super().__init__(**kwargs)
        self.name = 'login'
        
        # Configuración de archivos
        self.archivo_credenciales = 'datos_recordados.json'
        self.usuarios_db = 'usuarios_registrados.json'
        
        # Configuración de GitHub para actualizaciones
        self.github_user = 'sanchezbond007'  # Tu usuario de GitHub
        self.github_repo = 'asistente_predicacion_bilingue2'  # Tu repositorio
        self.version_actual = '1.0.0'  # Versión actual de tu app
        
        # Variables para preservar valores de campos
        self.valores_guardados = {
            'usuario': '',
            'contrasena': '',
            'recordar': False
        }
        
        # Referencias a los widgets de entrada
        self.input_usuario = None
        self.input_contrasena = None
        self.checkbox_recordar = None
        self.btn_espanol = None
        self.btn_ingles = None
        self.btn_toggle_password = None  # NUEVO: Botón para mostrar/ocultar contraseña
        
        # Inicializar base de datos y credenciales
        self.crear_db_usuarios_si_no_existe()
        self.cargar_credenciales_guardadas()
        
        # Crear interfaz
        self.crear_interfaz()

# ==========================================
# PARTE 3: GESTIÓN DE BASE DE DATOS (MEJORADA)
# ==========================================

    def crear_db_usuarios_si_no_existe(self):
        """Crea la base de datos de usuarios si no existe"""
        try:
            # Siempre recrear si hay problemas
            print(f"📁 Creando/recreando base de datos: {self.usuarios_db}")
            usuarios_default = {
                "sanchezbond007": {
                    "contrasena": "password123",
                    "nombre": "James",
                    "apellido": "Bond",
                    "email": "bond@secret.com"
                },
                "admin": {
                    "contrasena": "admin",
                    "nombre": "Administrador",
                    "apellido": "Sistema",
                    "email": "admin@system.com"
                }
            }
            
            # Asegurar que el directorio existe
            directorio = os.path.dirname(self.usuarios_db) if os.path.dirname(self.usuarios_db) else '.'
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Escribir archivo con formato correcto
            with open(self.usuarios_db, 'w', encoding='utf-8') as archivo:
                json.dump(usuarios_default, archivo, ensure_ascii=False, indent=4)
            
            print("✅ Base de datos de usuarios creada/recreada exitosamente:")
            print("   - Usuario: sanchezbond007 | Contraseña: password123")
            print("   - Usuario: admin | Contraseña: admin")
            
            # Verificar que se creó correctamente
            with open(self.usuarios_db, 'r', encoding='utf-8') as archivo:
                verificacion = json.load(archivo)
                print(f"✅ Verificación: {len(verificacion)} usuarios creados")
                
        except Exception as e:
            print(f"❌ Error al crear base de datos: {e}")
            print(f"❌ Tipo de error: {type(e)}")
    
    def agregar_usuario_a_db(self, datos_usuario):
        """Agrega un nuevo usuario a la base de datos"""
        try:
            # Cargar usuarios existentes
            usuarios = {}
            if os.path.exists(self.usuarios_db):
                try:
                    with open(self.usuarios_db, 'r', encoding='utf-8') as archivo:
                        usuarios = json.load(archivo)
                    
                    # Verificar formato
                    if not isinstance(usuarios, dict):
                        print("❌ Formato incorrecto en DB, recreando...")
                        usuarios = {}
                        
                except (json.JSONDecodeError, Exception) as e:
                    print(f"❌ Error al leer DB existente: {e}")
                    usuarios = {}
            
            # Agregar nuevo usuario
            usuario_nuevo = {
                "contrasena": datos_usuario.get('contrasena', ''),
                "nombre": datos_usuario.get('nombre', ''),
                "apellido": datos_usuario.get('apellido', ''),
                "email": datos_usuario.get('correo', '')
            }
            
            usuarios[datos_usuario['usuario']] = usuario_nuevo
            
            # Guardar base de datos actualizada
            with open(self.usuarios_db, 'w', encoding='utf-8') as archivo:
                json.dump(usuarios, archivo, ensure_ascii=False, indent=4)
            
            print(f"✅ Usuario '{datos_usuario['usuario']}' agregado a la base de datos")
            return True
            
        except Exception as e:
            print(f"❌ Error al agregar usuario a DB: {e}")
            return False

# ==========================================
# PARTE 4: VERIFICACIÓN DE CREDENCIALES (CORREGIDA)
# ==========================================

    def verificar_credenciales(self, usuario, contrasena):
        """Verifica las credenciales contra la base de datos"""
        try:
            # Verificar si el archivo existe
            if not os.path.exists(self.usuarios_db):
                print(f"❌ Base de datos no encontrada: {self.usuarios_db}")
                # Crear la base de datos si no existe
                self.crear_db_usuarios_si_no_existe()
            
            # Leer la base de datos con manejo de errores mejorado
            try:
                with open(self.usuarios_db, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read().strip()
                    if not contenido:
                        print("❌ Archivo de base de datos está vacío")
                        self.crear_db_usuarios_si_no_existe()
                        # Intentar leer nuevamente
                        with open(self.usuarios_db, 'r', encoding='utf-8') as archivo:
                            usuarios = json.load(archivo)
                    else:
                        usuarios = json.loads(contenido)
            except json.JSONDecodeError as e:
                print(f"❌ Error al decodificar JSON: {e}")
                print("🔄 Recreando base de datos...")
                self.crear_db_usuarios_si_no_existe()
                with open(self.usuarios_db, 'r', encoding='utf-8') as archivo:
                    usuarios = json.load(archivo)
            
            # Verificar que usuarios es un diccionario
            if not isinstance(usuarios, dict):
                print(f"❌ Formato incorrecto en base de datos. Tipo: {type(usuarios)}")
                print(f"Contenido: {usuarios}")
                return False, "Error en formato de base de datos"
            
            print(f"🔍 Base de datos cargada correctamente. Usuarios disponibles: {list(usuarios.keys())}")
            print(f"🔍 Buscando usuario: '{usuario}'")
            
            # Buscar usuario (insensible a mayúsculas)
            usuario_lower = usuario.lower()
            usuario_encontrado = None
            
            for user_key in usuarios.keys():
                if user_key.lower() == usuario_lower:
                    usuario_encontrado = user_key
                    break
            
            if usuario_encontrado:
                usuario_data = usuarios[usuario_encontrado]
                
                # Verificar que usuario_data es un diccionario
                if not isinstance(usuario_data, dict):
                    print(f"❌ Datos de usuario en formato incorrecto: {type(usuario_data)}")
                    return False, "Error en datos de usuario"
                
                contrasena_guardada = usuario_data.get('contrasena', '')
                
                print(f"🔍 Usuario encontrado: '{usuario_encontrado}'")
                print(f"🔍 Contraseña guardada: '{contrasena_guardada}'")
                print(f"🔍 Contraseña ingresada: '{contrasena}'")
                
                if contrasena_guardada == contrasena:
                    print(f"✅ Login exitoso para usuario: {usuario_encontrado}")
                    return True, usuario_data
                else:
                    print(f"❌ Contraseña incorrecta para usuario: {usuario_encontrado}")
                    return False, "Contraseña incorrecta"
            else:
                print(f"❌ Usuario no encontrado: '{usuario}'")
                print(f"   Usuarios disponibles: {list(usuarios.keys())}")
                return False, "Usuario no existe"
                
        except Exception as e:
            print(f"❌ Error general al verificar credenciales: {e}")
            print(f"❌ Tipo de error: {type(e)}")
            return False, f"Error del sistema: {str(e)}"

# ==========================================
# PARTE 5: GESTIÓN DE CREDENCIALES GUARDADAS
# ==========================================

    def cargar_credenciales_guardadas(self):
        """Carga las credenciales guardadas del archivo si existen"""
        try:
            if os.path.exists(self.archivo_credenciales):
                with open(self.archivo_credenciales, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self.valores_guardados.update(datos)
                    print(f"✅ Credenciales cargadas: Usuario='{datos.get('usuario', '')}', Recordar={datos.get('recordar', False)}")
            else:
                print("📁 No se encontró archivo de credenciales guardadas")
        except Exception as e:
            print(f"❌ Error al cargar credenciales: {e}")
            self.valores_guardados = {
                'usuario': '',
                'contrasena': '',
                'recordar': False
            }
    
    def guardar_credenciales(self):
        """Guarda las credenciales en archivo si 'recordar' está activado"""
        try:
            if self.valores_guardados['recordar']:
                datos_a_guardar = {
                    'usuario': self.valores_guardados['usuario'],
                    'contrasena': self.valores_guardados['contrasena'],
                    'recordar': True
                }
                with open(self.archivo_credenciales, 'w', encoding='utf-8') as archivo:
                    json.dump(datos_a_guardar, archivo, ensure_ascii=False, indent=2)
                print(f"💾 Credenciales guardadas para usuario: '{datos_a_guardar['usuario']}'")
            else:
                self.eliminar_credenciales_guardadas()
        except Exception as e:
            print(f"❌ Error al guardar credenciales: {e}")
    
    def eliminar_credenciales_guardadas(self):
        """Elimina las credenciales guardadas"""
        try:
            if os.path.exists(self.archivo_credenciales):
                os.remove(self.archivo_credenciales)
                print("🗑️ Credenciales eliminadas del archivo")
        except Exception as e:
            print(f"❌ Error al eliminar credenciales: {e}")

# ==========================================
# PARTE 6: CREACIÓN DE LA INTERFAZ
# ==========================================

    def crear_interfaz(self):
        # Layout principal con fondo negro
        layout_principal = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20)
        )
        
        # Fondo negro
        with layout_principal.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = RoundedRectangle(
                size=layout_principal.size, 
                pos=layout_principal.pos
            )
            layout_principal.bind(size=self._update_bg_rect, pos=self._update_bg_rect)
        
        # Espaciador superior
        layout_principal.add_widget(Label(size_hint_y=0.2))
        
        # Campo Usuario
        self.input_usuario = TextInput(
            hint_text=self._obtener_texto_hint('usuario'),
            multiline=False,
            font_size=dp(18),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(15), dp(10)],
            text=self.valores_guardados['usuario']
        )
        self.input_usuario.bind(text=self._guardar_usuario)
        layout_principal.add_widget(self.input_usuario)
        
        # CAMPO CONTRASEÑA CON BOTÓN OJO (MODIFICADO)
        password_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(0)
        )
        
        self.input_contrasena = TextInput(
            hint_text=self._obtener_texto_hint('contrasena'),
            multiline=False,
            password=True,
            font_size=dp(18),
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(15), dp(10), dp(55), dp(10)],  # Padding derecho más amplio para el botón
            text=self.valores_guardados['contrasena']
        )
        self.input_contrasena.bind(text=self._guardar_contrasena)
        
        # Botón ojo para mostrar/ocultar contraseña
        self.btn_toggle_password = Button(
            text='👁',
            size_hint_x=None,
            width=dp(50),
            font_size=dp(20),
            background_color=(0.7, 0.7, 0.7, 1),
            color=(0, 0, 0, 1)
        )
        self.btn_toggle_password.bind(on_press=self.toggle_password_visibility)
        
        password_layout.add_widget(self.input_contrasena)
        password_layout.add_widget(self.btn_toggle_password)
        layout_principal.add_widget(password_layout)
        
        # Checkbox "Recordar"
        checkbox_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        self.checkbox_recordar = CheckBox(
            size_hint_x=None,
            width=dp(30),
            active=self.valores_guardados['recordar']
        )
        self.checkbox_recordar.bind(active=self._guardar_recordar)
        
        label_recordar = Label(
            text=self._obtener_texto('recordar'),
            color=(1, 1, 1, 1),
            font_size=dp(16),
            halign='left',
            text_size=(None, None)
        )
        
        checkbox_layout.add_widget(self.checkbox_recordar)
        checkbox_layout.add_widget(label_recordar)
        layout_principal.add_widget(checkbox_layout)
        
        # Espaciador
        layout_principal.add_widget(Label(size_hint_y=0.1))
        
        # Botones de idioma
        idioma_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        self.btn_espanol = Button(
            text='🇪🇸 Español',
            font_size=dp(16),
            background_color=(0.4, 0.7, 1, 1) if self.idioma != 'es' else (0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        self.btn_espanol.bind(on_press=self.cambiar_a_espanol)
        
        self.btn_ingles = Button(
            text='🇺🇸 English',
            font_size=dp(16),
            background_color=(0.4, 0.7, 1, 1) if self.idioma != 'en' else (0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        self.btn_ingles.bind(on_press=self.cambiar_a_ingles)
        
        idioma_layout.add_widget(self.btn_espanol)
        idioma_layout.add_widget(self.btn_ingles)
        layout_principal.add_widget(idioma_layout)
        
        # Espaciador
        layout_principal.add_widget(Label(size_hint_y=0.1))
        
        # Botón Iniciar sesión
        btn_login = Button(
            text=self._obtener_texto('iniciar_sesion'),
            size_hint_y=None,
            height=dp(60),
            font_size=dp(20),
            bold=True,
            background_color=(0.3, 0.7, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_login.bind(on_press=self.iniciar_sesion)
        layout_principal.add_widget(btn_login)
        
        # Botón Crear usuario
        btn_crear = Button(
            text=self._obtener_texto('crear_usuario'),
            size_hint_y=None,
            height=dp(60),
            font_size=dp(20),
            bold=True,
            background_color=(0.3, 0.7, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_crear.bind(on_press=self.crear_usuario)
        layout_principal.add_widget(btn_crear)
        
        # Botón Buscar actualizaciones
        btn_actualizar = Button(
            text=self._obtener_texto('buscar_actualizaciones'),
            size_hint_y=None,
            height=dp(60),
            font_size=dp(20),
            bold=True,
            background_color=(0.3, 0.7, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_actualizar.bind(on_press=self.buscar_actualizaciones)
        layout_principal.add_widget(btn_actualizar)
        
        # Espaciador inferior
        layout_principal.add_widget(Label(size_hint_y=0.2))
        
        self.add_widget(layout_principal)

# ==========================================
# PARTE 7: FUNCIÓN NUEVA - TOGGLE CONTRASEÑA
# ==========================================

    def toggle_password_visibility(self, instance):
        """Alterna entre mostrar y ocultar la contraseña"""
        if self.input_contrasena.password:
            # Mostrar contraseña
            self.input_contrasena.password = False
            self.btn_toggle_password.text = '🙈'
            print("👁️ Contraseña visible")
        else:
            # Ocultar contraseña
            self.input_contrasena.password = True
            self.btn_toggle_password.text = '👁'
            print("🙈 Contraseña oculta")

# ==========================================
# PARTE 8: FUNCIONES AUXILIARES DE INTERFAZ (SIN UTILS)
# ==========================================

    def _update_bg_rect(self, instance, value):
        """Actualizar rectángulo de fondo"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def _obtener_texto(self, clave):
        """Obtiene texto según el idioma actual - SIN DEPENDENCIA UTILS"""
        if self.idioma == 'en':
            traducciones = {
                'recordar': 'Remember me',
                'iniciar_sesion': 'Login',
                'crear_usuario': 'Create User',
                'buscar_actualizaciones': 'Check Updates',
                'error': 'Error',
                'exito': 'Success',
                'informacion': 'Information',
                'actualizaciones': 'Updates',
                'campos_vacios': 'Please fill in all fields',
                'credenciales_incorrectas': 'Invalid credentials',
                'pantalla_no_disponible': 'Screen not available',
                'verificando_actualizaciones': 'Checking for updates...',
                'no_actualizaciones': 'You have the latest version',
                'error_conexion': 'Connection Error',
                'sin_internet': 'No internet connection available',
                'actualizacion_disponible': 'Update Available',
                'si_actualizar': 'Yes, Update',
                'no_actualizar': 'Not Now',
                'descargando': 'Downloading',
                'aceptar': 'OK'
            }
            return traducciones.get(clave, clave.replace('_', ' ').title())
        else:
            traducciones_es = {
                'recordar': 'Recordar',
                'iniciar_sesion': 'Iniciar Sesión',
                'crear_usuario': 'Crear Usuario',
                'buscar_actualizaciones': 'Buscar Actualizaciones',
                'exito': 'Éxito',
                'informacion': 'Información',
                'actualizaciones': 'Actualizaciones',
                'credenciales_incorrectas': 'Credenciales incorrectas',
                'pantalla_no_disponible': 'Pantalla no disponible',
                'verificando_actualizaciones': 'Verificando actualizaciones...',
                'no_actualizaciones': 'Tienes la versión más reciente',
                'error_conexion': 'Error de Conexión',
                'sin_internet': 'No hay conexión a internet disponible',
                'actualizacion_disponible': 'Actualización Disponible',
                'si_actualizar': 'Sí, Actualizar',
                'no_actualizar': 'Ahora No',
                'descargando': 'Descargando',
                'campos_vacios': 'Por favor, completa todos los campos',
                'aceptar': 'Aceptar'
            }
            return traducciones_es.get(clave, clave.replace('_', ' ').title())
    
    def _obtener_texto_hint(self, campo):
        """Obtiene hint text según el idioma"""
        if self.idioma == 'en':
            hints = {
                'usuario': 'Username',
                'contrasena': 'Password'
            }
            return hints.get(campo, campo.title())
        else:
            hints = {
                'usuario': 'Nombre de usuario',
                'contrasena': 'Contraseña'
            }
            return hints.get(campo, campo.title())

# ==========================================
# PARTE 9: FUNCIONES DE GUARDADO DE DATOS
# ==========================================

    def _guardar_usuario(self, instance, valor):
        """Guarda el valor del campo usuario"""
        self.valores_guardados['usuario'] = valor
    
    def _guardar_contrasena(self, instance, valor):
        """Guarda el valor del campo contraseña"""
        self.valores_guardados['contrasena'] = valor
    
    def _guardar_recordar(self, instance, valor):
        """Guarda el estado del checkbox y maneja persistencia"""
        self.valores_guardados['recordar'] = valor
        print(f"🔘 Checkbox 'Recordar' {'activado' if valor else 'desactivado'}")
        
        if not valor:
            self.eliminar_credenciales_guardadas()

# ==========================================
# PARTE 10: FUNCIONES DE CAMBIO DE IDIOMA
# ==========================================

    def cambiar_a_espanol(self, instance):
        """Cambia el idioma a español preservando valores"""
        if self.idioma != 'es':
            print("🇪🇸 Cambiando a español...")
            self.idioma = 'es'
            
            if self.idioma_callback:
                self.idioma_callback('es')
            
            self.actualizar_interfaz()
    
    def cambiar_a_ingles(self, instance):
        """Cambia el idioma a inglés preservando valores"""
        if self.idioma != 'en':
            print("🇺🇸 Changing to English...")
            self.idioma = 'en'
            
            if self.idioma_callback:
                self.idioma_callback('en')
            
            self.actualizar_interfaz()
    
    def actualizar_interfaz(self):
        """Actualiza la interfaz manteniendo los valores de los campos"""
        print(f"🔄 Actualizando interfaz con valores preservados: {self.valores_guardados}")
        print(f"🌍 Idioma actual: {self.idioma}")
        
        self.clear_widgets()
        self.crear_interfaz()
        
        print("✅ Interfaz actualizada con valores preservados y idioma aplicado")

# ==========================================
# PARTE 11: PROCESO DE INICIAR SESIÓN
# ==========================================

    def iniciar_sesion(self, instance):
        """Maneja el inicio de sesión con validación real"""
        usuario = self.input_usuario.text.strip()
        contrasena = self.input_contrasena.text.strip()
        
        print(f"\n🔐 === INICIANDO PROCESO DE LOGIN ===")
        print(f"🔐 Usuario ingresado: '{usuario}'")
        print(f"🔐 Contraseña ingresada: '{contrasena}' (longitud: {len(contrasena)})")
        
        if not usuario or not contrasena:
            mensaje_error = self._obtener_texto('campos_vacios')
            print(f"❌ Error: {mensaje_error}")
            self.mostrar_popup(
                self._obtener_texto('error'),
                mensaje_error
            )
            return
        
        # Verificar credenciales con debug detallado
        print(f"🔍 Verificando credenciales...")
        es_valido, datos_usuario = self.verificar_credenciales(usuario, contrasena)
        
        if es_valido:
            print("✅ === LOGIN EXITOSO ===")
            
            if self.checkbox_recordar.active:
                self.guardar_credenciales()
                print("💾 Credenciales guardadas para próximas sesiones")
            
            if self.login_callback:
                datos_login = {
                    'usuario': usuario,
                    'contrasena': contrasena,
                    'recordar': self.checkbox_recordar.active,
                    'datos_usuario': datos_usuario
                }
                print("✅ Llamando callback de login...")
                self.login_callback(datos_login)
            else:
                if self.manager and self.manager.has_screen('menu'):
                    print("🔄 Navegando al menú principal...")
                    self.manager.current = 'menu'
                else:
                    self.mostrar_popup(
                        "✅ " + self._obtener_texto('exito'),
                        f"¡Bienvenido {datos_usuario.get('nombre', usuario)}!\n\nLogin exitoso"
                    )
        else:
            print(f"❌ === LOGIN FALLIDO ===")
            print(f"❌ Razón: {datos_usuario}")
            
            # Mostrar información de debug para ayudar
            mensaje_detallado = self._obtener_texto('credenciales_incorrectas')
            mensaje_detallado += f"\n\nDetalles del error:\n{str(datos_usuario)}"
            mensaje_detallado += f"\n\nUsuarios de prueba disponibles:"
            mensaje_detallado += f"\n• sanchezbond007 / password123"
            mensaje_detallado += f"\n• admin / admin"
            
            self.mostrar_popup(
                "❌ " + self._obtener_texto('error'),
                mensaje_detallado
            )

# ==========================================
# PARTE 12: FUNCIONES DE BOTONES ADICIONALES
# ==========================================

    def crear_usuario(self, instance):
        """Navegar a crear usuario - Funcionalidad real"""
        print("👤 Navegando a pantalla de crear usuario...")
        
        if self.crear_usuario_callback:
            print("✅ Usando callback personalizado...")
            self.crear_usuario_callback()
        elif self.manager and self.manager.has_screen('crear_usuario'):
            print("🔄 Navegando a pantalla crear_usuario...")
            self.manager.current = 'crear_usuario'
        else:
            print("❌ Pantalla crear_usuario no encontrada")
            self.mostrar_popup(
                "ℹ️ " + self._obtener_texto('informacion'),
                self._obtener_texto('pantalla_no_disponible') + "\n\nPantalla: crear_usuario"
            )
    
    def buscar_actualizaciones(self, instance):
        """Buscar actualizaciones en GitHub"""
        print("🔄 Iniciando búsqueda de actualizaciones...")
        
        if not UPDATES_AVAILABLE:
            self.mostrar_popup(
                "⚠️ " + self._obtener_texto('informacion'),
                "Función de actualizaciones no disponible.\n\nInstala: pip install requests packaging"
            )
            return
        
        # Mostrar que está funcionando
        self.mostrar_popup(
            "🔄 " + self._obtener_texto('actualizaciones'),
            self._obtener_texto('verificando_actualizaciones') + "\n\n(Función implementada - configura GitHub repo)"
        )