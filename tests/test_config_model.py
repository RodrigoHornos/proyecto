"""
Tests para el modelo de configuración (ConfigModel y Theme).

Verifica el correcto funcionamiento del sistema de configuración incluyendo:
- Gestión de temas
- Persistencia de configuración
- Propiedades y validaciones
- Exportación/importación
"""

import pytest
import os
import tempfile
import json
from models.config_model import ConfigModel, Theme


class TestTheme:
    """Tests para el enum Theme."""
    
    def test_theme_values(self):
        """Test: valores del enum Theme."""
        assert Theme.LIGHT.value == "light"
        assert Theme.DARK.value == "dark"
        assert Theme.BLUE.value == "blue"
        assert Theme.GREEN.value == "green"
        assert Theme.PURPLE.value == "purple"
        assert Theme.HIGH_CONTRAST.value == "high_contrast"
    
    def test_theme_from_value(self):
        """Test: crear Theme desde valor."""
        theme = Theme("dark")
        assert theme == Theme.DARK
    
    def test_theme_invalid_value(self):
        """Test: valor inválido lanza excepción."""
        with pytest.raises(ValueError):
            Theme("invalid_theme")


class TestConfigModel:
    """Tests para la clase ConfigModel."""
    
    @pytest.fixture
    def temp_config_file(self):
        """Fixture que crea un archivo temporal para configuración."""
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)
    
    def test_create_config(self, temp_config_file):
        """Test: crear configuración."""
        config = ConfigModel(temp_config_file)
        
        assert config.theme == Theme.LIGHT
        assert config.font_size == 12
        assert config.mode == 'básico'
        assert config.auto_save == True
    
    def test_get_value(self, temp_config_file):
        """Test: obtener valor de configuración."""
        config = ConfigModel(temp_config_file)
        
        assert config.get('theme') == 'light'
        assert config.get('font_size') == 12
        assert config.get('nonexistent', 'default') == 'default'
    
    def test_set_value(self, temp_config_file):
        """Test: establecer valor de configuración."""
        config = ConfigModel(temp_config_file)
        
        success = config.set('font_size', 14)
        
        assert success
        assert config.get('font_size') == 14
    
    def test_set_invalid_key(self, temp_config_file):
        """Test: establecer clave inválida."""
        config = ConfigModel(temp_config_file)
        
        success = config.set('invalid_key', 'value')
        
        assert not success
    
    def test_save_and_load_config(self, temp_config_file):
        """Test: guardar y cargar configuración."""
        # Crear y configurar
        config1 = ConfigModel(temp_config_file)
        config1.set('font_size', 16)
        config1.set('mode', 'científico')
        config1.save_config()
        
        # Cargar en nueva instancia
        config2 = ConfigModel(temp_config_file)
        
        assert config2.get('font_size') == 16
        assert config2.get('mode') == 'científico'
    
    def test_auto_save(self, temp_config_file):
        """Test: auto-guardado de configuración."""
        config = ConfigModel(temp_config_file)
        config.set('auto_save', True)
        config.set('font_size', 18)
        
        # Cargar en nueva instancia
        config2 = ConfigModel(temp_config_file)
        
        assert config2.get('font_size') == 18
    
    def test_reset_to_defaults(self, temp_config_file):
        """Test: restaurar valores por defecto."""
        config = ConfigModel(temp_config_file)
        
        config.set('font_size', 20)
        config.set('mode', 'científico')
        
        config.reset_to_defaults()
        
        assert config.get('font_size') == 12
        assert config.get('mode') == 'básico'
    
    def test_reset_key(self, temp_config_file):
        """Test: restaurar clave específica."""
        config = ConfigModel(temp_config_file)
        
        config.set('font_size', 20)
        success = config.reset_key('font_size')
        
        assert success
        assert config.get('font_size') == 12
    
    def test_reset_invalid_key(self, temp_config_file):
        """Test: restaurar clave inválida."""
        config = ConfigModel(temp_config_file)
        
        success = config.reset_key('invalid_key')
        
        assert not success
    
    def test_theme_property(self, temp_config_file):
        """Test: propiedad theme."""
        config = ConfigModel(temp_config_file)
        
        assert config.theme == Theme.LIGHT
        
        config.theme = Theme.DARK
        assert config.theme == Theme.DARK
    
    def test_theme_property_from_string(self, temp_config_file):
        """Test: establecer theme desde string."""
        config = ConfigModel(temp_config_file)
        
        config.theme = "blue"
        assert config.theme == Theme.BLUE
    
    def test_get_theme_colors(self, temp_config_file):
        """Test: obtener colores de tema."""
        config = ConfigModel(temp_config_file)
        
        colors = config.get_theme_colors()
        
        assert isinstance(colors, dict)
        assert 'bg' in colors
        assert 'fg' in colors
        assert 'button_bg' in colors
    
    def test_get_theme_colors_specific(self, temp_config_file):
        """Test: obtener colores de tema específico."""
        config = ConfigModel(temp_config_file)
        
        colors = config.get_theme_colors(Theme.DARK)
        
        assert colors['bg'] == '#2B2B2B'
        assert colors['fg'] == '#FFFFFF'
    
    def test_font_size_property(self, temp_config_file):
        """Test: propiedad font_size."""
        config = ConfigModel(temp_config_file)
        
        config.font_size = 16
        assert config.font_size == 16
    
    def test_font_size_validation(self, temp_config_file):
        """Test: validación de font_size."""
        config = ConfigModel(temp_config_file)
        
        # Valores válidos
        config.font_size = 10
        assert config.font_size == 10
        
        # Valores inválidos (fuera de rango)
        config.font_size = 5  # Muy pequeño
        assert config.font_size == 10  # No cambia
        
        config.font_size = 30  # Muy grande
        assert config.font_size == 10  # No cambia
    
    def test_window_size_property(self, temp_config_file):
        """Test: propiedad window_size."""
        config = ConfigModel(temp_config_file)
        
        config.window_size = (800, 600)
        assert config.window_size == (800, 600)
    
    def test_window_position_property(self, temp_config_file):
        """Test: propiedad window_position."""
        config = ConfigModel(temp_config_file)
        
        assert config.window_position is None
        
        config.window_position = (100, 200)
        assert config.window_position == (100, 200)
        
        config.window_position = None
        assert config.window_position is None
    
    def test_mode_property(self, temp_config_file):
        """Test: propiedad mode."""
        config = ConfigModel(temp_config_file)
        
        config.mode = 'científico'
        assert config.mode == 'científico'
    
    def test_history_limit_property(self, temp_config_file):
        """Test: propiedad history_limit."""
        config = ConfigModel(temp_config_file)
        
        config.history_limit = 50
        assert config.history_limit == 50
    
    def test_history_limit_validation(self, temp_config_file):
        """Test: validación de history_limit."""
        config = ConfigModel(temp_config_file)
        
        config.history_limit = 0
        assert config.history_limit == 0
        
        # Valor negativo no se acepta
        config.history_limit = -10
        assert config.history_limit == 0  # No cambia
    
    def test_auto_save_property(self, temp_config_file):
        """Test: propiedad auto_save."""
        config = ConfigModel(temp_config_file)
        
        config.auto_save = False
        assert config.auto_save == False
        
        config.auto_save = True
        assert config.auto_save == True
    
    def test_to_dict(self, temp_config_file):
        """Test: exportar a diccionario."""
        config = ConfigModel(temp_config_file)
        
        config.set('font_size', 14)
        config.set('mode', 'científico')
        
        data = config.to_dict()
        
        assert isinstance(data, dict)
        assert data['font_size'] == 14
        assert data['mode'] == 'científico'
    
    def test_from_dict(self, temp_config_file):
        """Test: importar desde diccionario."""
        config = ConfigModel(temp_config_file)
        
        data = {
            'font_size': 18,
            'mode': 'científico',
            'theme': 'dark'
        }
        
        config.from_dict(data)
        
        assert config.get('font_size') == 18
        assert config.get('mode') == 'científico'
        assert config.get('theme') == 'dark'
    
    def test_from_dict_invalid_keys(self, temp_config_file):
        """Test: importar con claves inválidas."""
        config = ConfigModel(temp_config_file)
        
        data = {
            'font_size': 18,
            'invalid_key': 'value'
        }
        
        config.from_dict(data)
        
        assert config.get('font_size') == 18
        assert config.get('invalid_key') is None
    
    def test_str_representation(self, temp_config_file):
        """Test: representación en string."""
        config = ConfigModel(temp_config_file)
        
        str_repr = str(config)
        
        assert "ConfigModel" in str_repr
        assert "theme=" in str_repr
        assert "mode=" in str_repr
    
    def test_repr_representation(self, temp_config_file):
        """Test: representación técnica."""
        config = ConfigModel(temp_config_file)
        
        repr_str = repr(config)
        
        assert "ConfigModel" in repr_str
        assert "config_file" in repr_str
    
    def test_load_corrupted_config(self, temp_config_file):
        """Test: cargar configuración corrupta."""
        # Escribir JSON inválido
        with open(temp_config_file, 'w') as f:
            f.write("invalid json {")
        
        # Debe cargar valores por defecto
        config = ConfigModel(temp_config_file)
        
        assert config.get('font_size') == 12
        assert config.get('mode') == 'básico'
    
    def test_all_themes_have_colors(self, temp_config_file):
        """Test: todos los temas tienen colores definidos."""
        config = ConfigModel(temp_config_file)
        
        for theme in Theme:
            colors = config.get_theme_colors(theme)
            
            assert 'bg' in colors
            assert 'fg' in colors
            assert 'button_bg' in colors
            assert 'button_fg' in colors
            assert 'display_bg' in colors
            assert 'display_fg' in colors
    
    def test_config_persistence(self, temp_config_file):
        """Test: persistencia completa de configuración."""
        # Configurar múltiples valores
        config1 = ConfigModel(temp_config_file)
        config1.theme = Theme.DARK
        config1.font_size = 16
        config1.window_size = (800, 600)
        config1.window_position = (100, 100)
        config1.mode = 'científico'
        config1.history_limit = 50
        config1.save_config()
        
        # Cargar en nueva instancia
        config2 = ConfigModel(temp_config_file)
        
        assert config2.theme == Theme.DARK
        assert config2.font_size == 16
        assert config2.window_size == (800, 600)
        assert config2.window_position == (100, 100)
        assert config2.mode == 'científico'
        assert config2.history_limit == 50


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

# Made with Bob
