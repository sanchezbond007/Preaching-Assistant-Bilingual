import json
import os

# Ruta al archivo de traducciones
RUTA_TRADUCCIONES = os.path.join("utils", "traducciones.json")

def obtener_idioma_actual():
    """Devuelve el idioma actual guardado"""
    archivo_idioma = "utils/idioma_actual.json"
    if os.path.exists(archivo_idioma):
        with open(archivo_idioma, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos.get("idioma", "es")
    return "es"

def cambiar_idioma(nuevo_idioma):
    """Guarda el idioma actual"""
    archivo_idioma = "utils/idioma_actual.json"
    with open(archivo_idioma, 'w', encoding='utf-8') as f:
        json.dump({"idioma": nuevo_idioma}, f, ensure_ascii=False, indent=2)

def obtener_texto(clave, idioma=None):
    """Devuelve el texto traducido según el idioma"""
    if idioma is None:
        idioma = obtener_idioma_actual()

    if not os.path.exists(RUTA_TRADUCCIONES):
        print("⚠️ Archivo traducciones no encontrado:", RUTA_TRADUCCIONES)
        return clave

    with open(RUTA_TRADUCCIONES, 'r', encoding='utf-8') as f:
        traducciones = json.load(f)

    return traducciones.get(clave, {}).get(idioma, clave)