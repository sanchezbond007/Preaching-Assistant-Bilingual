#!/usr/bin/env python3
"""
SCRIPT PARA ARREGLAR EL FORMATO DE usuarios_registrados.json
El error indica que es un dict cuando debería ser una lista
"""

import json
import os
from datetime import datetime

def arreglar_formato_usuarios():
    print("🔧 === ARREGLANDO FORMATO DE USUARIOS ===")
    
    archivo = "usuarios_registrados.json"
    
    if not os.path.exists(archivo):
        print(f"❌ Archivo {archivo} no existe")
        return False
    
    try:
        # Leer archivo actual
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
        
        print(f"📄 Tipo de contenido actual: {type(contenido)}")
        
        # Si es un diccionario, convertir a lista
        if isinstance(contenido, dict):
            print("🔄 Convirtiendo dict a lista...")
            
            # Crear backup
            backup_file = f"{archivo}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(contenido, f, indent=2, ensure_ascii=False)
            print(f"💾 Backup creado: {backup_file}")
            
            # Convertir a lista de usuarios
            usuarios_lista = []
            
            # Si tiene estructura específica, extraer usuarios
            if 'usuarios' in contenido:
                if isinstance(contenido['usuarios'], list):
                    usuarios_lista = contenido['usuarios']
                elif isinstance(contenido['usuarios'], dict):
                    # Convertir cada entrada del dict en un usuario
                    for key, user_data in contenido['usuarios'].items():
                        if isinstance(user_data, dict):
                            user_data['usuario'] = key  # Asegurar que tenga el campo usuario
                            usuarios_lista.append(user_data)
            else:
                # Si el contenido raíz son usuarios directos
                for key, user_data in contenido.items():
                    if isinstance(user_data, dict):
                        # Si no tiene campo 'usuario', usar la key
                        if 'usuario' not in user_data:
                            user_data['usuario'] = key
                        usuarios_lista.append(user_data)
                    elif isinstance(user_data, str):
                        # Si es solo una string, crear usuario básico
                        usuarios_lista.append({
                            "usuario": key,
                            "contrasena": user_data,
                            "activo": True,
                            "tipo": "usuario_normal"
                        })
            
            print(f"📊 Usuarios extraídos: {len(usuarios_lista)}")
            
            # Mostrar usuarios encontrados
            for i, usuario in enumerate(usuarios_lista, 1):
                if isinstance(usuario, dict):
                    print(f"   {i}. {usuario.get('usuario', 'N/A')} - {usuario.get('contrasena', 'N/A')}")
            
            # Guardar formato corregido
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(usuarios_lista, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Formato corregido: {archivo} ahora es una lista")
            return True
            
        elif isinstance(contenido, list):
            print("✅ El archivo ya tiene formato correcto (lista)")
            
            # Mostrar usuarios
            for i, usuario in enumerate(contenido, 1):
                if isinstance(usuario, dict):
                    print(f"   {i}. {usuario.get('usuario', 'N/A')} - {usuario.get('contrasena', 'N/A')}")
            
            return True
        else:
            print(f"❌ Formato desconocido: {type(contenido)}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def actualizar_contrasena_usuario(usuario, nueva_contrasena):
    """Actualizar contraseña de un usuario específico"""
    print(f"🔐 === ACTUALIZANDO CONTRASEÑA DE {usuario} ===")
    
    archivo = "usuarios_registrados.json"
    
    if not os.path.exists(archivo):
        print(f"❌ Archivo {archivo} no existe")
        return False
    
    try:
        # Leer usuarios
        with open(archivo, 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
        
        if not isinstance(usuarios, list):
            print("❌ El archivo debe ser una lista. Ejecuta arreglar_formato_usuarios() primero")
            return False
        
        # Buscar y actualizar usuario
        usuario_encontrado = False
        for i, user in enumerate(usuarios):
            if isinstance(user, dict) and user.get('usuario') == usuario:
                print(f"🔍 Usuario encontrado: {usuario}")
                print(f"🔒 Contraseña antigua: {user.get('contrasena')}")
                
                # Actualizar contraseña
                usuarios[i]['contrasena'] = nueva_contrasena
                usuarios[i]['fecha_actualizacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"🔒 Contraseña nueva: {nueva_contrasena}")
                usuario_encontrado = True
                break
        
        if not usuario_encontrado:
            print(f"❌ Usuario '{usuario}' no encontrado")
            return False
        
        # Guardar cambios
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Contraseña actualizada para {usuario}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🛠️ === HERRAMIENTA DE REPARACIÓN DE USUARIOS ===")
    
    # 1. Arreglar formato
    print("\n1️⃣ ARREGLANDO FORMATO...")
    exito_formato = arreglar_formato_usuarios()
    
    if exito_formato:
        print("\n2️⃣ ¿ACTUALIZAR CONTRASEÑA?")
        print("Tu usuario 'sanchezbond007' tiene contraseña 'password123'")
        print("¿Quieres cambiarla a '3863'? (s/n): ", end="")
        
        # Para script automático, cambiar directamente
        # respuesta = input().lower()
        # if respuesta in ['s', 'si', 'yes', 'y']:
        
        print("Actualizando automáticamente...")
        exito_password = actualizar_contrasena_usuario('sanchezbond007', '3863')
        
        if exito_password:
            print("\n🎉 ¡REPARACIÓN COMPLETA!")
            print("✅ Formato corregido")
            print("✅ Contraseña actualizada")
            print("\n🔑 Ahora puedes hacer login con:")
            print("   Usuario: sanchezbond007")
            print("   Contraseña: 3863")
        else:
            print("\n⚠️ Formato corregido pero falló actualización de contraseña")
    
    else:
        print("\n❌ No se pudo corregir el formato")