#!/usr/bin/env python3
"""
Diagnóstico automático sin pausas interactivas
"""

import sys
import os
import importlib
import traceback
import time

def separador(titulo):
    """Crear separador visual"""
    print("\n" + "="*60)
    print(f"  {titulo}")
    print("="*60)

def paso(numero, titulo):
    """Mostrar paso del diagnóstico"""
    print(f"\n📋 PASO {numero}: {titulo}")
    print("-" * 40)

def diagnosticar_automatico():
    separador("DIAGNÓSTICO AUTOMÁTICO - ASISTENTE PREDICACIÓN")
    
    # PASO 1: Estructura de archivos
    paso(1, "VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    
    archivos_necesarios = [
        'main.py',
        'pantallas/__init__.py',
        'pantallas/menu.py'
    ]
    
    estructura_ok = True
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo)
            print(f"✅ {archivo:<25} ({tamaño:>6} bytes)")
        else:
            print(f"❌ {archivo:<25} NO EXISTE")
            estructura_ok = False
    
    print(f"\n📊 Resultado Paso 1: {'CORRECTA' if estructura_ok else 'PROBLEMAS DETECTADOS'}")
    
    # PASO 2: Contenido __init__.py
    paso(2, "ANALIZANDO pantallas/__init__.py")
    
    try:
        with open('pantallas/__init__.py', 'rb') as f:
            contenido_bytes = f.read()
        
        with open('pantallas/__init__.py', 'r', encoding='utf-8') as f:
            contenido_texto = f.read()
        
        print(f"📏 Tamaño: {len(contenido_bytes)} bytes")
        print(f"📝 Contenido: '{contenido_texto.strip()}'")
        
        # Verificar BOM
        if contenido_bytes.startswith(b'\xef\xbb\xbf'):
            print("⚠️ PROBLEMA: Archivo tiene BOM UTF-8 (puede causar problemas)")
            init_ok = False
        else:
            print("✅ Sin BOM - Encoding correcto")
            init_ok = True
            
    except Exception as e:
        print(f"❌ Error leyendo __init__.py: {e}")
        init_ok = False
    
    print(f"\n📊 Resultado Paso 2: {'CORRECTO' if init_ok else 'PROBLEMAS DETECTADOS'}")
    
    # PASO 3: Python Path
    paso(3, "VERIFICANDO PYTHON PATH")
    
    directorio_actual = os.getcwd()
    print(f"📂 Directorio actual: {directorio_actual}")
    
    if directorio_actual in sys.path:
        print("✅ Directorio actual está en sys.path")
        path_ok = True
    else:
        print("⚠️ Directorio actual NO está en sys.path")
        print("🔧 Agregando directorio actual...")
        sys.path.insert(0, directorio_actual)
        print("✅ Directorio agregado a sys.path")
        path_ok = True
    
    print(f"\n📊 Resultado Paso 3: {'CORRECTO' if path_ok else 'PROBLEMAS'}")
    
    # PASO 4: Limpiar caché
    paso(4, "LIMPIANDO CACHÉ DE MÓDULOS")
    
    modulos_pantallas = [name for name in sys.modules if 'pantallas' in name]
    if modulos_pantallas:
        print("🗑️ Módulos 'pantallas' encontrados en caché:")
        for modulo in modulos_pantallas:
            print(f"   - {modulo}")
            del sys.modules[modulo]
        print("✅ Módulos removidos del caché")
    else:
        print("✅ No hay módulos 'pantallas' en caché")
    
    importlib.invalidate_caches()
    print("✅ Caché de importación invalidado")
    
    print(f"\n📊 Resultado Paso 4: COMPLETADO")
    
    # PASO 5: IMPORTACIÓN CRÍTICA
    paso(5, "PRUEBA DE IMPORTACIÓN DETALLADA")
    
    try:
        print("🔄 Intento 1: Importando módulo 'pantallas'...")
        import pantallas
        print(f"✅ 'pantallas' importado exitosamente")
        print(f"   📁 Ubicación: {getattr(pantallas, '__file__', 'No disponible')}")
        
        print("\n🔄 Intento 2: Importando 'pantallas.menu'...")
        import pantallas.menu as menu_module
        print(f"✅ 'pantallas.menu' importado exitosamente")
        print(f"   📁 Ubicación: {getattr(menu_module, '__file__', 'No disponible')}")
        
        print("\n🔄 Intento 3: Verificando clase 'PantallaMenu'...")
        if hasattr(menu_module, 'PantallaMenu'):
            PantallaMenu = menu_module.PantallaMenu
            print(f"✅ PantallaMenu encontrada: {PantallaMenu}")
            print(f"   🏷️ Tipo: {type(PantallaMenu)}")
            
            # Verificar herencia
            from kivy.uix.screenmanager import Screen
            if issubclass(PantallaMenu, Screen):
                print("✅ PantallaMenu hereda correctamente de Screen")
                
                print("\n🔄 Intento 4: Creando instancia de prueba...")
                try:
                    # Crear instancia con parámetros mínimos
                    instancia = PantallaMenu(name='test_diagnostico')
                    print("✅ Instancia creada exitosamente")
                    print(f"   🏷️ Tipo de instancia: {type(instancia)}")
                    print(f"   📛 Nombre asignado: {instancia.name}")
                    
                    # Verificar que tiene widgets
                    print(f"   🧩 Widgets hijos: {len(instancia.children)}")
                    
                    separador("🎉 DIAGNÓSTICO: ¡TODO FUNCIONA PERFECTAMENTE!")
                    print("\n✅ Tu menu.py se importa correctamente")
                    print("✅ PantallaMenu se puede instanciar sin problemas")
                    print("✅ El problema DEBE ESTAR en main.py")
                    print("\n🔧 SOLUCIÓN: El problema está en cómo main.py usa tu menú")
                    print("🔧 Ejecuta: python main_corregido.py para ver la solución")
                    
                    return True, "IMPORTACIÓN PERFECTA"
                    
                except Exception as e:
                    print(f"❌ Error creando instancia: {type(e).__name__}: {e}")
                    print("\n📋 Detalles del error:")
                    traceback.print_exc()
                    return False, f"ERROR EN INSTANCIACIÓN: {e}"
                    
            else:
                error_msg = "PantallaMenu NO hereda de Screen"
                print(f"❌ {error_msg}")
                return False, error_msg
        else:
            print("❌ PantallaMenu NO encontrada en pantallas.menu")
            attrs = [attr for attr in dir(menu_module) if not attr.startswith('_')]
            print(f"   📋 Atributos disponibles: {attrs}")
            return False, "PANTALLA_MENU NO ENCONTRADA"
    
    except ImportError as e:
        error_msg = f"ImportError: {e}"
        print(f"❌ {error_msg}")
        print("\n📋 Traceback completo:")
        traceback.print_exc()
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Error inesperado: {type(e).__name__}: {e}"
        print(f"❌ {error_msg}")
        print("\n📋 Traceback completo:")
        traceback.print_exc()
        return False, error_msg

def mostrar_solucion_especifica(exito, error_msg):
    """Mostrar solución específica basada en el resultado"""
    separador("🔧 SOLUCIONES RECOMENDADAS")
    
    if exito:
        print("""
🎯 TU MENU.PY FUNCIONA PERFECTAMENTE

El problema está en main.py. Aquí está la solución:

1. EJECUTA ESTE COMANDO:
   python main_corregido.py

2. SI QUIERES ARREGLAR TU main.py ORIGINAL:
   - Busca la línea: from pantallas.menu import PantallaMenu
   - Asegúrate de que los callbacks se pasen correctamente
   - Verifica que no haya try/except que oculte errores

3. USA ESTA IMPORTACIÓN ROBUSTA EN main.py:
   
   try:
       from pantallas.menu import PantallaMenu
       print("✅ PantallaMenu importada correctamente")
   except Exception as e:
       print(f"❌ Error importando: {e}")
       raise
""")
    else:
        print(f"""
❌ PROBLEMA DETECTADO: {error_msg}

🔧 SOLUCIONES:

1. EJECUTA REPARACIÓN AUTOMÁTICA:
   python arreglar_importacion.py

2. VERIFICACIÓN MANUAL:
   - Abre pantallas/menu.py
   - Busca: class PantallaMenu(Screen):
   - Verifica: def __init__(self, **kwargs):
   - Confirma: super().__init__(**kwargs)

3. SI PERSISTE EL PROBLEMA:
   python test_simple.py
""")

def main():
    # Verificar directorio
    if not os.path.exists('main.py'):
        separador("❌ ERROR: DIRECTORIO INCORRECTO")
        print("No se encuentra main.py en este directorio")
        print(f"Directorio actual: {os.getcwd()}")
        print("Ejecuta este script desde el directorio del proyecto")
        return
    
    try:
        print("🚀 Iniciando diagnóstico automático...")
        time.sleep(1)  # Pequeña pausa para ver el inicio
        
        exito, mensaje = diagnosticar_automatico()
        
        mostrar_solucion_especifica(exito, mensaje)
        
        separador("📊 RESUMEN FINAL")
        if exito:
            print("🎉 DIAGNÓSTICO: EXITOSO")
            print("🎯 ACCIÓN: Ejecuta 'python main_corregido.py'")
        else:
            print("⚠️ DIAGNÓSTICO: PROBLEMAS DETECTADOS")
            print("🎯 ACCIÓN: Ejecuta 'python arreglar_importacion.py'")
        
    except Exception as e:
        separador("💥 ERROR EN DIAGNÓSTICO")
        print(f"Error inesperado: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()