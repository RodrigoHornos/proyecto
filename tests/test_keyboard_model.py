"""
Tests para el modelo de atajos de teclado (KeyboardModel y KeyAction).

Verifica el correcto funcionamiento del sistema de atajos incluyendo:
- Vinculación y desvinculación de teclas
- Atajos por defecto y personalizados
- Callbacks y triggers
- Exportación/importación
"""

import pytest
from models.keyboard_model import KeyboardModel, KeyAction


class TestKeyAction:
    """Tests para el enum KeyAction."""
    
    def test_key_action_values(self):
        """Test: valores del enum KeyAction."""
        assert KeyAction.NUMBER_0.value == "number_0"
        assert KeyAction.ADD.value == "add"
        assert KeyAction.CLEAR.value == "clear"
        assert KeyAction.SQRT.value == "sqrt"
    
    def test_key_action_from_value(self):
        """Test: crear KeyAction desde valor."""
        action = KeyAction("add")
        assert action == KeyAction.ADD
    
    def test_key_action_invalid_value(self):
        """Test: valor inválido lanza excepción."""
        with pytest.raises(ValueError):
            KeyAction("invalid_action")


class TestKeyboardModel:
    """Tests para la clase KeyboardModel."""
    
    def test_create_keyboard_model(self):
        """Test: crear modelo de teclado."""
        keyboard = KeyboardModel()
        
        assert keyboard.is_enabled()
        assert len(keyboard) > 0
        assert not keyboard.has_custom_bindings()
    
    def test_default_bindings(self):
        """Test: atajos por defecto."""
        keyboard = KeyboardModel()
        
        # Números
        assert keyboard.get_action('0') == KeyAction.NUMBER_0
        assert keyboard.get_action('5') == KeyAction.NUMBER_5
        assert keyboard.get_action('9') == KeyAction.NUMBER_9
        
        # Operadores
        assert keyboard.get_action('+') == KeyAction.ADD
        assert keyboard.get_action('-') == KeyAction.SUBTRACT
        assert keyboard.get_action('*') == KeyAction.MULTIPLY
        assert keyboard.get_action('/') == KeyAction.DIVIDE
        assert keyboard.get_action('=') == KeyAction.EQUALS
        
        # Funciones
        assert keyboard.get_action('<Escape>') == KeyAction.CLEAR
        assert keyboard.get_action('<BackSpace>') == KeyAction.DELETE
    
    def test_bind_key(self):
        """Test: vincular tecla a acción."""
        keyboard = KeyboardModel()
        
        success = keyboard.bind('x', KeyAction.MULTIPLY)
        
        assert success
        assert keyboard.get_action('x') == KeyAction.MULTIPLY
        assert keyboard.has_custom_bindings()
        assert keyboard.is_custom_binding('x')
    
    def test_bind_invalid_key(self):
        """Test: vincular tecla inválida."""
        keyboard = KeyboardModel()
        
        success = keyboard.bind('', KeyAction.ADD)
        
        assert not success
    
    def test_bind_invalid_action(self):
        """Test: vincular acción inválida."""
        keyboard = KeyboardModel()
        
        success = keyboard.bind('x', "invalid")
        
        assert not success
    
    def test_unbind_key(self):
        """Test: desvincular tecla."""
        keyboard = KeyboardModel()
        
        keyboard.bind('x', KeyAction.MULTIPLY)
        assert keyboard.get_action('x') == KeyAction.MULTIPLY
        
        success = keyboard.unbind('x')
        
        assert success
        assert keyboard.get_action('x') is None
        assert not keyboard.is_custom_binding('x')
    
    def test_unbind_default_key(self):
        """Test: desvincular tecla por defecto restaura el valor."""
        keyboard = KeyboardModel()
        
        # Cambiar atajo por defecto
        keyboard.bind('+', KeyAction.MULTIPLY)
        assert keyboard.get_action('+') == KeyAction.MULTIPLY
        
        # Desvincular restaura el valor por defecto
        keyboard.unbind('+')
        assert keyboard.get_action('+') == KeyAction.ADD
    
    def test_unbind_nonexistent_key(self):
        """Test: desvincular tecla inexistente."""
        keyboard = KeyboardModel()
        
        success = keyboard.unbind('nonexistent')
        
        assert not success
    
    def test_get_action_disabled(self):
        """Test: obtener acción cuando está deshabilitado."""
        keyboard = KeyboardModel()
        keyboard.disable()
        
        action = keyboard.get_action('+')
        
        assert action is None
    
    def test_get_key_for_action(self):
        """Test: obtener tecla para acción."""
        keyboard = KeyboardModel()
        
        key = keyboard.get_key_for_action(KeyAction.ADD)
        
        assert key == '+'
    
    def test_get_all_keys_for_action(self):
        """Test: obtener todas las teclas para una acción."""
        keyboard = KeyboardModel()
        
        keys = keyboard.get_all_keys_for_action(KeyAction.EQUALS)
        
        assert len(keys) >= 1
        assert '=' in keys
    
    def test_reset_to_defaults(self):
        """Test: restaurar atajos por defecto."""
        keyboard = KeyboardModel()
        
        # Añadir atajos personalizados
        keyboard.bind('x', KeyAction.MULTIPLY)
        keyboard.bind('y', KeyAction.DIVIDE)
        
        assert keyboard.has_custom_bindings()
        
        # Restaurar
        keyboard.reset_to_defaults()
        
        assert not keyboard.has_custom_bindings()
        assert keyboard.get_action('x') is None
        assert keyboard.get_action('+') == KeyAction.ADD
    
    def test_reset_key(self):
        """Test: restaurar tecla específica."""
        keyboard = KeyboardModel()
        
        # Cambiar atajo
        keyboard.bind('+', KeyAction.MULTIPLY)
        assert keyboard.get_action('+') == KeyAction.MULTIPLY
        
        # Restaurar
        success = keyboard.reset_key('+')
        
        assert success
        assert keyboard.get_action('+') == KeyAction.ADD
    
    def test_enable_disable(self):
        """Test: habilitar/deshabilitar atajos."""
        keyboard = KeyboardModel()
        
        assert keyboard.is_enabled()
        
        keyboard.disable()
        assert not keyboard.is_enabled()
        
        keyboard.enable()
        assert keyboard.is_enabled()
    
    def test_get_all_bindings(self):
        """Test: obtener todos los atajos."""
        keyboard = KeyboardModel()
        
        bindings = keyboard.get_all_bindings()
        
        assert isinstance(bindings, dict)
        assert len(bindings) > 0
        assert '+' in bindings
    
    def test_get_custom_bindings(self):
        """Test: obtener atajos personalizados."""
        keyboard = KeyboardModel()
        
        # Sin personalizaciones
        assert len(keyboard.get_custom_bindings()) == 0
        
        # Añadir personalización
        keyboard.bind('x', KeyAction.MULTIPLY)
        
        custom = keyboard.get_custom_bindings()
        assert len(custom) == 1
        assert 'x' in custom
    
    def test_get_bindings_by_category(self):
        """Test: obtener atajos por categoría."""
        keyboard = KeyboardModel()
        
        categories = keyboard.get_bindings_by_category()
        
        assert isinstance(categories, dict)
        assert 'Números' in categories
        assert 'Operadores' in categories
        assert 'Funciones Básicas' in categories
    
    def test_register_callback(self):
        """Test: registrar callback."""
        keyboard = KeyboardModel()
        called = []
        
        def callback():
            called.append(True)
        
        keyboard.register_callback(KeyAction.ADD, callback)
        keyboard.trigger_action(KeyAction.ADD)
        
        assert len(called) == 1
    
    def test_register_multiple_callbacks(self):
        """Test: registrar múltiples callbacks."""
        keyboard = KeyboardModel()
        calls = []
        
        def callback1():
            calls.append(1)
        
        def callback2():
            calls.append(2)
        
        keyboard.register_callback(KeyAction.ADD, callback1)
        keyboard.register_callback(KeyAction.ADD, callback2)
        keyboard.trigger_action(KeyAction.ADD)
        
        assert len(calls) == 2
        assert 1 in calls
        assert 2 in calls
    
    def test_unregister_callback(self):
        """Test: eliminar callback."""
        keyboard = KeyboardModel()
        called = []
        
        def callback():
            called.append(True)
        
        keyboard.register_callback(KeyAction.ADD, callback)
        success = keyboard.unregister_callback(KeyAction.ADD, callback)
        
        assert success
        
        keyboard.trigger_action(KeyAction.ADD)
        assert len(called) == 0
    
    def test_unregister_nonexistent_callback(self):
        """Test: eliminar callback inexistente."""
        keyboard = KeyboardModel()
        
        def callback():
            pass
        
        success = keyboard.unregister_callback(KeyAction.ADD, callback)
        
        assert not success
    
    def test_trigger_action_with_args(self):
        """Test: trigger con argumentos."""
        keyboard = KeyboardModel()
        received = []
        
        def callback(value, name="test"):
            received.append((value, name))
        
        keyboard.register_callback(KeyAction.ADD, callback)
        keyboard.trigger_action(KeyAction.ADD, 42, name="custom")
        
        assert len(received) == 1
        assert received[0] == (42, "custom")
    
    def test_to_dict(self):
        """Test: exportar a diccionario."""
        keyboard = KeyboardModel()
        
        keyboard.bind('x', KeyAction.MULTIPLY)
        keyboard.bind('y', KeyAction.DIVIDE)
        
        data = keyboard.to_dict()
        
        assert isinstance(data, dict)
        assert 'x' in data
        assert data['x'] == 'multiply'
        assert 'y' in data
        assert data['y'] == 'divide'
    
    def test_from_dict(self):
        """Test: importar desde diccionario."""
        keyboard = KeyboardModel()
        
        data = {
            'x': 'multiply',
            'y': 'divide',
            'z': 'add'
        }
        
        keyboard.from_dict(data)
        
        assert keyboard.get_action('x') == KeyAction.MULTIPLY
        assert keyboard.get_action('y') == KeyAction.DIVIDE
        assert keyboard.get_action('z') == KeyAction.ADD
    
    def test_from_dict_invalid_action(self):
        """Test: importar con acción inválida."""
        keyboard = KeyboardModel()
        
        data = {
            'x': 'invalid_action',
            'y': 'add'
        }
        
        keyboard.from_dict(data)
        
        # Acción inválida se ignora
        assert keyboard.get_action('x') is None
        # Acción válida se importa
        assert keyboard.get_action('y') == KeyAction.ADD
    
    def test_get_help_text(self):
        """Test: generar texto de ayuda."""
        keyboard = KeyboardModel()
        
        help_text = keyboard.get_help_text()
        
        assert isinstance(help_text, str)
        assert "Atajos de Teclado" in help_text
        assert "Números" in help_text
        assert "Operadores" in help_text
    
    def test_len(self):
        """Test: longitud del modelo."""
        keyboard = KeyboardModel()
        
        initial_len = len(keyboard)
        assert initial_len > 0
        
        keyboard.bind('x', KeyAction.MULTIPLY)
        assert len(keyboard) == initial_len + 1
    
    def test_contains(self):
        """Test: operador in."""
        keyboard = KeyboardModel()
        
        assert '+' in keyboard
        assert 'nonexistent' not in keyboard
        
        keyboard.bind('x', KeyAction.MULTIPLY)
        assert 'x' in keyboard
    
    def test_str_representation(self):
        """Test: representación en string."""
        keyboard = KeyboardModel()
        
        str_repr = str(keyboard)
        
        assert "KeyboardModel" in str_repr
        assert "atajos" in str_repr
        assert "habilitados" in str_repr
    
    def test_str_representation_disabled(self):
        """Test: representación cuando está deshabilitado."""
        keyboard = KeyboardModel()
        keyboard.disable()
        
        str_repr = str(keyboard)
        
        assert "deshabilitados" in str_repr
    
    def test_complex_key_combinations(self):
        """Test: combinaciones de teclas complejas."""
        keyboard = KeyboardModel()
        
        # Control+tecla
        assert keyboard.get_action('<Control-c>') == KeyAction.COPY
        assert keyboard.get_action('<Control-v>') == KeyAction.PASTE
        
        # Alt+tecla
        assert keyboard.get_action('<Alt-1>') == KeyAction.MODE_BASIC
    
    def test_multiple_keys_same_action(self):
        """Test: múltiples teclas para la misma acción."""
        keyboard = KeyboardModel()
        
        # Equals tiene múltiples atajos
        keys = keyboard.get_all_keys_for_action(KeyAction.EQUALS)
        
        assert len(keys) >= 2
        assert '=' in keys
        assert '<Return>' in keys
    
    def test_override_default_binding(self):
        """Test: sobrescribir atajo por defecto."""
        keyboard = KeyboardModel()
        
        # Cambiar '+' de ADD a MULTIPLY
        keyboard.bind('+', KeyAction.MULTIPLY)
        
        assert keyboard.get_action('+') == KeyAction.MULTIPLY
        assert keyboard.is_custom_binding('+')
        
        # Restaurar
        keyboard.reset_key('+')
        assert keyboard.get_action('+') == KeyAction.ADD
        assert not keyboard.is_custom_binding('+')
    
    def test_case_sensitive_keys(self):
        """Test: teclas sensibles a mayúsculas."""
        keyboard = KeyboardModel()
        
        # 'c' y 'C' son diferentes
        assert keyboard.get_action('c') == KeyAction.CLEAR
        assert keyboard.get_action('C') == KeyAction.CLEAR
        
        # Pero se pueden personalizar independientemente
        keyboard.bind('c', KeyAction.COPY)
        
        assert keyboard.get_action('c') == KeyAction.COPY
        assert keyboard.get_action('C') == KeyAction.CLEAR


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

# Made with Bob
