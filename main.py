import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Asegura acceso al directorio base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from pantallas.menu import PantallaMenu
from pantallas.sugerencias import PantallaSugerencias
from pantallas.temas_profundos import PantallaTemasProfundos
from pantallas.login import PantallaLogin
from pantallas.crear_usuario import PantallaCrearUsuario
from pantallas.aviso_legal import PantallaAvisoLegal

class AsistentePredicacionApp(App):
    def build(self):
        self.idioma = 'es'  # Idioma predeterminado
        self.sm = ScreenManager(transition=FadeTransition())

        # Pantalla Aviso Legal
        self.pantalla_aviso = PantallaAvisoLegal(
            name='aviso_legal',
            continuar_callback=self.ir_a_login
        )
        self.sm.add_widget(self.pantalla_aviso)

        # Pantalla Login
        self.pantalla_login = PantallaLogin(
            name='login',
            idioma_callback=self.cambiar_idioma,
            continuar_callback=self.ir_a_menu,
            crear_usuario_callback=self.ir_a_crear_usuario,
            actualizar_callback=self.buscar_actualizacion,
            login_callback=self.manejar_login_exitoso,  # ← NUEVO CALLBACK
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_login)

        # Pantalla Crear Usuario
        self.pantalla_crear_usuario = PantallaCrearUsuario(
            name='crear_usuario',
            volver_callback=self.ir_a_login,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_crear_usuario)

        # Pantalla Menú principal
        self.pantalla_menu = PantallaMenu(
            name='menu',
            sugerencias_callback=self.ir_a_sugerencias,
            profundos_callback=self.ir_a_profundos,
            buscar_callback=self.ir_a_busqueda,
            volver_callback=self.ir_a_login,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_menu)

        # Pantalla Sugerencias
        self.pantalla_sugerencias = PantallaSugerencias(
            name='sugerencias',
            volver_callback=self.ir_a_menu,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_sugerencias)

        # Pantalla Temas Profundos
        self.pantalla_profundos = PantallaTemasProfundos(
            name='temas_profundos',
            volver_callback=self.ir_a_menu,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_profundos)

        # Mostrar primero el aviso legal
        self.sm.current = 'aviso_legal'
        return self.sm

    def cambiar_idioma(self, nuevo_idioma):
        """Método mejorado para cambiar idioma en toda la aplicación"""
        print(f"🌍 === CAMBIO GLOBAL DE IDIOMA ===")
        print(f"🌍 De: '{self.idioma}' a '{nuevo_idioma}'")
        
        self.idioma = nuevo_idioma
        
        # Actualizar todas las pantallas
        self.pantalla_login.idioma = nuevo_idioma
        self.pantalla_crear_usuario.idioma = nuevo_idioma
        self.pantalla_menu.idioma = nuevo_idioma
        self.pantalla_sugerencias.idioma = nuevo_idioma
        self.pantalla_profundos.idioma = nuevo_idioma
        
        # Forzar actualización del menú si es la pantalla actual
        if self.sm.current == 'menu':
            print("🔄 Actualizando menú inmediatamente...")
            self.pantalla_menu.forzar_idioma(nuevo_idioma)
        
        print(f"🌍 === CAMBIO DE IDIOMA COMPLETADO ===")

    def manejar_login_exitoso(self, datos_login):
        """Maneja el login exitoso y navega al menú con idioma correcto"""
        print(f"✅ === LOGIN EXITOSO ===")
        print(f"✅ Usuario: {datos_login.get('usuario', 'N/A')}")
        print(f"✅ Idioma actual: '{self.idioma}'")
        
        # Asegurar que el menú tenga el idioma correcto ANTES de navegar
        print(f"🔧 Configurando idioma del menú: '{self.idioma}'")
        self.pantalla_menu.idioma = self.idioma
        self.pantalla_menu.forzar_idioma(self.idioma)
        
        # Navegar al menú
        print("🔄 Navegando al menú...")
        self.sm.current = 'menu'
        print(f"✅ === NAVEGACIÓN AL MENÚ COMPLETADA ===")

    def ir_a_login(self, *args):
        print("🔙 Navegando a login...")
        self.sm.current = 'login'

    def ir_a_crear_usuario(self, *args):
        print("👤 Navegando a crear usuario...")
        # Asegurar idioma correcto antes de navegar
        self.pantalla_crear_usuario.idioma = self.idioma
        self.sm.current = 'crear_usuario'

    def ir_a_menu(self, *args):
        print(f"🏠 Navegando a menú con idioma: '{self.idioma}'")
        # CRÍTICO: Actualizar idioma del menú antes de navegar
        self.pantalla_menu.idioma = self.idioma
        self.pantalla_menu.forzar_idioma(self.idioma)
        self.sm.current = 'menu'

    def ir_a_sugerencias(self, *args):
        print("📋 Navegando a sugerencias...")
        # Asegurar idioma correcto antes de navegar
        self.pantalla_sugerencias.idioma = self.idioma
        self.sm.current = 'sugerencias'

    def ir_a_profundos(self, *args):
        print("📚 Navegando a temas profundos...")
        # Asegurar idioma correcto antes de navegar
        self.pantalla_profundos.idioma = self.idioma
        self.sm.current = 'temas_profundos'

    def ir_a_busqueda(self, *args):
        print("🔍 Función de búsqueda aún no implementada.")
        # Aquí puedes agregar una pantalla real en el futuro:
        # self.pantalla_busqueda.idioma = self.idioma
        # self.sm.current = 'busqueda'

    def buscar_actualizacion(self, *args):
        print("🔄 Verificando actualizaciones...")

if __name__ == '__main__':
    AsistentePredicacionApp().run()