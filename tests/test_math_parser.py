#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el módulo math_parser
Verifica que el parser matemático seguro funciona correctamente
"""

import pytest
import math
from math_parser import MathParser, safe_eval, get_parser


class TestMathParser:
    """Tests para la clase MathParser"""
    
    @pytest.fixture
    def parser(self):
        """Fixture que proporciona una instancia del parser"""
        return MathParser()
    
    # Tests de operaciones básicas
    def test_suma_simple(self, parser):
        """Test de suma básica"""
        assert parser.parse("2+2") == 4.0
    
    def test_resta_simple(self, parser):
        """Test de resta básica"""
        assert parser.parse("10-5") == 5.0
    
    def test_multiplicacion_simple(self, parser):
        """Test de multiplicación básica"""
        assert parser.parse("3*4") == 12.0
    
    def test_division_simple(self, parser):
        """Test de división básica"""
        assert parser.parse("15/3") == 5.0
    
    def test_potencia(self, parser):
        """Test de potenciación"""
        assert parser.parse("2**3") == 8.0
    
    # Tests de precedencia de operadores
    def test_precedencia_multiplicacion(self, parser):
        """Test de precedencia: multiplicación antes que suma"""
        assert parser.parse("2+3*4") == 14.0
    
    def test_precedencia_parentesis(self, parser):
        """Test de precedencia con paréntesis"""
        assert parser.parse("(2+3)*4") == 20.0
    
    def test_expresion_compleja(self, parser):
        """Test de expresión compleja con múltiples operadores"""
        result = parser.parse("(10+5)*2-3/3")
        assert abs(result - 29.0) < 0.0001
    
    # Tests de funciones matemáticas
    def test_raiz_cuadrada(self, parser):
        """Test de raíz cuadrada"""
        assert parser.parse("sqrt(16)") == 4.0
    
    def test_seno(self, parser):
        """Test de función seno"""
        result = parser.parse("sin(0)")
        assert abs(result - 0.0) < 0.0001
    
    def test_coseno(self, parser):
        """Test de función coseno"""
        result = parser.parse("cos(0)")
        assert abs(result - 1.0) < 0.0001
    
    def test_tangente(self, parser):
        """Test de función tangente"""
        result = parser.parse("tan(0)")
        assert abs(result - 0.0) < 0.0001
    
    def test_logaritmo(self, parser):
        """Test de logaritmo"""
        result = parser.parse("log(100)")
        assert abs(result - 2.0) < 0.0001
    
    # Tests de constantes matemáticas
    def test_constante_pi(self, parser):
        """Test de constante pi"""
        result = parser.parse("pi")
        assert abs(result - math.pi) < 0.0001
    
    def test_constante_e(self, parser):
        """Test de constante e"""
        result = parser.parse("e")
        assert abs(result - math.e) < 0.0001
    
    # Tests de manejo de errores
    def test_division_por_cero(self, parser):
        """Test de división por cero"""
        with pytest.raises(ZeroDivisionError):
            parser.parse("10/0")
    
    def test_expresion_vacia(self, parser):
        """Test de expresión vacía"""
        with pytest.raises(ValueError):
            parser.parse("")
    
    def test_expresion_invalida(self, parser):
        """Test de expresión con sintaxis inválida"""
        # Nota: sympy es más permisivo que eval() y acepta multiplicación implícita
        # Probamos con una expresión que realmente sea inválida
        with pytest.raises(ValueError):
            parser.parse(")(")  # Paréntesis mal formados
    
    def test_caracteres_no_permitidos(self, parser):
        """Test de expresión con caracteres no permitidos"""
        with pytest.raises(ValueError):
            parser.parse("import os")
    
    def test_codigo_malicioso_import(self, parser):
        """Test de rechazo de código malicioso con import"""
        with pytest.raises(ValueError):
            parser.parse("__import__('os')")
    
    def test_codigo_malicioso_exec(self, parser):
        """Test de rechazo de código malicioso con exec"""
        with pytest.raises(ValueError):
            parser.parse("exec('print(1)')")
    
    def test_codigo_malicioso_eval(self, parser):
        """Test de rechazo de código malicioso con eval"""
        with pytest.raises(ValueError):
            parser.parse("eval('1+1')")
    
    # Tests de validación de sintaxis
    def test_validacion_sintaxis_correcta(self, parser):
        """Test de validación de sintaxis correcta"""
        is_valid, msg = parser.validate_syntax("2+2")
        assert is_valid is True
    
    def test_validacion_sintaxis_incorrecta(self, parser):
        """Test de validación de sintaxis incorrecta"""
        # Usar una expresión que realmente sea inválida
        is_valid, msg = parser.validate_syntax(")(")
        assert is_valid is False
    
    def test_validacion_expresion_vacia(self, parser):
        """Test de validación de expresión vacía"""
        is_valid, msg = parser.validate_syntax("")
        assert is_valid is False
    
    # Tests de números decimales
    def test_numero_decimal(self, parser):
        """Test de número decimal"""
        assert parser.parse("3.14") == 3.14
    
    def test_operacion_con_decimales(self, parser):
        """Test de operación con decimales"""
        result = parser.parse("2.5*4")
        assert abs(result - 10.0) < 0.0001
    
    # Tests de números negativos
    def test_numero_negativo(self, parser):
        """Test de número negativo"""
        assert parser.parse("-5") == -5.0
    
    def test_operacion_con_negativos(self, parser):
        """Test de operación con números negativos"""
        assert parser.parse("-5+3") == -2.0
    
    # Tests de casos extremos
    def test_numero_muy_grande(self, parser):
        """Test de número muy grande"""
        result = parser.parse("10**10")
        assert result == 10000000000.0
    
    def test_numero_muy_pequeno(self, parser):
        """Test de número muy pequeño"""
        result = parser.parse("0.0001")
        assert abs(result - 0.0001) < 0.00001


class TestSafeEval:
    """Tests para la función safe_eval"""
    
    def test_safe_eval_suma(self):
        """Test de safe_eval con suma"""
        assert safe_eval("2+2") == 4.0
    
    def test_safe_eval_multiplicacion(self):
        """Test de safe_eval con multiplicación"""
        assert safe_eval("3*4") == 12.0
    
    def test_safe_eval_expresion_compleja(self):
        """Test de safe_eval con expresión compleja"""
        result = safe_eval("(10+5)*2")
        assert result == 30.0
    
    def test_safe_eval_error(self):
        """Test de safe_eval con error"""
        with pytest.raises(ValueError):
            safe_eval("import os")


class TestGetParser:
    """Tests para la función get_parser (singleton)"""
    
    def test_get_parser_singleton(self):
        """Test de que get_parser devuelve la misma instancia"""
        parser1 = get_parser()
        parser2 = get_parser()
        assert parser1 is parser2
    
    def test_get_parser_funcional(self):
        """Test de que el parser obtenido funciona correctamente"""
        parser = get_parser()
        assert parser.parse("2+2") == 4.0


class TestSeguridad:
    """Tests específicos de seguridad"""
    
    @pytest.fixture
    def parser(self):
        """Fixture que proporciona una instancia del parser"""
        return MathParser()
    
    def test_no_permite_import(self, parser):
        """Test de que no permite import"""
        with pytest.raises(ValueError):
            parser.parse("import sys")
    
    def test_no_permite_exec(self, parser):
        """Test de que no permite exec"""
        with pytest.raises(ValueError):
            parser.parse("exec('x=1')")
    
    def test_no_permite_eval_anidado(self, parser):
        """Test de que no permite eval anidado"""
        with pytest.raises(ValueError):
            parser.parse("eval('2+2')")
    
    def test_no_permite_open(self, parser):
        """Test de que no permite open"""
        with pytest.raises(ValueError):
            parser.parse("open('file.txt')")
    
    def test_no_permite_dunder_methods(self, parser):
        """Test de que no permite métodos dunder"""
        with pytest.raises(ValueError):
            parser.parse("__import__('os')")
    
    def test_solo_operaciones_matematicas(self, parser):
        """Test de que solo permite operaciones matemáticas"""
        # Estas deberían funcionar
        assert parser.parse("2+2") == 4.0
        assert parser.parse("sqrt(16)") == 4.0
        assert parser.parse("sin(0)") == 0.0
        
        # Estas no deberían funcionar
        with pytest.raises(ValueError):
            parser.parse("print('hello')")


class TestCompatibilidadConTests:
    """Tests para verificar compatibilidad con tests existentes"""
    
    def test_compatibilidad_operaciones_basicas(self):
        """Test de compatibilidad con operaciones básicas"""
        assert safe_eval("2+2") == 4.0
        assert safe_eval("10-5") == 5.0
        assert safe_eval("3*4") == 12.0
        assert safe_eval("15/3") == 5.0
    
    def test_compatibilidad_expresiones_complejas(self):
        """Test de compatibilidad con expresiones complejas"""
        assert safe_eval("2+3*4") == 14.0
        assert safe_eval("(2+3)*4") == 20.0
    
    def test_compatibilidad_manejo_errores(self):
        """Test de compatibilidad con manejo de errores"""
        with pytest.raises(ZeroDivisionError):
            safe_eval("10/0")
        
        with pytest.raises(ValueError):
            safe_eval("invalid expression")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
