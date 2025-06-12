#!/usr/bin/env python3
"""
SCRIPT PARA MIGRAR USUARIO DE usuarios_nuevos.json A usuarios_registrados.json
Ejecuta este script para migrar tu usuario correctamente
"""

import json
import os
from datetime import datetime

def migrar_usuario():
    print("🔄 === MIGRACIÓN DE USUARIO ===")
    
    # Archivos
    archivo_origen = "usuarios_nuevos.json"
    archivo_destino = "usuarios_registrados.json"
    
    # Verificar que existe el archivo origen
    if not os.path.exists(archivo_origen):
        print(f"❌ No se encontró {archivo_origen}")
        return False
    
    try:
        # Leer usuarios nuevos
        with open(archivo_origen, 'r', encoding='utf-8') as f:
            usuarios_nuevos = json.load(f)
        
        print(f"📄 Usuarios en {archivo_origen}: {len(usuarios_nuevos)}")
        
        # Leer usuarios registrados (si existe)
        usuarios_registrados = []
        if os.path.exists(archivo_destino):
            with open(archivo_destino, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if contenido:
                    usuarios_registrados = json.load(f)
        
        print(f"📄 Usuarios en {archivo_destino}: {len(usuarios_registrados)}")
        
        # Migrar cada usuario
        usuarios_migrados = 0
        
        for usuario_nuevo in usuarios_nuevos:
            if isinstance(usuario_nuevo, dict):
                # Verificar que no existe ya
                existe = False
                for usuario_reg in usuarios_registrados:
                    if isinstance(usuario_reg, dict):
                        if usuario_reg.get('usuario') == usuario_nuevo.get('usuario'):
                            existe = True
                            break
                
                if not existe:
                    # Formatear para compatibilidad con login
                    usuario_formateado = {
                        "usuario": usuario_nuevo.get('usuario'),
                        "contrasena": usuario_nuevo.get('contrasena'),
                        "nombre": usuario_nuevo.get('nombre', ''),
                        "apellido": usuario_nuevo.get('apellido', ''),
                        "telefono": usuario_nuevo.get('telefono', ''),
                        "correo": usuario_nuevo.get('correo', ''),
                        "fecha_creacion": usuario_nuevo.get('fecha_creacion', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        "activo": True,
                        "tipo": "usuario_normal"
                    }
                    
                    usuarios_registrados.append(usuario_formateado)
                    usuarios_migrados += 1
                    
                    print(f"✅ Migrado: {usuario_nuevo.get('usuario')} - Contraseña: {usuario_nuevo.get('contrasena')}")
                else:
                    print(f"⚠️ Ya existe: {usuario_nuevo.get('usuario')}")
        
        # Guardar usuarios registrados
        with open(archivo_destino, 'w', encoding='utf-8') as f:
            json.dump(usuarios_registrados, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migración completada: {usuarios_migrados} usuarios migrados")
        print(f"📊 Total usuarios en {archivo_destino}: {len(usuarios_registrados)}")
        
        # Mostrar usuarios disponibles para login
        print("\n🔑 === USUARIOS DISPONIBLES PARA LOGIN ===")
        for i, usuario in enumerate(usuarios_registrados, 1):
            if isinstance(usuario, dict):
                print(f"   {i}. Usuario: {usuario.get('usuario')} - Contraseña: {usuario.get('contrasena')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        import traceback
        traceback.print_exc()
        return False

def mostrar_archivos():
    """Mostrar contenido de archivos de usuarios"""
    print("\n🔍 === CONTENIDO DE ARCHIVOS ===")
    
    archivos = ["usuarios_nuevos.json", "usuarios_registrados.json", "usuarios.json"]
    
    for archivo in archivos:
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = json.load(f)
                
                print(f"\n📄 {archivo}:")
                for i, usuario in enumerate(contenido, 1):
                    if isinstance(usuario, dict):
                        print(f"   {i}. {usuario.get('usuario', 'N/A')} - {usuario.get('contrasena', 'N/A')}")
                    else:
                        print(f"   {i}. {usuario}")
                        
            except Exception as e:
                print(f"❌ Error leyendo {archivo}: {e}")
        else:
            print(f"\n📄 {archivo}: No existe")

if __name__ == "__main__":
    print("🧪 === SCRIPT DE MIGRACIÓN DE USUARIOS ===")
    print("🎯 Este script migrará usuarios de usuarios_nuevos.json a usuarios_registrados.json")
    print()
    
    # Mostrar estado actual
    mostrar_archivos()
    
    # Realizar migración
    print("\n" + "="*50)
    exito = migrar_usuario()
    
    if exito:
        print("\n🎉 ¡MIGRACIÓN EXITOSA!")
        print("✅ Ahora puedes hacer login con los usuarios migrados")
    else:
        print("\n❌ MIGRACIÓN FALLIDA")
    
    # Mostrar estado final
    print("\n" + "="*50)
    mostrar_archivos()