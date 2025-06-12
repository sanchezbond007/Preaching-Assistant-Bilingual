# gestor_navegacion.py
"""
GestorNavegacion - Sistema centralizado de navegación para Asistente de Predicación
Autor: Integración con código existente
Fecha: Junio 2025
"""

from kivy.uix.screenmanager import SlideTransition, FadeTransition, NoTransition
from kivy.clock import Clock
import time
import json
import os

class GestorNavegacion:
    """
    Gestor centralizado de navegación que maneja todas las transiciones
    entre pantallas de manera consistente y validada.
    """
    
    def __init__(self, app_instance):
        """
        Inicializa el gestor de navegación
        
        Args:
            app_instance: Instancia de la aplicación Kivy principal
        """
        self.app = app_instance
        self.inicializar_configuracion()
        
        print("🧭 GestorNavegacion inicializado")
    
    def inicializar_configuracion(self):
        """Inicializa la configuración del gestor"""
        
        # Configuraciones de transición
        self.transiciones_disponibles = {
            'slide': SlideTransition,
            'fade': FadeTransition, 
            'none': NoTransition
        }
        
        # Configuraciones personalizadas por ruta
        self.configuraciones_navegacion = {
            # Flujo principal
            'aviso_legal->login': {
                'transicion': 'slide',
                'direccion': 'left',
                'duracion': 0.3,
                'validaciones': []
            },
            'login->send_resume': {
                'transicion': 'slide', 
                'direccion': 'left',
                'duracion': 0.3,
                'validaciones': ['usuario_autenticado']
            },
            'send_resume->menu': {
                'transicion': 'slide',
                'direccion': 'left', 
                'duracion': 0.3,
                'validaciones': ['usuario_autenticado']
            },
            
            # Navegación desde menú
            'menu->*': {  # Comodín para cualquier pantalla desde menú
                'transicion': 'slide',
                'direccion': 'left',
                'duracion': 0.3,
                'validaciones': ['usuario_autenticado']
            },
            
            # Vuelta al menú
            '*->menu': {  # Comodín para volver al menú
                'transicion': 'slide', 
                'direccion': 'right',
                'duracion': 0.3,
                'validaciones': ['usuario_autenticado']
            }
        }
        
        # Validadores disponibles
        self.validadores = {
            'usuario_autenticado': self._validar_usuario_autenticado,
            'pantalla_existe': self._validar_pantalla_existe,
            'gestor_temas_disponible': self._validar_gestor_temas
        }
        
        # Interceptores (funciones que se ejecutan antes/después de navegar)
        self.interceptores_pre = []
        self.interceptores_post = []
        
        # Historial de navegación
        self.historial = []
        self.indice_historial = -1
        
        # Estado interno
        self.navegacion_en_progreso = False
        self.pantalla_anterior = None
    
    def navegar_a(self, destino, datos=None, transicion_personalizada=None, forzar=False):
        """
        Navega a una pantalla específica con validaciones y configuraciones.
        
        Args:
            destino (str): Nombre de la pantalla destino
            datos (dict): Datos opcionales para pasar a la pantalla
            transicion_personalizada (dict): Configuración específica de transición
            forzar (bool): Si True, ignora las validaciones
            
        Returns:
            bool: True si la navegación fue exitosa, False si falló
        """
        
        if self.navegacion_en_progreso:
            print("⚠️ Navegación ya en progreso, ignorando solicitud")
            return False
        
        print(f"🧭 === NAVEGANDO A: {destino} ===")
        
        try:
            self.navegacion_en_progreso = True
            
            # 1. Validaciones previas
            if not forzar and not self._ejecutar_validaciones(destino):
                print(f"❌ Validaciones fallaron para '{destino}'")
                return False
            
            # 2. Ejecutar interceptores pre-navegación
            if not self._ejecutar_interceptores_pre(destino, datos):
                print(f"❌ Interceptores pre-navegación fallaron para '{destino}'")
                return False
            
            # 3. Preparar pantalla destino
            self._preparar_pantalla_destino(destino, datos)
            
            # 4. Configurar y aplicar transición
            self._aplicar_transicion(destino, transicion_personalizada)
            
            # 5. Realizar navegación
            pantalla_origen = self.app.root.current
            self.app.root.current = destino
            
            # 6. Actualizar estado y historial
            self._actualizar_estado_navegacion(pantalla_origen, destino)
            
            # 7. Ejecutar interceptores post-navegación (asíncrono)
            Clock.schedule_once(lambda dt: self._ejecutar_interceptores_post(destino, datos), 0.1)
            
            print(f"✅ Navegación a '{destino}' completada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error durante navegación a '{destino}': {e}")
            return False
        finally:
            self.navegacion_en_progreso = False
    
    def volver_atras(self):
        """Vuelve a la pantalla anterior en el historial"""
        if self.indice_historial > 0:
            entrada_anterior = self.historial[self.indice_historial - 1]
            return self.navegar_a(entrada_anterior['pantalla'], forzar=True)
        else:
            print("⚠️ No hay pantalla anterior en el historial")
            return False
    
    def ir_al_menu(self):
        """Método de conveniencia para ir al menú principal"""
        return self.navegar_a('menu')
    
    def ir_al_login(self):
        """Método de conveniencia para ir al login (logout)"""
        # Limpiar estado de usuario
        if hasattr(self.app, 'estado_app'):
            self.app.estado_app['usuario_actual'] = None
            self.app.estado_app['sesion_activa'] = False
        
        return self.navegar_a('login', forzar=True)
    
    # === MÉTODOS PRIVADOS ===
    
    def _ejecutar_validaciones(self, destino):
        """Ejecuta todas las validaciones para la navegación"""
        
        pantalla_actual = self.app.root.current
        ruta = f"{pantalla_actual}->{destino}"
        
        # Buscar configuración específica
        config = self.configuraciones_navegacion.get(ruta)
        if not config:
            # Buscar configuración con comodín
            config = self._buscar_configuracion_comodin(pantalla_actual, destino)
        
        if not config:
            print(f"ℹ️ Sin configuración específica para '{ruta}', usando validaciones por defecto")
            config = {'validaciones': ['pantalla_existe']}
        
        # Ejecutar validaciones
        for validacion in config.get('validaciones', []):
            if validacion in self.validadores:
                if not self.validadores[validacion](destino):
                    print(f"❌ Validación '{validacion}' falló para '{destino}'")
                    return False
            else:
                print(f"⚠️ Validador '{validacion}' no encontrado")
        
        return True
    
    def _buscar_configuracion_comodin(self, origen, destino):
        """Busca configuración usando comodines"""
        
        # Buscar origen->*
        config_origen = self.configuraciones_navegacion.get(f"{origen}->*")
        if config_origen:
            return config_origen
        
        # Buscar *->destino
        config_destino = self.configuraciones_navegacion.get(f"*->{destino}")
        if config_destino:
            return config_destino
        
        return None
    
    def _validar_usuario_autenticado(self, destino):
        """Valida que el usuario esté autenticado"""
        if hasattr(self.app, 'estado_app'):
            return self.app.estado_app.get('sesion_activa', False)
        
        # Fallback: verificar si existe archivo de sesión
        return os.path.exists('usuarios_registrados.json')
    
    def _validar_pantalla_existe(self, destino):
        """Valida que la pantalla destino exista"""
        try:
            self.app.root.get_screen(destino)
            return True
        except:
            print(f"❌ Pantalla '{destino}' no existe")
            return False
    
    def _validar_gestor_temas(self, destino):
        """Valida que el gestor de temas esté disponible"""
        return hasattr(self.app, 'gestor_temas') and self.app.gestor_temas is not None
    
    def _ejecutar_interceptores_pre(self, destino, datos):
        """Ejecuta interceptores antes de la navegación"""
        for interceptor in self.interceptores_pre:
            try:
                if not interceptor(self.app.root.current, destino, datos):
                    return False
            except Exception as e:
                print(f"❌ Error en interceptor pre-navegación: {e}")
                return False
        return True
    
    def _ejecutar_interceptores_post(self, destino, datos):
        """Ejecuta interceptores después de la navegación"""
        for interceptor in self.interceptores_post:
            try:
                interceptor(self.pantalla_anterior, destino, datos)
            except Exception as e:
                print(f"⚠️ Error en interceptor post-navegación: {e}")
    
    def _preparar_pantalla_destino(self, destino, datos):
        """Prepara la pantalla destino antes de mostrarla"""
        try:
            pantalla = self.app.root.get_screen(destino)
            
            # Actualizar idioma si la pantalla lo soporta
            if hasattr(pantalla, 'actualizar_idioma') and hasattr(self.app, 'idioma_actual'):
                pantalla.actualizar_idioma(self.app.idioma_actual)
            elif hasattr(pantalla, 'configurar_idioma') and hasattr(self.app, 'idioma_actual'):
                pantalla.configurar_idioma(self.app.idioma_actual)
            
            # Pasar datos si la pantalla lo soporta
            if datos and hasattr(pantalla, 'recibir_datos'):
                pantalla.recibir_datos(datos)
            
            # Configurar navegación si la pantalla lo necesita
            if hasattr(pantalla, 'configurar_navegacion'):
                pantalla.configurar_navegacion(self.navegar_a)
            
            # Configurar callback específicos
            self._configurar_callbacks_pantalla(pantalla, destino)
            
            print(f"✅ Pantalla '{destino}' preparada correctamente")
            
        except Exception as e:
            print(f"⚠️ Error preparando pantalla '{destino}': {e}")
    
    def _configurar_callbacks_pantalla(self, pantalla, nombre_pantalla):
        """Configura callbacks específicos según el tipo de pantalla"""
        
        if nombre_pantalla == 'send_resume':
            # Configurar callback para volver al menú
            if hasattr(pantalla, 'configurar_callback_menu'):
                pantalla.configurar_callback_menu(self.ir_al_menu)
        
        elif nombre_pantalla == 'menu':
            # Configurar navegación del menú
            if hasattr(pantalla, 'configurar_navegacion'):
                pantalla.configurar_navegacion(self._manejar_navegacion_menu)
        
        elif nombre_pantalla in ['schedule_reminder', 'mis_recordatorios']:
            # Configurar callback para volver al menú en recordatorios
            if hasattr(pantalla, 'configurar_callback_volver'):
                pantalla.configurar_callback_volver(self.ir_al_menu)
    
    def _manejar_navegacion_menu(self, destino):
        """Maneja la navegación específica desde el menú"""
        
        # Mapeo de destinos del menú a pantallas reales
        mapeo_pantallas = {
            'sugerencias': 'sugerencias',
            'buscar_temas': 'buscar_temas',
            'temas_profundos': 'temas_profundos', 
            'send_resume': 'send_resume',
            'schedule_reminder': 'schedule_reminder',
            'mis_recordatorios': 'mis_recordatorios'
        }
        
        pantalla_real = mapeo_pantallas.get(destino, destino)
        
        # Verificar disponibilidad
        if self._validar_pantalla_existe(pantalla_real):
            # Preparar datos de contexto
            datos_contexto = {
                'origen': 'menu',
                'usuario': getattr(self.app, 'usuario_actual', None),
                'idioma': getattr(self.app, 'idioma_actual', 'es')
            }
            
            return self.navegar_a(pantalla_real, datos_contexto)
        else:
            print(f"⚠️ Funcionalidad '{destino}' no está disponible")
            return False
    
    def _aplicar_transicion(self, destino, transicion_personalizada):
        """Aplica la transición configurada"""
        
        pantalla_actual = self.app.root.current
        ruta = f"{pantalla_actual}->{destino}"
        
        # Determinar configuración de transición
        config = transicion_personalizada
        if not config:
            config = self.configuraciones_navegacion.get(ruta, {})
            if not config:
                config = self._buscar_configuracion_comodin(pantalla_actual, destino) or {}
        
        # Aplicar configuración
        tipo_transicion = config.get('transicion', 'slide')
        direccion = config.get('direccion', 'left')
        duracion = config.get('duracion', 0.3)
        
        # Crear y configurar transición
        if tipo_transicion in self.transiciones_disponibles:
            transicion = self.transiciones_disponibles[tipo_transicion]()
            
            if hasattr(transicion, 'direction'):
                transicion.direction = direccion
            if hasattr(transicion, 'duration'):
                transicion.duration = duracion
            
            self.app.root.transition = transicion
            
            print(f"🎬 Transición aplicada: {tipo_transicion} ({direccion}, {duracion}s)")
        else:
            print(f"⚠️ Tipo de transición '{tipo_transicion}' no reconocido")
    
    def _actualizar_estado_navegacion(self, origen, destino):
        """Actualiza el estado interno después de la navegación"""
        
        self.pantalla_anterior = origen
        
        # Agregar al historial
        entrada_historial = {
            'pantalla': destino,
            'timestamp': time.time(),
            'origen': origen,
            'usuario': getattr(self.app, 'usuario_actual', None)
        }
        
        # Mantener historial limitado
        self.historial.append(entrada_historial)
        if len(self.historial) > 50:  # Límite de historial
            self.historial.pop(0)
        
        self.indice_historial = len(self.historial) - 1
        
        # Actualizar estado de la app si existe
        if hasattr(self.app, 'estado_app'):
            self.app.estado_app['pantalla_actual'] = destino
            self.app.estado_app['historial_navegacion'] = self.historial[-10:]  # Últimas 10
        
        print(f"📊 Estado actualizado: {origen} → {destino}")
    
    # === MÉTODOS PÚBLICOS DE CONFIGURACIÓN ===
    
    def agregar_validador(self, nombre, funcion_validador):
        """Agrega un validador personalizado"""
        self.validadores[nombre] = funcion_validador
        print(f"✅ Validador '{nombre}' agregado")
    
    def agregar_interceptor_pre(self, funcion_interceptor):
        """Agrega un interceptor que se ejecuta antes de navegar"""
        self.interceptores_pre.append(funcion_interceptor)
        print("✅ Interceptor pre-navegación agregado")
    
    def agregar_interceptor_post(self, funcion_interceptor):
        """Agrega un interceptor que se ejecuta después de navegar"""
        self.interceptores_post.append(funcion_interceptor)
        print("✅ Interceptor post-navegación agregado")
    
    def configurar_ruta(self, origen, destino, configuracion):
        """Configura una ruta específica de navegación"""
        ruta = f"{origen}->{destino}"
        self.configuraciones_navegacion[ruta] = configuracion
        print(f"✅ Ruta '{ruta}' configurada")
    
    def obtener_historial(self, limite=10):
        """Obtiene el historial de navegación"""
        return self.historial[-limite:] if limite else self.historial
    
    def limpiar_historial(self):
        """Limpia el historial de navegación"""
        self.historial.clear()
        self.indice_historial = -1
        print("🗑️ Historial de navegación limpiado")


# === INTEGRACIÓN CON TU CÓDIGO ACTUAL ===

def integrar_gestor_navegacion(app_instance):
    """
    Función de integración para agregar el gestor a tu aplicación existente
    sin romper el código actual.
    """
    
    print("🔧 === INTEGRANDO GESTOR DE NAVEGACIÓN ===")
    
    # Crear el gestor
    gestor = GestorNavegacion(app_instance)
    
    # Agregar a la aplicación
    app_instance.gestor_navegacion = gestor
    
    # Configurar interceptores útiles
    def interceptor_logging(origen, destino, datos):
        print(f"📊 Navegación registrada: {origen} → {destino}")
        return True
    
    def interceptor_guardar_estado(origen, destino, datos):
        """Interceptor para guardar estado antes de navegar"""
        try:
            pantalla_origen = app_instance.root.get_screen(origen)
            if hasattr(pantalla_origen, 'guardar_estado'):
                pantalla_origen.guardar_estado()
        except:
            pass
        return True
    
    gestor.agregar_interceptor_pre(interceptor_guardar_estado)
    gestor.agregar_interceptor_post(interceptor_logging)
    
    # Configurar validaciones específicas para tu app
    def validar_datos_interesado():
        """Validador para pantallas que requieren datos del interesado"""
        return hasattr(app_instance, 'gestor_temas') and app_instance.gestor_temas is not None
    
    gestor.agregar_validador('datos_interesado', validar_datos_interesado)
    
    # Configurar rutas específicas de tu aplicación
    gestor.configurar_ruta('send_resume', 'menu', {
        'transicion': 'slide',
        'direccion': 'right',
        'duracion': 0.3,
        'validaciones': ['usuario_autenticado']
    })
    
    print("✅ GestorNavegacion integrado exitosamente")
    return gestor


# === EJEMPLO DE USO CON TU CÓDIGO ===

"""
# En tu AsistentePredicacionApp.build():

def build(self):
    # ... tu código actual ...
    
    # Agregar esta línea después de crear el screen manager:
    self.gestor_navegacion = integrar_gestor_navegacion(self)
    
    # ... resto de tu código ...

# Reemplazar navegaciones directas:

# ANTES:
def callback_login_exitoso(self, usuario, idioma):
    self.root.current = 'send_resume'

# DESPUÉS:
def callback_login_exitoso(self, usuario, idioma):
    self.gestor_navegacion.navegar_a('send_resume', {
        'usuario': usuario,
        'idioma': idioma,
        'origen': 'login'
    })

# ANTES:
def manejar_navegacion(self, destino):
    self.root.current = destino

# DESPUÉS:
def manejar_navegacion(self, destino):
    return self.gestor_navegacion.navegar_a(destino)
"""
# gestor_navegacion_simple.py
"""
GestorNavegacion - Versión SIMPLE y SEGURA
Solo mejora tu código actual sin romper nada
"""

class GestorNavegacionSimple:
    """
    Versión simple del gestor que solo mejora tu código actual
    sin agregar complejidad que pueda causar errores.
    """
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.historial = []
        print("🧭 GestorNavegacion Simple inicializado")
    
    def navegar_a(self, destino, datos=None):
        """
        Navegación simple con validación básica
        """
        try:
            print(f"🧭 Navegando a: {destino}")
            
            # Validación básica: ¿existe la pantalla?
            try:
                self.app.root.get_screen(destino)
            except:
                print(f"❌ Pantalla '{destino}' no existe")
                return False
            
            # Guardar en historial
            self.historial.append({
                'de': self.app.root.current,
                'a': destino
            })
            
            # Navegación normal (como tu código actual)
            self.app.root.current = destino
            
            print(f"✅ Navegación a '{destino}' exitosa")
            return True
            
        except Exception as e:
            print(f"❌ Error navegando a '{destino}': {e}")
            return False
    
    def ir_al_menu(self):
        """Método de conveniencia para ir al menú"""
        return self.navegar_a('menu')
    
    def obtener_historial(self):
        """Obtiene el historial simple"""
        return self.historial[-10:]  # Últimas 10 navegaciones


# === INTEGRACIÓN ULTRA-SIMPLE ===

def agregar_gestor_simple(app_instance):
    """
    Agrega el gestor simple SIN romper tu código actual
    """
    try:
        # Solo crear el gestor, nada más
        gestor = GestorNavegacionSimple(app_instance)
        app_instance.gestor_navegacion = gestor
        print("✅ GestorNavegacion Simple agregado")
        return gestor
    except Exception as e:
        print(f"❌ Error agregando gestor: {e}")
        return None


# === PARA USAR EN TU CÓDIGO ===
"""
INTEGRACIÓN MUY SIMPLE:

1. En tu AsistentePredicacionApp.__init__():
   
   def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.idioma_actual = 'es'
       self.gestor_temas = None
       self.gestor_navegacion = None  # 🆕 Agregar esta línea

2. En tu build(), al final:

   def build(self):
       # ... todo tu código actual ...
       
       # 🆕 Agregar estas líneas AL FINAL:
       from gestor_navegacion_simple import agregar_gestor_simple
       self.gestor_navegacion = agregar_gestor_simple(self)
       
       return sm

3. OPCIONAL - Usar el gestor (puedes hacerlo gradualmente):

   # En lugar de:
   self.root.current = 'menu'
   
   # Puedes usar:
   if self.gestor_navegacion:
       self.gestor_navegacion.navegar_a('menu')
   else:
       self.root.current = 'menu'  # Fallback
"""