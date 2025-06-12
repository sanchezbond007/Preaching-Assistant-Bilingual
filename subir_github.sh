#!/bin/bash

# Navega a la carpeta del proyecto
cd /storage/emulated/0/prueba_asistente_predicacion_bilingue || {
  echo "❌ No se encontró la ruta del proyecto. Verifica la carpeta."
  exit 1
}

# Agrega todos los cambios
git add .

# Muestra archivos preparados para commit
echo "📝 Archivos listos para commit:"
git status

# Commit automático con fecha
mensaje="Actualización automática - $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$mensaje"

# Sube a GitHub
echo "🚀 Subiendo cambios a GitHub..."
git push -u origin main

# Confirmación
echo "✅ Cambios subidos correctamente a GitHub."
