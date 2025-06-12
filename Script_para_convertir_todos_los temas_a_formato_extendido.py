import os
import json

CARPETA_ORIGEN = '/storage/emulated/0/prueba_asistente_predicacion_bilingue/datos/temas/'
CARPETA_DESTINO = '/storage/emulated/0/prueba_asistente_predicacion_bilingue/datos/temas_convertidos/'

if not os.path.exists(CARPETA_DESTINO):
    os.makedirs(CARPETA_DESTINO)

def formato_extendido(tema):
    return {
        "titulo": tema.get("titulo", {"es": tema.get("titulo_es", ""), "en": tema.get("titulo_en", "")}),
        "contenido": tema.get("contenido", {"es": tema.get("contenido_es", ""), "en": tema.get("contenido_en", "")}),
        "respuesta": tema.get("respuesta", {"es": tema.get("respuesta_es", ""), "en": tema.get("respuesta_en", "")}),
        "cita": tema.get("cita", ""),
        "link": tema.get("link", ""),
        "argumentos": tema.get("argumentos", {
            "argumentos_biblicos": [],
            "argumentos_logicos": [],
            "argumentos_historicos": [],
            "fuentes_recomendadas": []
        }),
        "secciones": tema.get("secciones", []),
        "versiculos": tema.get("versiculos", []),
        "enlaces": tema.get("enlaces", []),
        "conclusion": tema.get("conclusion", {"es": tema.get("conclusion_es", ""), "en": tema.get("conclusion_en", "")}),
        "copyright": tema.get("copyright", {
            "es": tema.get("copyright_es", ""),
            "en": tema.get("copyright_en", "")
        })
    }

for archivo in os.listdir(CARPETA_ORIGEN):
    if archivo.endswith('.json') and archivo.startswith('bloque_'):
        ruta_origen = os.path.join(CARPETA_ORIGEN, archivo)
        ruta_destino = os.path.join(CARPETA_DESTINO, archivo)
        try:
            with open(ruta_origen, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            if isinstance(datos, dict) and "temas" in datos:
                temas_convertidos = [formato_extendido(t) for t in datos["temas"]]
                datos_convertidos = {"temas": temas_convertidos}
            else:
                datos_convertidos = formato_extendido(datos)
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                json.dump(datos_convertidos, f, ensure_ascii=False, indent=2)
            print(f'Archivo convertido: {archivo}')
        except Exception as e:
            print(f'Error procesando {archivo}: {e}')
