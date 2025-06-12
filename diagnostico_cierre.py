#!/usr/bin/env python3
"""
Diagnóstico para identificar por qué la app se cierra
"""

print("🔍 === DIAGNÓSTICO DE CIERRE DE APP ===")

try:
    print("1. Verificando imports de Kivy...")
    from kivy.app import App
    print("   ✅ App importado")
    
    from kivy.uix.label import Label
    print("   ✅ Label importado")
    
    from kivy.uix.button import Button
    print("   ✅ Button importado")
    
    print("2. Verificando configuración de Kivy...")
    from kivy.config import Config
    print("   ✅ Config importado")
    
    print("3. Creando app de prueba mínima...")
    
    class TestApp(App):
        def build(self):
            print("   🔧 Construyendo interfaz...")
            return Label(text='¡App funcionando!\nSi ves esto, Kivy está bien')
    
    print("4. Intentando ejecutar app...")
    app = TestApp()
    
    print("5. Llamando app.run()...")
    app.run()
    
    print("6. ✅ App se ejecutó sin problemas")

except Exception as e:
    print(f"❌ ERROR DETECTADO: {type(e).__name__}: {e}")
    print("\n📋 DETALLES DEL ERROR:")
    import traceback
    traceback.print_exc()
    
    print("\n🔧 POSIBLES SOLUCIONES:")
    if "No module named" in str(e):
        print("- Instalar Kivy: pip install kivy")
    elif "Window" in str(e):
        print("- Problema de ventana: revisar configuración de display")
    elif "SDL" in str(e):
        print("- Problema SDL: ejecutar en entorno compatible")
    else:
        print("- Error inesperado: revisar logs completos")

print("\n📊 DIAGNÓSTICO COMPLETADO")