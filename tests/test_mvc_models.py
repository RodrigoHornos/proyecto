#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para los modelos de la arquitectura MVC
Verifica que los modelos funcionen correctamente de forma aislada
"""

import pytest
from models import CalculatorModel, MemoryModel


class TestCalculatorModel:
    """Tests para el modelo de la calculadora"""
    
    @pytest.fixture
    def model(self):
        """Fixture que proporciona una instancia del modelo"""
        return CalculatorModel()
    
    # Tests de gestión de expresión
    
    def test_initial_expression_empty(self, model):
        """Test de que la expresión inicial está vacía"""
        assert model.expression == ""
    
    def test_add_character(self, model):
        """Test de añadir caracteres"""
        model.add_character('5')
        assert model.expression == "5"
        model.add_character('+')
        assert model.expression == "5+"
        model.add_character('3')
        assert model.expression == "5+3"
    
    def test_clear(self, model):
        """Test de limpiar expresión"""
        model.expression = "5+3"
        model.clear()
        assert model.expression == ""
    
    def test_delete_last(self, model):
        """Test de borrar último carácter"""
        model.expression = "123"
        model.delete_last()
        assert model.expression == "12"
        model.delete_last()
        assert model.expression == "1"
        model.delete_last()
        assert model.expression == ""
    
    # Tests de cálculo
    
    def test_calculate_simple_sum(self, model):
        """Test de cálculo simple"""
        model.expression = "2+2"
        success, result, error = model.calculate()
        assert success is True
        assert result == "4"
        assert error is None
        assert model.expression == "4"
    
    def test_calculate_complex_expression(self, model):
        """Test de expresión compleja"""
        model.expression = "(10+5)*2"
        success, result, error = model.calculate()
        assert success is True
        assert result == "30"
        assert error is None
    
    def test_calculate_division_by_zero(self, model):
        """Test de división por cero"""
        model.expression = "10/0"
        success, result, error = model.calculate()
        assert success is False
        assert error == "Error: Div/0"
    
    def test_calculate_invalid_expression(self, model):
        """Test de expresión inválida"""
        model.expression = ")()"
        success, result, error = model.calculate()
        assert success is False
        assert error == "Error: Sintaxis"
    
    def test_calculate_empty_expression(self, model):
        """Test de expresión vacía"""
        model.expression = ""
        success, result, error = model.calculate()
        assert success is False
        assert error == "No hay expresión"
    
    # Tests de cambio de signo
    
    def test_change_sign_positive_to_negative(self, model):
        """Test de cambiar signo positivo a negativo"""
        model.expression = "5"
        success, result, error = model.change_sign()
        assert success is True
        assert model.expression == "-5"
    
    def test_change_sign_negative_to_positive(self, model):
        """Test de cambiar signo negativo a positivo"""
        model.expression = "-5"
        success, result, error = model.change_sign()
        assert success is True
        assert model.expression == "5"
    
    def test_change_sign_expression(self, model):
        """Test de cambiar signo de expresión"""
        model.expression = "3+5"
        success, result, error = model.change_sign()
        assert success is True
        assert model.expression == "-8"
    
    # Tests de funciones científicas
    
    def test_sqrt_function(self, model):
        """Test de raíz cuadrada"""
        model.expression = "16"
        success, result, error = model.apply_scientific_function('sqrt')
        assert success is True
        assert float(result) == 4.0
    
    def test_sqrt_negative(self, model):
        """Test de raíz cuadrada de número negativo"""
        model.expression = "-4"
        success, result, error = model.apply_scientific_function('sqrt')
        assert success is False
        assert error == "Error: √ negativa"
    
    def test_pow_function(self, model):
        """Test de potencia al cuadrado"""
        model.expression = "5"
        success, result, error = model.apply_scientific_function('pow')
        assert success is True
        assert float(result) == 25.0
    
    def test_log_function(self, model):
        """Test de logaritmo"""
        model.expression = "100"
        success, result, error = model.apply_scientific_function('log')
        assert success is True
        assert abs(float(result) - 2.0) < 0.0001
    
    def test_log_zero(self, model):
        """Test de logaritmo de cero"""
        model.expression = "0"
        success, result, error = model.apply_scientific_function('log')
        assert success is False
        assert error == "Error: log ≤ 0"
    
    def test_sin_function(self, model):
        """Test de seno"""
        model.expression = "0"
        success, result, error = model.apply_scientific_function('sin')
        assert success is True
        assert abs(float(result)) < 0.0001
    
    def test_cos_function(self, model):
        """Test de coseno"""
        model.expression = "0"
        success, result, error = model.apply_scientific_function('cos')
        assert success is True
        assert abs(float(result) - 1.0) < 0.0001
    
    def test_tan_function(self, model):
        """Test de tangente"""
        model.expression = "0"
        success, result, error = model.apply_scientific_function('tan')
        assert success is True
        assert abs(float(result)) < 0.0001
    
    # Tests de obtener valor
    
    def test_get_expression_value(self, model):
        """Test de obtener valor de expresión"""
        model.expression = "2+3"
        success, value, error = model.get_expression_value()
        assert success is True
        assert value == 5.0
        assert error is None
    
    def test_get_expression_value_empty(self, model):
        """Test de obtener valor de expresión vacía"""
        model.expression = ""
        success, value, error = model.get_expression_value()
        assert success is False
        assert value == 0
        assert error == "No hay expresión"


class TestMemoryModel:
    """Tests para el modelo de memoria"""
    
    @pytest.fixture
    def memory(self):
        """Fixture que proporciona una instancia del modelo de memoria"""
        return MemoryModel()
    
    def test_initial_value_zero(self, memory):
        """Test de que el valor inicial es cero"""
        assert memory.value == 0
    
    def test_add_value(self, memory):
        """Test de sumar valor a memoria"""
        result = memory.add(5)
        assert result == 5
        assert memory.value == 5
    
    def test_add_multiple_values(self, memory):
        """Test de sumar múltiples valores"""
        memory.add(5)
        memory.add(3)
        assert memory.value == 8
    
    def test_subtract_value(self, memory):
        """Test de restar valor de memoria"""
        memory.add(10)
        result = memory.subtract(3)
        assert result == 7
        assert memory.value == 7
    
    def test_recall_value(self, memory):
        """Test de recuperar valor de memoria"""
        memory.add(42)
        result = memory.recall()
        assert result == 42
        assert memory.value == 42  # No debe cambiar
    
    def test_clear_memory(self, memory):
        """Test de limpiar memoria"""
        memory.add(100)
        result = memory.clear()
        assert result == 0
        assert memory.value == 0
    
    def test_store_value(self, memory):
        """Test de almacenar valor directamente"""
        result = memory.store(25)
        assert result == 25
        assert memory.value == 25
    
    def test_store_replaces_value(self, memory):
        """Test de que store reemplaza el valor"""
        memory.add(10)
        memory.store(50)
        assert memory.value == 50
    
    def test_operations_with_decimals(self, memory):
        """Test de operaciones con decimales"""
        memory.add(2.5)
        memory.add(3.7)
        assert abs(memory.value - 6.2) < 0.0001
    
    def test_operations_with_negative(self, memory):
        """Test de operaciones con negativos"""
        memory.add(-5)
        assert memory.value == -5
        memory.subtract(-3)
        assert memory.value == -2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
