#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para operaciones básicas de la calculadora
"""

import pytest
import tkinter as tk
import sys
import os

# Añadir el directorio padre al path para importar calculadora
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculadora import Calculadora


class TestOperacionesBasicas:
    """Tests para operaciones aritméticas básicas"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora para cada test"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_suma_simple(self, calc):
        """Test suma de dos números positivos"""
        calc.expresion = "5+3"
        calc.calcular()
        assert calc.expresion == "8"
    
    def test_suma_negativos(self, calc):
        """Test suma con números negativos"""
        calc.expresion = "-5+3"
        calc.calcular()
        assert calc.expresion == "-2"
    
    def test_suma_decimales(self, calc):
        """Test suma con decimales"""
        calc.expresion = "5.5+3.2"
        calc.calcular()
        assert float(calc.expresion) == pytest.approx(8.7, rel=1e-9)
    
    def test_resta_simple(self, calc):
        """Test resta de dos números"""
        calc.expresion = "10-3"
        calc.calcular()
        assert calc.expresion == "7"
    
    def test_resta_resultado_negativo(self, calc):
        """Test resta con resultado negativo"""
        calc.expresion = "3-10"
        calc.calcular()
        assert calc.expresion == "-7"
    
    def test_multiplicacion_simple(self, calc):
        """Test multiplicación básica"""
        calc.expresion = "5*3"
        calc.calcular()
        assert calc.expresion == "15"
    
    def test_multiplicacion_por_cero(self, calc):
        """Test multiplicación por cero"""
        calc.expresion = "5*0"
        calc.calcular()
        assert calc.expresion == "0"
    
    def test_multiplicacion_negativos(self, calc):
        """Test multiplicación con negativos"""
        calc.expresion = "-5*3"
        calc.calcular()
        assert calc.expresion == "-15"
    
    def test_division_simple(self, calc):
        """Test división básica"""
        calc.expresion = "10/2"
        calc.calcular()
        # Con el nuevo parser, 10/2 = 5 (entero) no 5.0
        assert calc.expresion == "5"
    
    def test_division_con_decimales(self, calc):
        """Test división con resultado decimal"""
        calc.expresion = "10/3"
        calc.calcular()
        assert float(calc.expresion) == pytest.approx(3.333333, rel=1e-5)
    
    def test_division_por_cero(self, calc):
        """Test división por cero debe mostrar error"""
        calc.expresion = "10/0"
        calc.calcular()
        assert calc.entrada_texto.get() == "Error: Div/0"
        assert calc.expresion == ""
    
    def test_precedencia_operadores(self, calc):
        """Test precedencia de operadores (multiplicación antes que suma)"""
        calc.expresion = "2+3*4"
        calc.calcular()
        assert calc.expresion == "14"
    
    def test_precedencia_con_parentesis(self, calc):
        """Test precedencia con paréntesis"""
        calc.expresion = "(2+3)*4"
        calc.calcular()
        assert calc.expresion == "20"
    
    def test_operacion_compleja(self, calc):
        """Test operación compleja con múltiples operadores"""
        calc.expresion = "10+5*2-3/3"
        calc.calcular()
        assert float(calc.expresion) == pytest.approx(19.0, rel=1e-9)
    
    def test_numeros_muy_grandes(self, calc):
        """Test con números muy grandes"""
        calc.expresion = "999999999*999999999"
        calc.calcular()
        assert float(calc.expresion) == pytest.approx(999999998000000001, rel=1e-9)
    
    def test_numeros_muy_pequenos(self, calc):
        """Test con números muy pequeños"""
        calc.expresion = "0.0001*0.0001"
        calc.calcular()
        assert float(calc.expresion) == pytest.approx(0.00000001, rel=1e-9)


class TestFuncionesBasicas:
    """Tests para funciones básicas de la interfaz"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_agregar_caracter(self, calc):
        """Test agregar caracteres a la expresión"""
        calc.agregar_caracter('5')
        assert calc.expresion == "5"
        calc.agregar_caracter('+')
        assert calc.expresion == "5+"
        calc.agregar_caracter('3')
        assert calc.expresion == "5+3"
    
    def test_limpiar(self, calc):
        """Test función limpiar"""
        calc.expresion = "5+3"
        calc.entrada_texto.set("5+3")
        calc.limpiar()
        assert calc.expresion == ""
        assert calc.entrada_texto.get() == ""
    
    def test_borrar_entrada(self, calc):
        """Test función borrar último carácter"""
        calc.expresion = "5+3"
        calc.entrada_texto.set("5+3")
        calc.borrar_entrada()
        assert calc.expresion == "5+"
        calc.borrar_entrada()
        assert calc.expresion == "5"
    
    def test_cambiar_signo_positivo_a_negativo(self, calc):
        """Test cambiar signo de positivo a negativo"""
        calc.expresion = "5"
        calc.cambiar_signo()
        assert calc.expresion == "-5"
    
    def test_cambiar_signo_negativo_a_positivo(self, calc):
        """Test cambiar signo de negativo a positivo"""
        calc.expresion = "-5"
        calc.cambiar_signo()
        assert calc.expresion == "5"
    
    def test_cambiar_signo_expresion(self, calc):
        """Test cambiar signo de una expresión"""
        calc.expresion = "5+3"
        calc.cambiar_signo()
        assert calc.expresion == "-8"


class TestExpresionesInvalidas:
    """Tests para manejo de expresiones inválidas"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_expresion_vacia(self, calc):
        """Test calcular con expresión vacía"""
        calc.expresion = ""
        calc.calcular()
        assert calc.expresion == ""
    
    def test_expresion_invalida(self, calc):
        """Test expresión sintácticamente incorrecta"""
        calc.expresion = "5++"
        calc.calcular()
        assert calc.entrada_texto.get() == "Error"
        assert calc.expresion == ""
    
    def test_operador_sin_operando(self, calc):
        """Test operador sin segundo operando"""
        calc.expresion = "5+"
        calc.calcular()
        assert calc.entrada_texto.get() == "Error"
        assert calc.expresion == ""
    
    def test_parentesis_sin_cerrar(self, calc):
        """Test paréntesis sin cerrar"""
        calc.expresion = "(5+3"
        calc.calcular()
        assert calc.entrada_texto.get() == "Error"
        assert calc.expresion == ""

# Made with Bob
