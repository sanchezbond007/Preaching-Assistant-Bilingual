#!/usr/bin/env python3
"""
Script de diagnóstico para detectar problemas de importación
Ejecutar: python diagnosticar.py
"""

import sys
import os
import importlib
import traceback

def diagnosticar_problema():
    print("🔍 === DIAGNÓSTICO DE IMPORTACIÓN ===\n")
    
    # 1. Verificar estructura de archivos
    print("📁 ESTRUCTURA DE ARCHIVOS:")
    archivos = [
        'main.py',
        'pantallas/__init__.py',
        'pantallas/menu.py'
    ]
    
    for archivo in archivos:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo)
            print(f"   ✅ {archivo} ({tamaño} bytes)")
        else:
            print(f"   ❌ {archivo} - NO EXISTE")
    
    # 2. Verificar contenido de __init__.py
    print("\n📄 CONTENIDO DE __init__.py:")
    try:
        with open('pantallas/__init__.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
            print(f"   Contenido: '{contenido}'")
            if len(contenido.strip()) == 0:
                print("   ⚠️ Archivo vacío (esto está bien)")
    except Exception as e:
        print(f"   ❌ Error leyendo __init__.py: {e}")
    
    # 3. Verificar sys.path
    print("\n🛤️ PYTHON PATH:")
    for i, path in enumerate(sys.path[:5]):  # Solo primeros 5
        print(f"   {i}: {path}")
    
    # 4. Limpiar caché e intentar importación
    print("\n🧹 LIMPIANDO CACHÉ...")
    modulos_pantallas = [name for name in sys.modules if 'pantallas' in name]
    for modulo in modulos_pantallas:
        del sys.modules[modulo]
        print(f"   🗑️ Removido: {modulo}")
    
    importlib.invalidate_caches()
    print("   ✅ Caché invalidado")
    
    # 5. Intento de importación CON DEBUGGING
    print("\n🔬 INTENTO DE IMPORTACIÓN:")
    try:
        print("   Paso 1: Importando pantallas...")
        import pantallas
        print(f"   ✅ pantallas importado: {pantallas}")
        
        print("   Paso 2: Importando pantallas.menu...")
        import pantallas.menu
        print(f"   ✅ pantallas.menu importado: {pantallas.menu}")
        
        print("   Paso 3: Verificando PantallaMenu...")
        if hasattr(pantallas.menu, 'PantallaMenu'):
            PantallaMenu = pantallas.menu.PantallaMenu
            print(f"   ✅ PantallaMenu encontrada: {PantallaMenu}")
            
            # Verificar herencia
            from kivy.uix.screenmanager import Screen
            if issubclass(PantallaMenu, Screen):
                print("   ✅ PantallaMenu es subclase de Screen")
            else:
                print("   ❌ PantallaMenu NO es subclase de Screen")
        else:
            print("   ❌ PantallaMenu NO encontrada en pantallas.menu")
            print(f"   Atributos disponibles: {[attr for attr in dir(pantallas.menu) if not attr.startswith('_')]}")
        
        print("\n🎯 RESULTADO: IMPORTACIÓN EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN IMPORTACIÓN: {type(e).__name__}: {e}")
        print("\n📋 TRACEBACK COMPLETO:")
        traceback.print_exc()
        return False

def verificar_encoding():
    print("\n🔤 VERIFICANDO ENCODING DE ARCHIVOS:")
    archivos = ['pantallas/__init__.py', 'pantallas/menu.py']
    
    for archivo in archivos:
        if os.path.exists(archivo):
            try:
                # Leer como binario para detectar BOM
                with open(archivo, 'rb') as f:
                    primeros_bytes = f.read(10)
                
                # Verificar BOM UTF-8
                if primeros_bytes.startswith(b'\xef\xbb\xbf'):
                    print(f"   ⚠️ {archivo} - TIENE BOM UTF-8 (puede causar problemas)")
                else:
                    print(f"   ✅ {archivo} - Sin BOM")
                
                # Intentar leer como UTF-8
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    print(f"   ✅ {archivo} - UTF-8 válido ({len(contenido)} caracteres)")
                    
            except Exception as e:
                print(f"   ❌ {archivo} - Error: {e}")

if __name__ == '__main__':
    print("🚀 Iniciando diagnóstico...\n")
    
    # Verificar encoding primero
    verificar_encoding()
    
    # Diagnóstico principal
    exito = diagnosticar_problema()
    
    print("\n" + "="*50)
    if exito:
        print("✅ DIAGNÓSTICO: Sin problemas detectados")
        print("🔧 Si aún tienes problemas, ejecuta: python arreglar_importacion.py")
    else:
        print("❌ DIAGNÓSTICO: Problemas detectados")
        print("🔧 Ejecuta: python arreglar_importacion.py")
    print("="*50)