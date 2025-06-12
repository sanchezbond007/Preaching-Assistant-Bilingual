# ============================================
# ARCHIVO: pantalla_datos.py
# ============================================
# GUARDAR ESTE CÓDIGO EN UN ARCHIVO LLAMADO "pantalla_datos.py"

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock
import json
import datetime
import os

class PantallaDatos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'datos_interesado'
        self.construir_interfaz()
    
    def construir_interfaz(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Título
        titulo = Label(
            text='🎯 DATOS DEL INTERESADO',
            font_size=dp(26),
            size_hint_y=None,
            height=dp(60),
            color=(1, 1, 1, 1),
            bold=True
        )
        layout.add_widget(titulo)
        
        # Status
        self.status = Label(
            text='✅ Sistema listo - Completa los datos',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(40),
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status)
        
        # Campo Nombre
        layout.add_widget(Label(
            text='👤 Nombre:',
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        ))
        
        self.nombre_input = TextInput(
            hint_text='Ingresa el nombre...',
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            font_size=dp(16)
        )
        layout.add_widget(self.nombre_input)
        
        # Campo Teléfono
        layout.add_widget(Label(
            text='📞 Teléfono:',
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1),
            font_size=dp(16)
        ))
        
        self.telefono_input = TextInput(
            hint_text='Ingresa el teléfono...',
            size_hint_y=None,
            height=dp(50),
            multiline=False,
            font_size=dp(16)
        )
        layout.add_widget(self.telefono_input)
        
        # BOTONES - Layout horizontal
        botones_layout = BoxLayout(orientation='horizontal', spacing=dp(15), size_hint_y=None, height=dp(70))
        
        # Botón GUARDAR
        self.btn_guardar = Button(
            text='💾 GUARDAR',
            font_size=dp(18),
            background_color=(0.2, 0.8, 0.2, 1),  # Verde
            color=(1, 1, 1, 1)
        )
        self.btn_guardar.bind(on_press=self.guardar_datos)
        botones_layout.add_widget(self.btn_guardar)
        
        # Botón OMITIR
        self.btn_omitir = Button(
            text='⏭️ OMITIR',
            font_size=dp(18),
            background_color=(0.8, 0.5, 0.2, 1),  # Naranja
            color=(1, 1, 1, 1)
        )
        self.btn_omitir.bind(on_press=self.omitir_datos)
        botones_layout.add_widget(self.btn_omitir)
        
        layout.add_widget(botones_layout)
        
        # Botón TEST
        btn_test = Button(
            text='🧪 TEST FUNCIONAMIENTO',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.5, 0.2, 0.8, 1)
        )
        btn_test.bind(on_press=self.test_funcionamiento)
        layout.add_widget(btn_test)
        
        self.add_widget(layout)
    
    def guardar_datos(self, instance):
        """FUNCIÓN QUE SÍ FUNCIONA - Guarda los datos"""
        try:
            # Cambiar color para feedback
            instance.background_color = (0.8, 0.8, 0.2, 1)  # Amarillo
            
            # Obtener datos
            nombre = self.nombre_input.text.strip() or "Sin nombre"
            telefono = self.telefono_input.text.strip()
            
            # Crear registro
            datos = {
                'nombre': nombre,
                'telefono': telefono,
                'fecha': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Guardar archivo
            filename = f'interesado_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            # Feedback exitoso
            self.status.text = f'✅ GUARDADO: {nombre}'
            self.status.color = (0, 1, 0, 1)
            instance.background_color = (0, 1, 0, 1)  # Verde
            
            print(f"✅ DATOS GUARDADOS: {filename}")
            print(f"📄 Contenido: {datos}")
            
            # Navegar al menú después de 1 segundo
            Clock.schedule_once(lambda dt: self.navegar_menu(), 1.0)
            
        except Exception as e:
            self.status.text = f'❌ ERROR: {str(e)}'
            self.status.color = (1, 0, 0, 1)
            print(f"❌ Error al guardar: {e}")
    
    def omitir_datos(self, instance):
        """FUNCIÓN QUE SÍ FUNCIONA - Omite los datos"""
        try:
            instance.background_color = (0.5, 0.5, 0.5, 1)  # Gris
            self.status.text = '⏭️ DATOS OMITIDOS - Continuando...'
            self.status.color = (0.8, 0.8, 0.8, 1)
            
            print("⏭️ DATOS OMITIDOS por el usuario")
            
            # Navegar después de 0.5 segundos
            Clock.schedule_once(lambda dt: self.navegar_menu(), 0.5)
            
        except Exception as e:
            self.status.text = f'❌ ERROR: {str(e)}'
            self.status.color = (1, 0, 0, 1)
            print(f"❌ Error al omitir: {e}")
    
    def test_funcionamiento(self, instance):
        """FUNCIÓN DE TEST - Verifica que todo funcione"""
        try:
            instance.background_color = (0.2, 0.8, 0.8, 1)  # Cian
            
            # Info del sistema
            if self.manager:
                pantallas = [screen.name for screen in self.manager.screens]
                info = f"Pantallas: {pantallas}"
            else:
                info = "Sin ScreenManager"
            
            self.status.text = f'🧪 TEST OK! {info}'
            self.status.color = (0, 1, 1, 1)
            
            print("=== 🧪 TEST DE FUNCIONAMIENTO ===")
            print(f"📝 Nombre: '{self.nombre_input.text}'")
            print(f"📞 Teléfono: '{self.telefono_input.text}'")
            print(f"🖥️ ScreenManager: {self.manager}")
            print(f"📋 {info}")
            print("================================")
            
        except Exception as e:
            self.status.text = f'❌ TEST ERROR: {str(e)}'
            self.status.color = (1, 0, 0, 1)
            print(f"❌ Error en test: {e}")
    
    def navegar_menu(self):
        """FUNCIÓN DE NAVEGACIÓN - Va al menú principal"""
        try:
            if not self.manager:
                self.status.text = '❌ No hay ScreenManager'
                return
            
            # Pantallas posibles (en orden de prioridad)
            pantallas_objetivo = [
                'menu_principal',
                'menu_temporal',
                'menu',
                'main_menu'
            ]
            
            pantallas_disponibles = [screen.name for screen in self.manager.screens]
            
            # Intentar navegar
            for pantalla in pantallas_objetivo:
                if pantalla in pantallas_disponibles:
                    self.manager.current = pantalla
                    self.status.text = f'✅ Navegando a: {pantalla}'
                    self.status.color = (0, 1, 0, 1)
                    print(f"✅ Navegación exitosa a: {pantalla}")
                    return
            
            # Si no encuentra ninguna
            self.status.text = f'❓ Disponibles: {pantallas_disponibles}'
            self.status.color = (1, 1, 0, 1)
            print(f"❓ Pantallas disponibles: {pantallas_disponibles}")
            
        except Exception as e:
            self.status.text = f'❌ Error navegación: {str(e)}'
            self.status.color = (1, 0, 0, 1)
            print(f"❌ Error en navegación: {e}")