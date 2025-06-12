"""
GESTOR DE INTERESADOS - VERSIÓN TERMUX
Para Asistente de Predicación en Android
"""

import os
import json
from datetime import datetime

class GestorInteresados:
    def __init__(self):
        self.nombre_actual = ""
        self.email_actual = ""
        self.telefono_actual = ""
        self.temas_vistos = []
        
        # Crear carpeta en el directorio actual
        self.carpeta = "historiales"
        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)
        
        print("✅ Gestor iniciado")
    
    def establecer_interesado(self, nombre, email="", telefono=""):
        if not nombre or len(nombre.strip()) < 2:
            print("❌ Nombre inválido")
            return False
        
        self.nombre_actual = nombre.strip()
        self.email_actual = email.strip()
        self.telefono_actual = telefono.strip()
        self.cargar_historial()
        
        print(f"✅ Interesado: {self.nombre_actual}")
        return True
    
    def tiene_interesado(self):
        return bool(self.nombre_actual)
    
    def agregar_tema(self, tema, categoria="general"):
        if not self.tiene_interesado():
            print("⚠️ No hay interesado")
            return False
        
        nuevo_tema = {
            "tema": tema,
            "categoria": categoria,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.now().strftime("%H:%M:%S")
        }
        
        self.temas_vistos.append(nuevo_tema)
        self.guardar_historial()
        print(f"✅ Tema: {tema}")
        return True
    
    def cargar_historial(self):
        archivo = self.obtener_archivo()
        try:
            if os.path.exists(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.temas_vistos = datos.get("temas", [])
                print(f"📖 Cargado: {len(self.temas_vistos)} temas")
            else:
                self.temas_vistos = []
                print("📝 Nuevo historial")
        except Exception as e:
            print(f"❌ Error cargar: {e}")
            self.temas_vistos = []
    
    def guardar_historial(self):
        archivo = self.obtener_archivo()
        try:
            datos = {
                "nombre": self.nombre_actual,
                "email": self.email_actual,
                "telefono": self.telefono_actual,
                "fecha_actualizacion": datetime.now().isoformat(),
                "total": len(self.temas_vistos),
                "temas": self.temas_vistos
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Guardado")
            return True
        except Exception as e:
            print(f"❌ Error guardar: {e}")
            return False
    
    def obtener_archivo(self):
        nombre_limpio = "".join(c if c.isalnum() else "_" for c in self.nombre_actual)
        return os.path.join(self.carpeta, f"{nombre_limpio}.json")
    
    def obtener_resumen(self):
        if not self.tiene_interesado():
            return None
        
        categorias = {}
        for tema in self.temas_vistos:
            cat = tema["categoria"]
            categorias[cat] = categorias.get(cat, 0) + 1
        
        return {
            "nombre": self.nombre_actual,
            "email": self.email_actual,
            "telefono": self.telefono_actual,
            "total_temas": len(self.temas_vistos),
            "categorias": categorias
        }
    
    def limpiar_sesion(self):
        self.nombre_actual = ""
        self.email_actual = ""
        self.telefono_actual = ""
        self.temas_vistos = []
        print("🧹 Sesión limpiada")

def requiere_interesado(gestor):
    if not gestor.tiene_interesado():
        return False, "Debe establecer un interesado antes de continuar"
    return True, ""

# Test rápido
if __name__ == "__main__":
    print("🧪 Test rápido...")
    g = GestorInteresados()
    
    # Test establecer
    ok = g.establecer_interesado("María Test", "maria@test.com")
    print(f"Test 1: {'✅' if ok else '❌'}")
    
    # Test agregar tema
    ok = g.agregar_tema("Tema de prueba", "test")
    print(f"Test 2: {'✅' if ok else '❌'}")
    
    # Test resumen
    resumen = g.obtener_resumen()
    print(f"Test 3: {'✅' if resumen else '❌'}")
    
    if resumen:
        print(f"📊 {resumen['nombre']}: {resumen['total_temas']} temas")
    
    print("🧪 Test completado")