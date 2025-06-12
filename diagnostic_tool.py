from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.logger import Logger
from kivy.clock import Clock

class DiagnosticWidget(Button):
    """Widget de diagnóstico que reporta TODO"""
    
    def __init__(self, test_name, **kwargs):
        super().__init__(**kwargs)
        self.test_name = test_name
        
    def on_touch_down(self, touch):
        Logger.info(f"DIAGNOSTIC: {self.test_name} - Touch DOWN en {touch.pos}")
        Logger.info(f"DIAGNOSTIC: Widget pos: {self.pos}, size: {self.size}")
        Logger.info(f"DIAGNOSTIC: Collide point: {self.collide_point(*touch.pos)}")
        
        if self.collide_point(*touch.pos):
            Logger.info(f"DIAGNOSTIC: {self.test_name} - TOUCH DETECTADO")
        else:
            Logger.info(f"DIAGNOSTIC: {self.test_name} - Touch FUERA del widget")
            
        return super().on_touch_down(touch)
    
    def on_press(self):
        Logger.info(f"DIAGNOSTIC: {self.test_name} - ON_PRESS EJECUTADO!")
        super().on_press()

class DiagnosticScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'diagnostic'
        
        layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Título
        title = Label(
            text="🔍 HERRAMIENTA DE DIAGNÓSTICO",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)
        
        # Info de Kivy
        import kivy
        version_label = Label(
            text=f"Kivy version: {kivy.__version__}",
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(version_label)
        
        # Label de resultados
        self.result_label = Label(
            text="Presiona cualquier botón para probar...",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(100),
            text_size=(None, None),
            halign='center'
        )
        layout.add_widget(self.result_label)
        
        # Test 1: Botón normal
        btn1 = DiagnosticWidget(
            test_name="NORMAL",
            text="TEST 1: Botón Normal",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60)
        )
        btn1.bind(on_press=lambda x: self.report_success("Botón Normal"))
        layout.add_widget(btn1)
        
        # Test 2: Botón con background transparent
        btn2 = DiagnosticWidget(
            test_name="TRANSPARENT",
            text="TEST 2: Background Transparent",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60),
            background_color=(0, 0, 0, 0)
        )
        btn2.bind(on_press=lambda x: self.report_success("Background Transparent"))
        layout.add_widget(btn2)
        
        # Test 3: Botón con canvas graphics
        btn3 = DiagnosticWidget(
            test_name="CUSTOM_GRAPHICS",
            text="TEST 3: Con Canvas Graphics",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60),
            background_color=(0, 0, 0, 0)
        )
        
        from kivy.graphics import Color, RoundedRectangle
        with btn3.canvas.before:
            Color(1, 0.3, 0.3, 1)  # Rojo
            self.btn3_bg = RoundedRectangle(
                pos=btn3.pos,
                size=btn3.size,
                radius=[dp(10)]
            )
            btn3.bind(size=self.update_btn3_bg, pos=self.update_btn3_bg)
        
        btn3.bind(on_press=lambda x: self.report_success("Canvas Graphics"))
        layout.add_widget(btn3)
        
        # Test 4: Touch directo
        touch_test = Button(
            text="TEST 4: Detectar Touch Directo",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60)
        )
        touch_test.bind(on_touch_down=self.direct_touch_test)
        layout.add_widget(touch_test)
        
        # Test programático
        program_test = Button(
            text="TEST 5: Trigger Programático",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60)
        )
        program_test.bind(on_press=lambda x: self.programmatic_test())
        layout.add_widget(program_test)
        
        self.add_widget(layout)
        
        # Auto-test después de 2 segundos
        Clock.schedule_once(self.auto_test, 2)
    
    def update_btn3_bg(self, instance, value):
        self.btn3_bg.pos = instance.pos
        self.btn3_bg.size = instance.size
    
    def report_success(self, test_name):
        message = f"✅ {test_name}: FUNCIONA CORRECTAMENTE!"
        Logger.info(f"DIAGNOSTIC: {message}")
        self.result_label.text = message
        print(message)  # También en consola normal
    
    def direct_touch_test(self, instance, touch):
        if instance.collide_point(*touch.pos):
            message = f"✅ TOUCH DIRECTO: Detectado en {touch.pos}"
            Logger.info(f"DIAGNOSTIC: {message}")
            self.result_label.text = message
            print(message)
            return True
        return False
    
    def programmatic_test(self):
        message = "✅ PROGRAMÁTICO: Trigger funciona!"
        Logger.info(f"DIAGNOSTIC: {message}")
        self.result_label.text = message
        print(message)
    
    def auto_test(self, dt):
        Logger.info("DIAGNOSTIC: Auto-test iniciado")
        print("🤖 AUTO-TEST: Verificando configuración...")
        
        # Verificar que los widgets están correctamente añadidos
        widget_count = len(self.children[0].children)  # BoxLayout children
        Logger.info(f"DIAGNOSTIC: {widget_count} widgets en layout")
        print(f"📊 Widgets detectados: {widget_count}")

class DiagnosticApp(App):
    def build(self):
        # Habilitar logging detallado
        Logger.setLevel('DEBUG')
        
        sm = ScreenManager()
        sm.add_widget(DiagnosticScreen())
        return sm

if __name__ == "__main__":
    print("🔍 INICIANDO DIAGNÓSTICO COMPLETO...")
    print("📋 Instrucciones:")
    print("   1. Presiona cada botón TEST")
    print("   2. Observa los mensajes en consola")
    print("   3. Reporta cuáles funcionan y cuáles no")
    print("=" * 50)
    
    DiagnosticApp().run()