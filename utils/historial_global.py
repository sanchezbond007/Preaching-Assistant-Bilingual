utils/historial_global.py

Manejador de historial general de sesiones (estilo singleton)

from datetime import datetime

class HistorialSesion: _instance = None

def __new__(cls):
    if cls._instance is None:
        cls._instance = super(HistorialSesion, cls).__new__(cls)
        cls._instance.historial = []
        cls._instance.sesion_actual = None
        cls._instance.datos_interesado = None
    return cls._instance

def iniciar_nueva_sesion(self, datos_interesado):
    self.datos_interesado = datos_interesado
    self.sesion_actual = {
        'inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'interesado': datos_interesado,
        'consultas': []
    }

def obtener_datos_interesado(self):
    return self.datos_interesado if self.datos_interesado else {}

def agregar_consulta(self, fuente, titulo, contenido, idioma='es'):
    if self.sesion_actual is None:
        self.iniciar_sesion_temporal()
    consulta = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'fuente': fuente,
        'titulo': titulo,
        'contenido': contenido,
        'idioma': idioma
    }
    self.sesion_actual['consultas'].append(consulta)

def iniciar_sesion_temporal(self):
    datos_temporales = {
        'nombre': 'Sesión Temporal',
        'telefono': '',
        'email': '',
        'testigo': 'Usuario',
        'fecha_inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'idioma': 'es'
    }
    self.iniciar_nueva_sesion(datos_temporales)

def obtener_historial_sesion(self):
    if self.sesion_actual is None:
        return {
            'inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'interesado': {},
            'consultas': []
        }
    return self.sesion_actual

def limpiar_sesion(self):
    if self.sesion_actual:
        datos_interesado = self.sesion_actual['interesado']
        self.sesion_actual = {
            'inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'interesado': datos_interesado,
            'consultas': []
        }

def tiene_sesion_activa(self):
    return self.sesion_actual is not None

def contar_consultas(self):
    if self.sesion_actual:
        return len(self.sesion_actual['consultas'])
    return 0

def get_info_for_sharing(self):
    if not self.datos_interesado:
        return {
            'destinatario': '',
            'telefono': '',
            'email': '',
            'testigo': ''
        }
    return {
        'destinatario': self.datos_interesado.get('nombre', ''),
        'telefono': self.datos_interesado.get('telefono', ''),
        'email': self.datos_interesado.get('email', ''),
        'testigo': self.datos_interesado.get('testigo', '')
    }

