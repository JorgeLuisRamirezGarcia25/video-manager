#!/bin/bash

# Script para ejecutar YouTube Audio Downloader Pro
# Navegamos al directorio del proyecto
cd "$(dirname "$0")"

# Verificamos si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv venv
    
    echo "📦 Instalando dependencias..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install yt-dlp tkinterdnd2 pillow
else
    echo "✅ Entorno virtual encontrado"
fi

# Activamos el entorno virtual y ejecutamos la aplicación
echo "🚀 Iniciando YouTube Audio Downloader Pro..."
source venv/bin/activate
python programa_audio_youtube_interfaz.py
