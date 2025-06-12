#!/usr/bin/env python3

print("=== PRUEBA RAPIDA ===")

# Test 1: Verificar archivos
import os
print("1. Archivos:")
if os.path.exists('pantallas/__init__.py'):
    print("   ✅ __init__.py existe")
else:
    print("   ❌ __init__.py NO existe")

if os.path.exists('pantallas/menu.py'):
    print("   ✅ menu.py existe")
else:
    print("   ❌ menu.py NO existe")

# Test 2: Intentar importación
print("\n2. Importación:")
try:
    from pantallas.menu import PantallaMenu
    print("   ✅ IMPORTACIÓN EXITOSA")
    print(f"   ✅ PantallaMenu = {PantallaMenu}")
    
    # Test 3: Crear instancia
    print("\n3. Crear instancia:")
    menu = PantallaMenu(name='test')
    print("   ✅ INSTANCIA CREADA")
    print("   🎉 TODO FUNCIONA - EL PROBLEMA ESTÁ EN main.py")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    print("   🔧 HAY QUE ARREGLAR menu.py")

print("\n=== FIN ===")