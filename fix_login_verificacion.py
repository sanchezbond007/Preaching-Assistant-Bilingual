# CÓDIGO PARA ARREGLAR EL MÉTODO DE VERIFICACIÓN EN login.py

def verificar_credenciales(self, usuario, contrasena):
    """
    REEMPLAZA EL MÉTODO verificar_credenciales EN pantallas/login.py
    CON ESTE CÓDIGO CORREGIDO
    """
    print(f"🔍 Verificando credenciales...")
    
    try:
        archivo_usuarios = "usuarios_registrados.json"
        
        if not os.path.exists(archivo_usuarios):
            print(f"❌ Archivo {archivo_usuarios} no existe")
            return False, "Base de datos no encontrada"
        
        # Leer usuarios
        with open(archivo_usuarios, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
            if not contenido:
                print("❌ Archivo vacío")
                return False, "Base de datos vacía"
            
            usuarios = json.loads(contenido)
        
        print(f"🔍 Base de datos cargada. Tipo: {type(usuarios)}")
        
        # ✅ ASEGURAR QUE SEA UNA LISTA
        if isinstance(usuarios, dict):
            print("🔄 Convirtiendo dict a lista...")
            usuarios_lista = []
            for key, value in usuarios.items():
                if isinstance(value, dict):
                    if 'usuario' not in value:
                        value['usuario'] = key
                    usuarios_lista.append(value)
                elif isinstance(value, str):
                    usuarios_lista.append({
                        "usuario": key,
                        "contrasena": value,
                        "activo": True
                    })
            usuarios = usuarios_lista
        
        # ✅ VERIFICAR QUE SEA LISTA
        if not isinstance(usuarios, list):
            print(f"❌ Formato incorrecto: {type(usuarios)}")
            return False, "Formato de base de datos incorrecto"
        
        # Obtener lista de usuarios para mostrar
        usuarios_disponibles = []
        for user in usuarios:
            if isinstance(user, dict):
                usuarios_disponibles.append(user.get('usuario', 'N/A'))
        
        print(f"🔍 Usuarios disponibles: {usuarios_disponibles}")
        
        # Buscar usuario
        print(f"🔍 Buscando usuario: '{usuario}'")
        
        for user in usuarios:
            if isinstance(user, dict) and user.get('usuario') == usuario:
                print(f"🔍 Usuario encontrado. Contraseña guardada: '{user.get('contrasena')}'")
                print(f"🔍 Contraseña ingresada: '{contrasena}'")
                
                if user.get('contrasena') == contrasena:
                    print(f"✅ Login exitoso para usuario: {usuario}")
                    return True, "Login exitoso"
                else:
                    print(f"❌ Contraseña incorrecta para usuario: {usuario}")
                    print(f"   Esperada: '{user.get('contrasena')}' | Recibida: '{contrasena}'")
                    return False, "Contraseña incorrecta"
        
        print(f"❌ Usuario '{usuario}' no encontrado")
        return False, "Usuario no encontrado"
        
    except json.JSONDecodeError as e:
        print(f"❌ Error JSON: {e}")
        return False, "Error en base de datos"
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error del sistema: {str(e)}"

# ✅ TAMBIÉN NECESITAS AÑADIR ESTE IMPORT AL INICIO DEL ARCHIVO login.py:
# import json
# import os