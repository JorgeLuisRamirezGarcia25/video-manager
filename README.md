# 🎵 YouTube Audio Downloader Pro

Una aplicación moderna y elegante para descargar audio de alta calidad desde YouTube con una interfaz de usuario completamente renovada.

## ✨ Características Principales

### 🎨 Interfaz Moderna
- **Diseño Responsive**: Se adapta automáticamente al tamaño de la ventana
- **UI/UX Mejorada**: Interfaz limpia y profesional con iconos y colores modernos
- **Tipografía Mejorada**: Fuentes Segoe UI para mejor legibilidad
- **Esquema de Colores**: Paleta de colores Material Design

### 🚀 Funcionalidades Avanzadas
- **Drag & Drop**: Arrastra archivos de texto directamente a la aplicación
- **Pegado Automático**: Botón para pegar URLs desde el portapapeles
- **Progress Tracking**: Barra de progreso y registro detallado en tiempo real
- **Configuración Avanzada**: Panel de configuración con múltiples opciones
- **Estadísticas**: Seguimiento de descargas exitosas y errores

### 🎵 Opciones de Audio
- **Múltiples Calidades**: 128, 192, 320 kbps
- **Formatos Soportados**: MP3, M4A, OGG
- **Detección de Duplicados**: Omite archivos ya descargados
- **Reintentos Configurables**: Sistema robusto de reintentos

### 📁 Gestión de Archivos
- **Selección de Carpeta**: Interfaz mejorada para selección de destino
- **Soporte de Playlists**: Descarga playlists completas de YouTube
- **Archivos de URLs**: Soporte para archivos de texto con múltiples URLs
- **Validación de Entrada**: Validación completa de URLs y archivos

## 🛠️ Instalación

### Método 1: Ejecución Automática (Recomendado)
```bash
# Clonar o descargar el proyecto
# Navegar al directorio del proyecto
cd video-manager-main

# Ejecutar el script de inicio (instalará dependencias automáticamente)
./run_app.sh
```

### Método 2: Instalación Manual

#### Prerrequisitos
- Python 3.7 o superior
- FFmpeg (para conversión de audio)

#### Instalación de FFmpeg

##### En Kali Linux/Debian/Ubuntu:
```bash
sudo apt update
sudo apt install ffmpeg
```

##### En Windows:
```bash
# Descargar FFmpeg desde https://ffmpeg.org/download.html
# Extraer y agregar al PATH del sistema
```

##### En macOS:
```bash
brew install ffmpeg
```

#### Instalación Manual del Proyecto

1. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/macOS
# o
venv\Scripts\activate     # En Windows
```

2. **Instalar dependencias:**
```bash
pip install --upgrade pip
pip install yt-dlp tkinterdnd2 pillow
```

3. **Ejecutar la aplicación:**
```bash
python programa_audio_youtube_interfaz.py
```

## 🎯 Uso de la Aplicación

### Métodos de Entrada
1. **URL Individual**: Pega una URL de YouTube directamente
2. **Archivo de URLs**: Selecciona un archivo .txt con una URL por línea
3. **Drag & Drop**: Arrastra un archivo .txt a la zona de drop

### Proceso de Descarga
1. **Configurar Entrada**: URL, archivo o drag & drop
2. **Seleccionar Carpeta**: Elige dónde guardar los archivos
3. **Configurar Opciones**: (Opcional) Ajusta calidad y formato
4. **Iniciar Descarga**: Haz clic en "Descargar Audio"
5. **Monitorear Progreso**: Observa el progreso en tiempo real

### Panel de Configuración
- **Calidad de Audio**: 128, 192, 320 kbps
- **Formato de Salida**: MP3, M4A, OGG
- **Omitir Existentes**: Evita re-descargar archivos
- **Número de Reintentos**: Configura reintentos para URLs fallidas

## 📊 Interfaz de Usuario

### Secciones Principales
1. **Header**: Título y descripción de la aplicación
2. **Input Section**: Entrada de URLs con drag & drop
3. **Control Section**: Botones principales de acción
4. **Progress Section**: Barra de progreso y log detallado
5. **Footer**: Estadísticas y información de versión

### Responsive Design
- **Grid Layout**: Sistema de grid que se adapta al tamaño
- **Minimum Size**: Tamaño mínimo de ventana para usabilidad
- **Proportional Scaling**: Elementos se escalan proporcionalmente
- **Auto-centering**: Ventana se centra automáticamente

## 📝 Formato del Archivo de URLs

Crea un archivo `.txt` con una URL por línea:

```
https://www.youtube.com/watch?v=VIDEO_ID1
https://www.youtube.com/watch?v=VIDEO_ID2
https://www.youtube.com/playlist?list=PLAYLIST_ID
```

## 🐛 Solución de Problemas

### Errores Comunes
- **FFmpeg no encontrado**: Instala FFmpeg y agrégalo al PATH
- **Error de red**: Verifica tu conexión a internet
- **URLs inválidas**: Verifica que las URLs sean de YouTube válidas
- **Permisos de carpeta**: Asegúrate de tener permisos de escritura

## 📜 Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE.
