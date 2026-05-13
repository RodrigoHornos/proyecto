"""
Tests para el modelo de modos de operación.
"""

import pytest
from models.mode_model import CalculatorMode, ModeModel


class TestCalculatorMode:
    """Tests para el enum CalculatorMode."""
    
    def test_mode_values(self):
        """Verifica que los modos tengan los valores correctos."""
        assert CalculatorMode.BASIC.value == "basic"
        assert CalculatorMode.EXTENDED.value == "extended"
        assert CalculatorMode.SCIENTIFIC.value == "scientific"
        assert CalculatorMode.PROGRAMMER.value == "programmer"
        assert CalculatorMode.GRAPHING.value == "graphing"
    
    def test_mode_from_value(self):
        """Verifica la creación de modos desde valores string."""
        assert CalculatorMode.from_value("basic") == CalculatorMode.BASIC
        assert CalculatorMode.from_value("extended") == CalculatorMode.EXTENDED
        assert CalculatorMode.from_value("scientific") == CalculatorMode.SCIENTIFIC
        assert CalculatorMode.from_value("BASIC") == CalculatorMode.BASIC  # Case insensitive
    
    def test_mode_invalid_value(self):
        """Verifica que se lance error con valores inválidos."""
        with pytest.raises(ValueError):
            CalculatorMode.from_value("invalid")


class TestModeModel:
    """Tests para el modelo de modos."""
    
    def test_create_mode_model_default(self):
        """Verifica la creación con modo por defecto."""
        model = ModeModel()
        assert model.current_mode == CalculatorMode.BASIC
        assert len(model.get_mode_history()) == 1
    
    def test_create_mode_model_with_mode(self):
        """Verifica la creación con modo específico."""
        model = ModeModel(CalculatorMode.SCIENTIFIC)
        assert model.current_mode == CalculatorMode.SCIENTIFIC
    
    def test_set_mode(self):
        """Verifica el cambio de modo."""
        model = ModeModel()
        model.set_mode(CalculatorMode.EXTENDED)
        assert model.current_mode == CalculatorMode.EXTENDED
    
    def test_set_mode_invalid_type(self):
        """Verifica que se lance error con tipo inválido."""
        model = ModeModel()
        with pytest.raises(TypeError):
            model.current_mode = "basic"
    
    def test_get_mode(self):
        """Verifica la obtención del modo actual."""
        model = ModeModel(CalculatorMode.SCIENTIFIC)
        assert model.get_mode() == CalculatorMode.SCIENTIFIC
    
    def test_mode_history(self):
        """Verifica el historial de cambios de modo."""
        model = ModeModel()
        model.set_mode(CalculatorMode.EXTENDED)
        model.set_mode(CalculatorMode.SCIENTIFIC)
        
        history = model.get_mode_history()
        assert len(history) == 3
        assert history[0] == CalculatorMode.BASIC
        assert history[1] == CalculatorMode.EXTENDED
        assert history[2] == CalculatorMode.SCIENTIFIC
    
    def test_clear_mode_history(self):
        """Verifica la limpieza del historial."""
        model = ModeModel()
        model.set_mode(CalculatorMode.EXTENDED)
        model.set_mode(CalculatorMode.SCIENTIFIC)
        
        model.clear_mode_history()
        history = model.get_mode_history()
        assert len(history) == 1
        assert history[0] == CalculatorMode.SCIENTIFIC
    
    def test_get_previous_mode(self):
        """Verifica la obtención del modo anterior."""
        model = ModeModel()
        model.set_mode(CalculatorMode.EXTENDED)
        
        previous = model.get_previous_mode()
        assert previous == CalculatorMode.BASIC
    
    def test_get_previous_mode_no_history(self):
        """Verifica que retorne None sin historial."""
        model = ModeModel()
        assert model.get_previous_mode() is None
    
    def test_switch_to_previous_mode(self):
        """Verifica el cambio al modo anterior."""
        model = ModeModel()
        model.set_mode(CalculatorMode.EXTENDED)
        model.set_mode(CalculatorMode.SCIENTIFIC)
        
        result = model.switch_to_previous_mode()
        assert result is True
        assert model.current_mode == CalculatorMode.EXTENDED
    
    def test_switch_to_previous_mode_no_history(self):
        """Verifica que retorne False sin historial."""
        model = ModeModel()
        result = model.switch_to_previous_mode()
        assert result is False
    
    def test_get_available_operations_basic(self):
        """Verifica las operaciones disponibles en modo básico."""
        model = ModeModel(CalculatorMode.BASIC)
        ops = model.get_available_operations()
        
        assert '+' in ops
        assert '-' in ops
        assert '*' in ops
        assert '/' in ops
        assert '0' in ops
        assert '9' in ops
        assert 'sqrt' not in ops  # No disponible en básico
    
    def test_get_available_operations_extended(self):
        """Verifica las operaciones disponibles en modo ampliado."""
        model = ModeModel(CalculatorMode.EXTENDED)
        ops = model.get_available_operations()
        
        assert '+' in ops
        assert 'sqrt' in ops
        assert 'sin' in ops
        assert 'cos' in ops
        assert 'π' in ops
        assert 'asin' not in ops  # No disponible en ampliado
    
    def test_get_available_operations_scientific(self):
        """Verifica las operaciones disponibles en modo científico."""
        model = ModeModel(CalculatorMode.SCIENTIFIC)
        ops = model.get_available_operations()
        
        assert '+' in ops
        assert 'sqrt' in ops
        assert 'sin' in ops
        assert 'asin' in ops
        assert 'sinh' in ops
        assert 'factorial' in ops
    
    def test_get_available_operations_programmer(self):
        """Verifica las operaciones disponibles en modo programador."""
        model = ModeModel(CalculatorMode.PROGRAMMER)
        ops = model.get_available_operations()
        
        assert '+' in ops
        assert 'AND' in ops
        assert 'OR' in ops
        assert 'XOR' in ops
        assert 'BIN' in ops
        assert 'HEX' in ops
    
    def test_get_available_operations_graphing(self):
        """Verifica las operaciones disponibles en modo gráfico."""
        model = ModeModel(CalculatorMode.GRAPHING)
        ops = model.get_available_operations()
        
        assert '+' in ops
        assert 'sin' in ops
        assert 'x' in ops
        assert 'y' in ops
        assert 'PLOT' in ops
    
    def test_get_available_operations_specific_mode(self):
        """Verifica obtener operaciones de un modo específico."""
        model = ModeModel(CalculatorMode.BASIC)
        ops = model.get_available_operations(CalculatorMode.SCIENTIFIC)
        
        assert 'asin' in ops  # Disponible en científico
    
    def test_is_operation_available(self):
        """Verifica si una operación está disponible."""
        model = ModeModel(CalculatorMode.BASIC)
        
        assert model.is_operation_available('+') is True
        assert model.is_operation_available('sqrt') is False
    
    def test_is_operation_available_specific_mode(self):
        """Verifica disponibilidad en modo específico."""
        model = ModeModel(CalculatorMode.BASIC)
        
        assert model.is_operation_available('sqrt', CalculatorMode.EXTENDED) is True
        assert model.is_operation_available('sqrt', CalculatorMode.BASIC) is False
    
    def test_get_mode_description(self):
        """Verifica la obtención de descripciones de modo."""
        model = ModeModel(CalculatorMode.BASIC)
        desc = model.get_mode_description()
        
        assert "básicas" in desc.lower()
        assert "+" in desc
    
    def test_get_mode_description_specific_mode(self):
        """Verifica descripción de modo específico."""
        model = ModeModel(CalculatorMode.BASIC)
        desc = model.get_mode_description(CalculatorMode.SCIENTIFIC)
        
        assert "científicas" in desc.lower() or "avanzadas" in desc.lower()
    
    def test_register_callback(self):
        """Verifica el registro de callbacks."""
        model = ModeModel()
        called = []
        
        def callback(old_mode, new_mode):
            called.append((old_mode, new_mode))
        
        model.register_callback("test", callback)
        model.set_mode(CalculatorMode.EXTENDED)
        
        assert len(called) == 1
        assert called[0] == (CalculatorMode.BASIC, CalculatorMode.EXTENDED)
    
    def test_register_multiple_callbacks(self):
        """Verifica el registro de múltiples callbacks."""
        model = ModeModel()
        called1 = []
        called2 = []
        
        def callback1(old_mode, new_mode):
            called1.append((old_mode, new_mode))
        
        def callback2(old_mode, new_mode):
            called2.append((old_mode, new_mode))
        
        model.register_callback("test1", callback1)
        model.register_callback("test2", callback2)
        model.set_mode(CalculatorMode.EXTENDED)
        
        assert len(called1) == 1
        assert len(called2) == 1
    
    def test_unregister_callback(self):
        """Verifica la eliminación de callbacks."""
        model = ModeModel()
        called = []
        
        def callback(old_mode, new_mode):
            called.append((old_mode, new_mode))
        
        model.register_callback("test", callback)
        result = model.unregister_callback("test")
        
        assert result is True
        
        model.set_mode(CalculatorMode.EXTENDED)
        assert len(called) == 0
    
    def test_unregister_nonexistent_callback(self):
        """Verifica eliminación de callback inexistente."""
        model = ModeModel()
        result = model.unregister_callback("nonexistent")
        assert result is False
    
    def test_callback_error_handling(self):
        """Verifica que errores en callbacks no interrumpan el flujo."""
        model = ModeModel()
        
        def bad_callback(old_mode, new_mode):
            raise Exception("Error en callback")
        
        model.register_callback("bad", bad_callback)
        
        # No debe lanzar excepción
        model.set_mode(CalculatorMode.EXTENDED)
        assert model.current_mode == CalculatorMode.EXTENDED
    
    def test_get_all_modes(self):
        """Verifica la obtención de todos los modos."""
        model = ModeModel()
        modes = model.get_all_modes()
        
        assert len(modes) == 5
        assert CalculatorMode.BASIC in modes
        assert CalculatorMode.EXTENDED in modes
        assert CalculatorMode.SCIENTIFIC in modes
        assert CalculatorMode.PROGRAMMER in modes
        assert CalculatorMode.GRAPHING in modes
    
    def test_to_dict(self):
        """Verifica la conversión a diccionario."""
        model = ModeModel(CalculatorMode.EXTENDED)
        model.set_mode(CalculatorMode.SCIENTIFIC)
        
        data = model.to_dict()
        
        assert data['current_mode'] == 'scientific'
        assert len(data['mode_history']) == 2
        assert data['mode_history'][0] == 'extended'
        assert data['mode_history'][1] == 'scientific'
    
    def test_from_dict(self):
        """Verifica la creación desde diccionario."""
        data = {
            'current_mode': 'scientific',
            'mode_history': ['basic', 'extended', 'scientific']
        }
        
        model = ModeModel.from_dict(data)
        
        assert model.current_mode == CalculatorMode.SCIENTIFIC
        assert len(model.get_mode_history()) == 3
    
    def test_from_dict_minimal(self):
        """Verifica creación desde diccionario mínimo."""
        data = {}
        model = ModeModel.from_dict(data)
        
        assert model.current_mode == CalculatorMode.BASIC
    
    def test_str_representation(self):
        """Verifica la representación en string."""
        model = ModeModel(CalculatorMode.EXTENDED)
        s = str(model)
        
        assert "ModeModel" in s
        assert "extended" in s
        assert "history_length" in s
    
    def test_repr_representation(self):
        """Verifica la representación detallada."""
        model = ModeModel(CalculatorMode.EXTENDED)
        r = repr(model)
        
        assert "ModeModel" in r
        assert "current_mode" in r
        assert "mode_history" in r
    
    def test_mode_operations_completeness(self):
        """Verifica que todos los modos tengan operaciones definidas."""
        model = ModeModel()
        
        for mode in CalculatorMode:
            ops = model.get_available_operations(mode)
            assert len(ops) > 0, f"Modo {mode} no tiene operaciones definidas"
    
    def test_mode_descriptions_completeness(self):
        """Verifica que todos los modos tengan descripción."""
        model = ModeModel()
        
        for mode in CalculatorMode:
            desc = model.get_mode_description(mode)
            assert len(desc) > 0, f"Modo {mode} no tiene descripción"
            assert desc != "Modo desconocido"
    
    def test_basic_mode_operations_subset(self):
        """Verifica que básico sea subconjunto de ampliado."""
        model = ModeModel()
        basic_ops = model.get_available_operations(CalculatorMode.BASIC)
        extended_ops = model.get_available_operations(CalculatorMode.EXTENDED)
        
        # Todas las operaciones básicas deben estar en ampliado
        # (excepto algunas específicas de memoria que pueden variar)
        common_ops = {'+', '-', '*', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}
        assert common_ops.issubset(basic_ops)
        assert common_ops.issubset(extended_ops)
    
    def test_extended_mode_operations_subset(self):
        """Verifica que ampliado sea subconjunto de científico."""
        model = ModeModel()
        extended_ops = model.get_available_operations(CalculatorMode.EXTENDED)
        scientific_ops = model.get_available_operations(CalculatorMode.SCIENTIFIC)
        
        # Operaciones científicas básicas deben estar en ambos
        common_ops = {'sqrt', 'sin', 'cos', 'tan', 'log'}
        assert common_ops.issubset(extended_ops)
        assert common_ops.issubset(scientific_ops)
    
    def test_mode_property_setter(self):
        """Verifica el setter de la propiedad current_mode."""
        model = ModeModel()
        model.current_mode = CalculatorMode.SCIENTIFIC
        
        assert model.current_mode == CalculatorMode.SCIENTIFIC
        assert len(model.get_mode_history()) == 2

# Made with Bob
