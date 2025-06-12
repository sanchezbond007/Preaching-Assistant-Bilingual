"""
gestores/gestor_usuarios.py
Gestor Modular de Usuarios - Manejo de autenticación y credenciales
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, Tuple, Optional, List

class GestorUsuarios:
    def __init__(self, archivo_usuarios='usuarios_registrados.json'):
        """
        Inicializa el gestor de usuarios
        
        Args:
            archivo_usuarios (str): Ruta al archivo de usuarios
        """
        self.archivo_usuarios = archivo_usuarios
        self.usuarios_cache = {}
        self.sesion_actual = None
        self.cargar_usuarios()
        print("✅ GestorUsuarios inicializado")
    
    def cargar_usuarios(self) -> bool:
        """
        Carga los usuarios desde el archivo JSON
        
        Returns:
            bool: True si se cargó correctamente, False si hubo error
        """
        try:
            if os.path.exists(self.archivo_usuarios):
                with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.usuarios_cache = data.get('usuarios', {})
                    print(f"✅ {len(self.usuarios_cache)} usuarios cargados")
                    return True
            else:
                # Crear archivo con usuarios por defecto
                self.crear_archivo_usuarios_inicial()
                return True
        except Exception as e:
            print(f"❌ Error cargando usuarios: {e}")
            return False
    
    def crear_archivo_usuarios_inicial(self):
        """Crea el archivo inicial de usuarios con datos por defecto"""
        usuarios_inicial = {
            'usuarios': {
                'admin': 'admin123',
                'test': 'test123',
                'sanchezbond007': '************'
            },
            'credenciales_guardadas': {},
            'configuracion': {
                'permitir_recordar_credenciales': True,
                'tiempo_sesion_minutos': 60,
                'intentos_login_max': 3
            },
            'historial_login': [],
            'usuarios_bloqueados': {},
            'metadata': {
                'version': '1.0',
                'fecha_creacion': datetime.now().isoformat(),
                'ultima_actualizacion': datetime.now().isoformat()
            }
        }
        
        try:
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios_inicial, f, indent=2, ensure_ascii=False)
            
            self.usuarios_cache = usuarios_inicial['usuarios']
            print("✅ Archivo de usuarios inicial creado")
        except Exception as e:
            print(f"❌ Error creando archivo inicial: {e}")
    
    def validar_credenciales(self, usuario: str, contrasena: str) -> Tuple[bool, str]:
        """
        Valida las credenciales de un usuario
        
        Args:
            usuario (str): Nombre de usuario
            contrasena (str): Contraseña
            
        Returns:
            Tuple[bool, str]: (es_valido, mensaje)
        """
        try:
            # Verificar si el usuario está bloqueado
            if self.usuario_bloqueado(usuario):
                return False, "Usuario bloqueado temporalmente"
            
            # Verificar credenciales
            if usuario in self.usuarios_cache:
                if self.usuarios_cache[usuario] == contrasena:
                    # Login exitoso
                    self.registrar_login_exitoso(usuario)
                    self.sesion_actual = {
                        'usuario': usuario,
                        'timestamp': datetime.now().isoformat(),
                        'activo': True
                    }
                    return True, f"Login exitoso para {usuario}"
                else:
                    # Contraseña incorrecta
                    self.registrar_intento_fallido(usuario)
                    return False, "Contraseña incorrecta"
            else:
                # Usuario no existe
                self.registrar_intento_fallido(usuario)
                return False, "Usuario no encontrado"
                
        except Exception as e:
            print(f"❌ Error validando credenciales: {e}")
            return False, "Error interno de validación"
    
    def usuario_bloqueado(self, usuario: str) -> bool:
        """
        Verifica si un usuario está bloqueado
        
        Args:
            usuario (str): Nombre de usuario
            
        Returns:
            bool: True si está bloqueado
        """
        try:
            # Cargar datos actuales
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            usuarios_bloqueados = data.get('usuarios_bloqueados', {})
            
            if usuario in usuarios_bloqueados:
                tiempo_bloqueo = datetime.fromisoformat(usuarios_bloqueados[usuario])
                # Bloqueo por 15 minutos
                tiempo_actual = datetime.now()
                if (tiempo_actual - tiempo_bloqueo).total_seconds() > 900:  # 15 minutos
                    # Desbloquear usuario
                    del usuarios_bloqueados[usuario]
                    self.guardar_datos({'usuarios_bloqueados': usuarios_bloqueados})
                    return False
                else:
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error verificando bloqueo: {e}")
            return False
    
    def registrar_login_exitoso(self, usuario: str):
        """Registra un login exitoso en el historial"""
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            historial = data.get('historial_login', [])
            historial.append({
                'usuario': usuario,
                'timestamp': datetime.now().isoformat(),
                'exitoso': True,
                'ip': 'local'  # En una app móvil no hay IP
            })
            
            # Mantener solo los últimos 50 registros
            if len(historial) > 50:
                historial = historial[-50:]
            
            # Resetear intentos fallidos si existen
            intentos_fallidos = data.get('intentos_fallidos', {})
            if usuario in intentos_fallidos:
                del intentos_fallidos[usuario]
            
            self.guardar_datos({
                'historial_login': historial,
                'intentos_fallidos': intentos_fallidos
            })
            
        except Exception as e:
            print(f"❌ Error registrando login exitoso: {e}")
    
    def registrar_intento_fallido(self, usuario: str):
        """Registra un intento de login fallido"""
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            intentos_fallidos = data.get('intentos_fallidos', {})
            usuarios_bloqueados = data.get('usuarios_bloqueados', {})
            
            # Incrementar contador de intentos fallidos
            if usuario in intentos_fallidos:
                intentos_fallidos[usuario] += 1
            else:
                intentos_fallidos[usuario] = 1
            
            # Bloquear usuario si supera 3 intentos
            if intentos_fallidos[usuario] >= 3:
                usuarios_bloqueados[usuario] = datetime.now().isoformat()
                print(f"🔒 Usuario {usuario} bloqueado por intentos fallidos")
            
            # Registrar en historial
            historial = data.get('historial_login', [])
            historial.append({
                'usuario': usuario,
                'timestamp': datetime.now().isoformat(),
                'exitoso': False,
                'ip': 'local'
            })
            
            self.guardar_datos({
                'intentos_fallidos': intentos_fallidos,
                'usuarios_bloqueados': usuarios_bloqueados,
                'historial_login': historial
            })
            
        except Exception as e:
            print(f"❌ Error registrando intento fallido: {e}")
    
    def guardar_credenciales(self, usuario: str, contrasena: str, recordar: bool = False):
        """
        Guarda las credenciales para recordar en futuras sesiones
        
        Args:
            usuario (str): Nombre de usuario
            contrasena (str): Contraseña
            recordar (bool): Si debe recordar las credenciales
        """
        try:
            credenciales_guardadas = {}
            
            if recordar:
                credenciales_guardadas = {
                    'usuario': usuario,
                    'contrasena': contrasena,  # En producción, esto debería estar encriptado
                    'recordar': True,
                    'fecha_guardado': datetime.now().isoformat()
                }
                print(f"💾 Credenciales guardadas para: {usuario}")
            
            self.guardar_datos({'credenciales_guardadas': credenciales_guardadas})
            
        except Exception as e:
            print(f"❌ Error guardando credenciales: {e}")
    
    def cargar_credenciales_guardadas(self) -> Optional[Dict]:
        """
        Carga las credenciales guardadas
        
        Returns:
            Optional[Dict]: Credenciales guardadas o None
        """
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            credenciales = data.get('credenciales_guardadas', {})
            
            if credenciales and credenciales.get('recordar', False):
                print(f"✅ Credenciales cargadas para: {credenciales.get('usuario', '')}")
                return credenciales
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error cargando credenciales guardadas: {e}")
            return None
    
    def crear_usuario(self, usuario: str, contrasena: str, es_admin: bool = False) -> Tuple[bool, str]:
        """
        Crea un nuevo usuario
        
        Args:
            usuario (str): Nombre de usuario
            contrasena (str): Contraseña
            es_admin (bool): Si el usuario es administrador
            
        Returns:
            Tuple[bool, str]: (exitoso, mensaje)
        """
        try:
            # Verificar si el usuario ya existe
            if usuario in self.usuarios_cache:
                return False, "El usuario ya existe"
            
            # Validar datos
            if len(usuario) < 3:
                return False, "El usuario debe tener al menos 3 caracteres"
            
            if len(contrasena) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"
            
            # Agregar usuario
            self.usuarios_cache[usuario] = contrasena
            
            # Guardar en archivo
            self.guardar_datos({'usuarios': self.usuarios_cache})
            
            # Registrar creación
            self.registrar_evento_usuario(usuario, 'usuario_creado', {'es_admin': es_admin})
            
            print(f"👤 Usuario {usuario} creado exitosamente")
            return True, f"Usuario {usuario} creado correctamente"
            
        except Exception as e:
            print(f"❌ Error creando usuario: {e}")
            return False, "Error interno al crear usuario"
    
    def cambiar_contrasena(self, usuario: str, contrasena_actual: str, contrasena_nueva: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña de un usuario
        
        Args:
            usuario (str): Nombre de usuario
            contrasena_actual (str): Contraseña actual
            contrasena_nueva (str): Nueva contraseña
            
        Returns:
            Tuple[bool, str]: (exitoso, mensaje)
        """
        try:
            # Verificar credenciales actuales
            es_valido, _ = self.validar_credenciales(usuario, contrasena_actual)
            if not es_valido:
                return False, "Contraseña actual incorrecta"
            
            # Validar nueva contraseña
            if len(contrasena_nueva) < 6:
                return False, "La nueva contraseña debe tener al menos 6 caracteres"
            
            # Actualizar contraseña
            self.usuarios_cache[usuario] = contrasena_nueva
            self.guardar_datos({'usuarios': self.usuarios_cache})
            
            # Registrar cambio
            self.registrar_evento_usuario(usuario, 'contrasena_cambiada')
            
            return True, "Contraseña cambiada exitosamente"
            
        except Exception as e:
            print(f"❌ Error cambiando contraseña: {e}")
            return False, "Error interno al cambiar contraseña"
    
    def listar_usuarios(self) -> List[str]:
        """
        Lista todos los usuarios registrados
        
        Returns:
            List[str]: Lista de nombres de usuario
        """
        return list(self.usuarios_cache.keys())
    
    def obtener_estadisticas_usuarios(self) -> Dict:
        """
        Obtiene estadísticas de usuarios
        
        Returns:
            Dict: Estadísticas de usuarios
        """
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            historial = data.get('historial_login', [])
            usuarios_bloqueados = data.get('usuarios_bloqueados', {})
            
            # Contar logins exitosos por usuario
            logins_por_usuario = {}
            for entrada in historial:
                if entrada.get('exitoso', False):
                    usuario = entrada['usuario']
                    logins_por_usuario[usuario] = logins_por_usuario.get(usuario, 0) + 1
            
            estadisticas = {
                'total_usuarios': len(self.usuarios_cache),
                'usuarios_activos': len([u for u in self.usuarios_cache.keys() if u not in usuarios_bloqueados]),
                'usuarios_bloqueados': len(usuarios_bloqueados),
                'total_logins': len([h for h in historial if h.get('exitoso', False)]),
                'logins_por_usuario': logins_por_usuario,
                'ultimo_login': historial[-1] if historial else None
            }
            
            return estadisticas
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def registrar_evento_usuario(self, usuario: str, evento: str, datos_extra: Dict = None):
        """Registra un evento del usuario en el historial"""
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            eventos = data.get('eventos_usuario', [])
            
            evento_data = {
                'usuario': usuario,
                'evento': evento,
                'timestamp': datetime.now().isoformat(),
                'datos_extra': datos_extra or {}
            }
            
            eventos.append(evento_data)
            
            # Mantener solo los últimos 100 eventos
            if len(eventos) > 100:
                eventos = eventos[-100:]
            
            self.guardar_datos({'eventos_usuario': eventos})
            
        except Exception as e:
            print(f"❌ Error registrando evento: {e}")
    
    def guardar_datos(self, datos_actualizados: Dict):
        """
        Actualiza datos específicos en el archivo de usuarios
        
        Args:
            datos_actualizados (Dict): Datos a actualizar
        """
        try:
            # Cargar datos actuales
            data = {}
            if os.path.exists(self.archivo_usuarios):
                with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # Actualizar datos
            for clave, valor in datos_actualizados.items():
                data[clave] = valor
            
            # Actualizar timestamp
            if 'metadata' not in data:
                data['metadata'] = {}
            data['metadata']['ultima_actualizacion'] = datetime.now().isoformat()
            
            # Guardar
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        if self.sesion_actual:
            usuario = self.sesion_actual['usuario']
            self.registrar_evento_usuario(usuario, 'sesion_cerrada')
            self.sesion_actual = None
            print(f"👋 Sesión cerrada para: {usuario}")
    
    def obtener_sesion_actual(self) -> Optional[Dict]:
        """
        Obtiene información de la sesión actual
        
        Returns:
            Optional[Dict]: Información de sesión o None
        """
        return self.sesion_actual
    
    def usuario_logueado(self) -> bool:
        """
        Verifica si hay un usuario logueado
        
        Returns:
            bool: True si hay sesión activa
        """
        return self.sesion_actual is not None and self.sesion_actual.get('activo', False)

# Función de utilidad para testing
def test_gestor_usuarios():
    """Función de prueba para el gestor de usuarios"""
    print("🧪 === TESTING GESTOR USUARIOS ===")
    
    gestor = GestorUsuarios('test_usuarios.json')
    
    # Test 1: Login válido
    resultado, mensaje = gestor.validar_credenciales('admin', 'admin123')
    print(f"Test 1 - Login válido: {resultado} - {mensaje}")
    
    # Test 2: Login inválido
    resultado, mensaje = gestor.validar_credenciales('admin', 'wrongpass')
    print(f"Test 2 - Login inválido: {resultado} - {mensaje}")
    
    # Test 3: Crear usuario
    resultado, mensaje = gestor.crear_usuario('testuser', 'testpass123')
    print(f"Test 3 - Crear usuario: {resultado} - {mensaje}")
    
    # Test 4: Estadísticas
    stats = gestor.obtener_estadisticas_usuarios()
    print(f"Test 4 - Estadísticas: {stats}")
    
    # Limpiar archivo de test
    if os.path.exists('test_usuarios.json'):
        os.remove('test_usuarios.json')
    
    print("✅ Testing completado")

if __name__ == '__main__':
    # Ejecutar tests si se ejecuta directamente
    test_gestor_usuarios()