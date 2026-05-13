#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para funciones científicas de la calculadora
"""

import pytest
import tkinter as tk
import math
import sys
import os

# Añadir el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculadora import Calculadora


class TestFuncionesTrigonometricas:
    """Tests para funciones trigonométricas"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_sin_0(self, calc):
        """Test seno de 0 grados"""
        calc.expresion = "0"
        calc.funcion_cientifica('sin')
        assert float(calc.expresion) == pytest.approx(0.0, abs=1e-10)
    
    def test_sin_30(self, calc):
        """Test seno de 30 grados"""
        calc.expresion = "30"
        calc.funcion_cientifica('sin')
        assert float(calc.expresion) == pytest.approx(0.5, rel=1e-9)
    
    def test_sin_90(self, calc):
        """Test seno de 90 grados"""
        calc.expresion = "90"
        calc.funcion_cientifica('sin')
        assert float(calc.expresion) == pytest.approx(1.0, rel=1e-9)
    
    def test_cos_0(self, calc):
        """Test coseno de 0 grados"""
        calc.expresion = "0"
        calc.funcion_cientifica('cos')
        assert float(calc.expresion) == pytest.approx(1.0, rel=1e-9)
    
    def test_cos_60(self, calc):
        """Test coseno de 60 grados"""
        calc.expresion = "60"
        calc.funcion_cientifica('cos')
        assert float(calc.expresion) == pytest.approx(0.5, rel=1e-9)
    
    def test_cos_90(self, calc):
        """Test coseno de 90 grados"""
        calc.expresion = "90"
        calc.funcion_cientifica('cos')
        assert float(calc.expresion) == pytest.approx(0.0, abs=1e-10)
    
    def test_tan_0(self, calc):
        """Test tangente de 0 grados"""
        calc.expresion = "0"
        calc.funcion_cientifica('tan')
        assert float(calc.expresion) == pytest.approx(0.0, abs=1e-10)
    
    def test_tan_45(self, calc):
        """Test tangente de 45 grados"""
        calc.expresion = "45"
        calc.funcion_cientifica('tan')
        assert float(calc.expresion) == pytest.approx(1.0, rel=1e-9)
    
    def test_sin_negativo(self, calc):
        """Test seno de ángulo negativo"""
        calc.expresion = "-30"
        calc.funcion_cientifica('sin')
        assert float(calc.expresion) == pytest.approx(-0.5, rel=1e-9)


class TestFuncionesMatematicas:
    """Tests para otras funciones matemáticas"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_sqrt_4(self, calc):
        """Test raíz cuadrada de 4"""
        calc.expresion = "4"
        calc.funcion_cientifica('sqrt')
        assert float(calc.expresion) == pytest.approx(2.0, rel=1e-9)
    
    def test_sqrt_9(self, calc):
        """Test raíz cuadrada de 9"""
        calc.expresion = "9"
        calc.funcion_cientifica('sqrt')
        assert float(calc.expresion) == pytest.approx(3.0, rel=1e-9)
    
    def test_sqrt_2(self, calc):
        """Test raíz cuadrada de 2"""
        calc.expresion = "2"
        calc.funcion_cientifica('sqrt')
        assert float(calc.expresion) == pytest.approx(1.41421356, rel=1e-7)
    
    def test_sqrt_0(self, calc):
        """Test raíz cuadrada de 0"""
        calc.expresion = "0"
        calc.funcion_cientifica('sqrt')
        assert float(calc.expresion) == pytest.approx(0.0, abs=1e-10)
    
    def test_sqrt_negativo(self, calc):
        """Test raíz cuadrada de número negativo debe dar error"""
        calc.expresion = "-4"
        calc.funcion_cientifica('sqrt')
        assert calc.entrada_texto.get() == "Error: √ negativa"
        assert calc.expresion == ""
    
    def test_pow_2(self, calc):
        """Test potencia al cuadrado de 2"""
        calc.expresion = "2"
        calc.funcion_cientifica('pow')
        assert float(calc.expresion) == pytest.approx(4.0, rel=1e-9)
    
    def test_pow_5(self, calc):
        """Test potencia al cuadrado de 5"""
        calc.expresion = "5"
        calc.funcion_cientifica('pow')
        assert float(calc.expresion) == pytest.approx(25.0, rel=1e-9)
    
    def test_pow_negativo(self, calc):
        """Test potencia al cuadrado de número negativo"""
        calc.expresion = "-3"
        calc.funcion_cientifica('pow')
        assert float(calc.expresion) == pytest.approx(9.0, rel=1e-9)
    
    def test_pow_decimal(self, calc):
        """Test potencia al cuadrado de decimal"""
        calc.expresion = "2.5"
        calc.funcion_cientifica('pow')
        assert float(calc.expresion) == pytest.approx(6.25, rel=1e-9)
    
    def test_log_10(self, calc):
        """Test logaritmo base 10 de 10"""
        calc.expresion = "10"
        calc.funcion_cientifica('log')
        assert float(calc.expresion) == pytest.approx(1.0, rel=1e-9)
    
    def test_log_100(self, calc):
        """Test logaritmo base 10 de 100"""
        calc.expresion = "100"
        calc.funcion_cientifica('log')
        assert float(calc.expresion) == pytest.approx(2.0, rel=1e-9)
    
    def test_log_1(self, calc):
        """Test logaritmo base 10 de 1"""
        calc.expresion = "1"
        calc.funcion_cientifica('log')
        assert float(calc.expresion) == pytest.approx(0.0, abs=1e-10)
    
    def test_log_cero(self, calc):
        """Test logaritmo de 0 debe dar error"""
        calc.expresion = "0"
        calc.funcion_cientifica('log')
        assert calc.entrada_texto.get() == "Error: log ≤ 0"
        assert calc.expresion == ""
    
    def test_log_negativo(self, calc):
        """Test logaritmo de número negativo debe dar error"""
        calc.expresion = "-5"
        calc.funcion_cientifica('log')
        assert calc.entrada_texto.get() == "Error: log ≤ 0"
        assert calc.expresion == ""


class TestFuncionesCientificasConExpresiones:
    """Tests para funciones científicas aplicadas a expresiones"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_sqrt_de_suma(self, calc):
        """Test raíz cuadrada de una suma"""
        calc.expresion = "9+16"
        calc.funcion_cientifica('sqrt')
        assert float(calc.expresion) == pytest.approx(5.0, rel=1e-9)
    
    def test_sin_de_multiplicacion(self, calc):
        """Test seno de una multiplicación"""
        calc.expresion = "15*2"
        calc.funcion_cientifica('sin')
        # sin(30°) = 0.5
        assert float(calc.expresion) == pytest.approx(0.5, rel=1e-9)
    
    def test_pow_de_division(self, calc):
        """Test potencia de una división"""
        calc.expresion = "10/2"
        calc.funcion_cientifica('pow')
        assert float(calc.expresion) == pytest.approx(25.0, rel=1e-9)
    
    def test_funcion_sin_expresion(self, calc):
        """Test función científica sin expresión previa"""
        calc.expresion = ""
        calc.funcion_cientifica('sin')
        # No debe hacer nada si no hay expresión
        assert calc.expresion == ""

# Made with Bob
