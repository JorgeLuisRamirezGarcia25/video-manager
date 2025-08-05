"""
Módulo de estilos y temas para el Video Manager
Contiene definiciones de colores, fuentes y estilos personalizados
"""

class ModernTheme:
    """Tema moderno oscuro para la aplicación"""
    
    # Paleta de colores principal
    COLORS = {
        'bg_primary': '#1e1e1e',      # Fondo principal
        'bg_secondary': '#2d2d2d',    # Fondo secundario
        'bg_accent': '#404040',       # Fondo de acentos
        'bg_hover': '#4a4a4a',        # Hover estados
        
        'text_primary': '#ffffff',    # Texto principal
        'text_secondary': '#b3b3b3',  # Texto secundario
        'text_muted': '#808080',      # Texto deshabilitado
        
        'accent': '#0078d4',          # Color de acento principal
        'accent_hover': '#106ebe',    # Color de acento hover
        'accent_light': '#40a9ff',    # Color de acento claro
        
        'success': '#16c60c',         # Verde éxito
        'success_hover': '#14a085',   # Verde éxito hover
        'warning': '#f7b500',         # Amarillo advertencia
        'error': '#d13438',           # Rojo error
        'info': '#17a2b8',            # Azul información
        
        # Gradientes
        'gradient_primary': '#0078d4, #40a9ff',
        'gradient_success': '#16c60c, #52c41a',
    }
    
    # Configuración de fuentes
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'subtitle': ('Segoe UI', 11),
        'section': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'button': ('Segoe UI', 10),
        'button_large': ('Segoe UI', 12, 'bold'),
        'monospace': ('Consolas', 9),
        'small': ('Segoe UI', 8),
    }
    
    # Espaciado y medidas
    SPACING = {
        'xs': 5,
        'sm': 10,
        'md': 15,
        'lg': 20,
        'xl': 30,
    }
    
    # Configuración de bordes y esquinas
    BORDERS = {
        'radius': 6,
        'width': 1,
    }

class LightTheme:
    """Tema claro para la aplicación"""
    
    COLORS = {
        'bg_primary': '#ffffff',
        'bg_secondary': '#f8f9fa',
        'bg_accent': '#e9ecef',
        'bg_hover': '#dee2e6',
        
        'text_primary': '#212529',
        'text_secondary': '#6c757d',
        'text_muted': '#adb5bd',
        
        'accent': '#0d6efd',
        'accent_hover': '#0b5ed7',
        'accent_light': '#6ea8fe',
        
        'success': '#198754',
        'success_hover': '#157347',
        'warning': '#ffc107',
        'error': '#dc3545',
        'info': '#0dcaf0',
        
        'gradient_primary': '#0d6efd, #6ea8fe',
        'gradient_success': '#198754, #20c997',
    }
    
    FONTS = ModernTheme.FONTS.copy()
    SPACING = ModernTheme.SPACING.copy()
    BORDERS = ModernTheme.BORDERS.copy()

def get_theme(theme_name="dark"):
    """Obtiene el tema especificado"""
    if theme_name.lower() == "light":
        return LightTheme()
    return ModernTheme()

# Animaciones y transiciones (para futuras mejoras)
ANIMATIONS = {
    'fast': 200,      # milisegundos
    'normal': 300,
    'slow': 500,
}

# Iconos Unicode para usar en la interfaz
ICONS = {
    'download': '⬇️',
    'folder': '📁',
    'file': '📄',
    'music': '🎵',
    'settings': '⚙️',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': '💡',
    'cancel': '⏹️',
    'play': '▶️',
    'pause': '⏸️',
    'link': '🔗',
    'log': '📋',
    'progress': '📊',
    'heart': '❤️',
    'rocket': '🚀',
    'celebrate': '🎉',
    'skip': '⏭️',
}
