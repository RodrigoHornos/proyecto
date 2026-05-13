"""
Modelo de configuración para la calculadora.

Este módulo gestiona la configuración de la aplicación, incluyendo temas,
preferencias del usuario y persistencia de datos.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from enum import Enum


class Theme(Enum):
    """Temas disponibles para la calculadora."""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    HIGH_CONTRAST = "high_contrast"


class ConfigModel:
    """
    Modelo que gestiona la configuración de la aplicación.
    
    Attributes:
        theme: Tema actual de la interfaz
        font_size: Tamaño de fuente
        window_size: Tamaño de la ventana (ancho, alto)
        window_position: Posición de la ventana (x, y)
        mode: Modo de operación actual
        history_limit: Límite de entradas en historial
        auto_save: Si se guarda automáticamente
        sound_enabled: Si los sonidos están habilitados
        animations_enabled: Si las animaciones están habilitadas
    """
    
    # Configuración por defecto
    DEFAULT_CONFIG = {
        'theme': Theme.LIGHT.value,
        'font_size': 12,
        'window_size': (400, 600),
        'window_position': None,
        'mode': 'básico',
        'history_limit': 100,
        'auto_save': True,
        'sound_enabled': False,
        'animations_enabled': True,
        'keyboard_shortcuts': {},
        'decimal_places': 10,
        'angle_unit': 'degrees',  # degrees o radians
        'scientific_notation': False,
        'thousands_separator': False,
    }
    
    # Definición de temas
    THEMES = {
        Theme.LIGHT: {
            'bg': '#FFFFFF',
            'fg': '#000000',
            'button_bg': '#F0F0F0',
            'button_fg': '#000000',
            'button_active': '#E0E0E0',
            'display_bg': '#FFFFFF',
            'display_fg': '#000000',
            'operator_bg': '#FFA500',
            'operator_fg': '#FFFFFF',
            'equals_bg': '#4CAF50',
            'equals_fg': '#FFFFFF',
        },
        Theme.DARK: {
            'bg': '#2B2B2B',
            'fg': '#FFFFFF',
            'button_bg': '#3C3C3C',
            'button_fg': '#FFFFFF',
            'button_active': '#4C4C4C',
            'display_bg': '#1E1E1E',
            'display_fg': '#FFFFFF',
            'operator_bg': '#FF8C00',
            'operator_fg': '#FFFFFF',
            'equals_bg': '#45A049',
            'equals_fg': '#FFFFFF',
        },
        Theme.BLUE: {
            'bg': '#E3F2FD',
            'fg': '#0D47A1',
            'button_bg': '#BBDEFB',
            'button_fg': '#0D47A1',
            'button_active': '#90CAF9',
            'display_bg': '#FFFFFF',
            'display_fg': '#0D47A1',
            'operator_bg': '#2196F3',
            'operator_fg': '#FFFFFF',
            'equals_bg': '#1976D2',
            'equals_fg': '#FFFFFF',
        },
        Theme.GREEN: {
            'bg': '#E8F5E9',
            'fg': '#1B5E20',
            'button_bg': '#C8E6C9',
            'button_fg': '#1B5E20',
            'button_active': '#A5D6A7',
            'display_bg': '#FFFFFF',
            'display_fg': '#1B5E20',
            'operator_bg': '#4CAF50',
            'operator_fg': '#FFFFFF',
            'equals_bg': '#388E3C',
            'equals_fg': '#FFFFFF',
        },
        Theme.PURPLE: {
            'bg': '#F3E5F5',
            'fg': '#4A148C',
            'button_bg': '#E1BEE7',
            'button_fg': '#4A148C',
            'button_active': '#CE93D8',
            'display_bg': '#FFFFFF',
            'display_fg': '#4A148C',
            'operator_bg': '#9C27B0',
            'operator_fg': '#FFFFFF',
            'equals_bg': '#7B1FA2',
            'equals_fg': '#FFFFFF',
        },
        Theme.HIGH_CONTRAST: {
            'bg': '#000000',
            'fg': '#FFFF00',
            'button_bg': '#000000',
            'button_fg': '#FFFF00',
            'button_active': '#333333',
            'display_bg': '#000000',
            'display_fg': '#FFFF00',
            'operator_bg': '#FFFF00',
            'operator_fg': '#000000',
            'equals_bg': '#00FF00',
            'equals_fg': '#000000',
        },
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Inicializa el modelo de configuración.
        
        Args:
            config_file: Ruta al archivo de configuración (opcional)
        """
        self._config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self._config_file = config_file or self._get_default_config_path()
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """
        Obtiene la ruta por defecto del archivo de configuración.
        
        Returns:
            Ruta al archivo de configuración
        """
        # Usar directorio home del usuario
        home = Path.home()
        config_dir = home / '.calculadora'
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / 'config.json')
    
    def _load_config(self) -> None:
        """Carga la configuración desde el archivo."""
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Actualizar solo las claves válidas
                    for key, value in loaded_config.items():
                        if key in self.DEFAULT_CONFIG:
                            self._config[key] = value
            except (json.JSONDecodeError, IOError):
                # Si hay error, usar configuración por defecto
                pass
    
    def save_config(self) -> bool:
        """
        Guarda la configuración en el archivo.
        
        Returns:
            True si se guardó correctamente
        """
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
            
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.
        
        Args:
            key: Clave de configuración
            default: Valor por defecto si no existe
            
        Returns:
            Valor de configuración
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Establece un valor de configuración.
        
        Args:
            key: Clave de configuración
            value: Valor a establecer
            
        Returns:
            True si se estableció correctamente
        """
        if key not in self.DEFAULT_CONFIG:
            return False
        
        self._config[key] = value
        
        # Auto-guardar si está habilitado
        if self._config.get('auto_save', True):
            self.save_config()
        
        return True
    
    def reset_to_defaults(self) -> None:
        """Restaura la configuración a los valores por defecto."""
        self._config = self.DEFAULT_CONFIG.copy()
        if self._config.get('auto_save', True):
            self.save_config()
    
    def reset_key(self, key: str) -> bool:
        """
        Restaura una clave específica a su valor por defecto.
        
        Args:
            key: Clave a restaurar
            
        Returns:
            True si se restauró
        """
        if key in self.DEFAULT_CONFIG:
            self._config[key] = self.DEFAULT_CONFIG[key]
            if self._config.get('auto_save', True):
                self.save_config()
            return True
        return False
    
    @property
    def theme(self) -> Theme:
        """Tema actual."""
        theme_value = self._config.get('theme', Theme.LIGHT.value)
        try:
            return Theme(theme_value)
        except ValueError:
            return Theme.LIGHT
    
    @theme.setter
    def theme(self, value: Theme) -> None:
        """Establece el tema."""
        if isinstance(value, Theme):
            self.set('theme', value.value)
        elif isinstance(value, str):
            try:
                theme = Theme(value)
                self.set('theme', theme.value)
            except ValueError:
                pass
    
    def get_theme_colors(self, theme: Optional[Theme] = None) -> Dict[str, str]:
        """
        Obtiene los colores de un tema.
        
        Args:
            theme: Tema a consultar (None = tema actual)
            
        Returns:
            Diccionario con los colores del tema
        """
        if theme is None:
            theme = self.theme
        
        return self.THEMES.get(theme, self.THEMES[Theme.LIGHT]).copy()
    
    @property
    def font_size(self) -> int:
        """Tamaño de fuente."""
        return self._config.get('font_size', 12)
    
    @font_size.setter
    def font_size(self, value: int) -> None:
        """Establece el tamaño de fuente."""
        if 8 <= value <= 24:
            self.set('font_size', value)
    
    @property
    def window_size(self) -> tuple:
        """Tamaño de ventana (ancho, alto)."""
        return tuple(self._config.get('window_size', (400, 600)))
    
    @window_size.setter
    def window_size(self, value: tuple) -> None:
        """Establece el tamaño de ventana."""
        if len(value) == 2 and all(isinstance(v, int) and v > 0 for v in value):
            self.set('window_size', list(value))
    
    @property
    def window_position(self) -> Optional[tuple]:
        """Posición de ventana (x, y)."""
        pos = self._config.get('window_position')
        return tuple(pos) if pos else None
    
    @window_position.setter
    def window_position(self, value: Optional[tuple]) -> None:
        """Establece la posición de ventana."""
        if value is None:
            self.set('window_position', None)
        elif len(value) == 2 and all(isinstance(v, int) for v in value):
            self.set('window_position', list(value))
    
    @property
    def mode(self) -> str:
        """Modo de operación actual."""
        return self._config.get('mode', 'básico')
    
    @mode.setter
    def mode(self, value: str) -> None:
        """Establece el modo de operación."""
        self.set('mode', value)
    
    @property
    def history_limit(self) -> int:
        """Límite de entradas en historial."""
        return self._config.get('history_limit', 100)
    
    @history_limit.setter
    def history_limit(self, value: int) -> None:
        """Establece el límite de historial."""
        if value >= 0:
            self.set('history_limit', value)
    
    @property
    def auto_save(self) -> bool:
        """Si se guarda automáticamente."""
        return self._config.get('auto_save', True)
    
    @auto_save.setter
    def auto_save(self, value: bool) -> None:
        """Establece el auto-guardado."""
        self.set('auto_save', value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Exporta la configuración a diccionario.
        
        Returns:
            Diccionario con la configuración
        """
        return self._config.copy()
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Importa configuración desde diccionario.
        
        Args:
            data: Diccionario con configuración
        """
        for key, value in data.items():
            if key in self.DEFAULT_CONFIG:
                self._config[key] = value
        
        if self._config.get('auto_save', True):
            self.save_config()
    
    def __str__(self) -> str:
        """Representación en string."""
        return f"ConfigModel(theme={self.theme.value}, mode={self.mode}, font_size={self.font_size})"
    
    def __repr__(self) -> str:
        """Representación técnica."""
        return f"ConfigModel(config_file='{self._config_file}')"

# Made with Bob
