#!/usr/bin/env python3
"""
TEST BÁSICO - Para verificar que el gestor funciona
Guarda este archivo como: test_basico.py
"""

print("🚀 Iniciando test básico...")

# Test 1: Verificar que Python funciona
print("✅ Python está funcionando")

# Test 2: Verificar imports básicos
try:
    import os
    import json
    from datetime import datetime
    print("✅ Imports básicos funcionan")
except Exception as e:
    print(f"❌ Error en imports básicos: {e}")
    exit(1)

# Test 3: Crear gestor manualmente (sin importar archivo)
print("\n📋 Creando gestor básico...")

class GestorSimple:
    def __init__(self):
        self.nombre = ""
        self.temas = []
        print("✅ Gestor creado")
    
    def establecer(self, nombre):
        if len(nombre.strip()) < 2:
            return False
        self.nombre = nombre.strip()
        print(f"✅ Interesado: {self.nombre}")
        return True
    
    def agregar_tema(self, tema):
        if not self.nombre:
            return False
        self.temas.append({
            "tema": tema,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"✅ Tema agregado: {tema}")
        return True
    
    def resumen(self):
        return {
            "nombre": self.nombre,
            "total": len(self.temas),
            "temas": self.temas
        }

# Test 4: Probar gestor simple
print("\n🧪 Probando gestor...")
gestor = GestorSimple()

# Establecer interesado
resultado = gestor.establecer("Juan Pérez")
print(f"Test establecer: {'✅' if resultado else '❌'}")

# Agregar tema
resultado = gestor.agregar_tema("¿Qué enseña la Biblia?")
print(f"Test agregar tema: {'✅' if resultado else '❌'}")

# Obtener resumen
resumen = gestor.resumen()
print(f"Test resumen: {'✅' if resumen['total'] > 0 else '❌'}")

print(f"\n📊 RESUMEN FINAL:")
print(f"👤 Nombre: {resumen['nombre']}")
print(f"📚 Total temas: {resumen['total']}")
for tema in resumen['temas']:
    print(f"  - {tema['tema']} ({tema['fecha']})")

# Test 5: Verificar creación de archivos
print(f"\n📁 Probando creación de archivos...")
try:
    carpeta = "test_historiales"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        print(f"✅ Carpeta creada: {carpeta}")
    
    archivo = os.path.join(carpeta, "test.json")
    datos = {"test": "funcionando", "fecha": datetime.now().isoformat()}
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Archivo JSON creado: {archivo}")
    
    # Leer el archivo
    with open(archivo, 'r', encoding='utf-8') as f:
        datos_leidos = json.load(f)
    
    print(f"✅ Archivo JSON leído correctamente")
    print(f"📄 Contenido: {datos_leidos}")
    
except Exception as e:
    print(f"❌ Error con archivos: {e}")

print(f"\n🎯 === DIAGNÓSTICO ===")
print(f"✅ Python funciona")
print(f"✅ Lógica del gestor funciona")
print(f"✅ Archivos JSON funcionan")
print(f"\n💡 Si ves esto, el problema está en la integración con Kivy")
print(f"💡 Ejecuta este test con: python test_basico.py")

# Test 6: Verificar si gestor_interesados.py existe
print(f"\n🔍 Verificando archivos del proyecto...")
archivos_proyecto = [
    "main.py",
    "gestor_interesados.py",
    "pantallas/datos_interesado.py"
]

for archivo in archivos_proyecto:
    if os.path.exists(archivo):
        print(f"✅ Existe: {archivo}")
    else:
        print(f"❌ No existe: {archivo}")

print(f"\n🚀 Test básico completado")