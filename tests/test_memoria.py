#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el sistema de memoria de la calculadora
"""

import pytest
import tkinter as tk
import sys
import os

# Añadir el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculadora import Calculadora


class TestSistemaMemoria:
    """Tests para las operaciones de memoria"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_memoria_inicial_cero(self, calc):
        """Test que la memoria inicia en 0"""
        assert calc.memoria == 0
    
    def test_memoria_sumar_positivo(self, calc):
        """Test sumar valor positivo a memoria"""
        calc.expresion = "5"
        calc.memoria_sumar()
        assert calc.memoria == 5.0
    
    def test_memoria_sumar_multiple(self, calc):
        """Test sumar múltiples valores a memoria"""
        calc.expresion = "5"
        calc.memoria_sumar()
        calc.expresion = "3"
        calc.memoria_sumar()
        assert calc.memoria == 8.0
    
    def test_memoria_sumar_negativo(self, calc):
        """Test sumar valor negativo a memoria"""
        calc.expresion = "-5"
        calc.memoria_sumar()
        assert calc.memoria == -5.0
    
    def test_memoria_sumar_decimal(self, calc):
        """Test sumar decimal a memoria"""
        calc.expresion = "2.5"
        calc.memoria_sumar()
        assert calc.memoria == pytest.approx(2.5, rel=1e-9)
    
    def test_memoria_restar_positivo(self, calc):
        """Test restar valor positivo de memoria"""
        calc.memoria = 10
        calc.expresion = "3"
        calc.memoria_restar()
        assert calc.memoria == 7.0
    
    def test_memoria_restar_multiple(self, calc):
        """Test restar múltiples valores de memoria"""
        calc.memoria = 10
        calc.expresion = "3"
        calc.memoria_restar()
        calc.expresion = "2"
        calc.memoria_restar()
        assert calc.memoria == 5.0
    
    def test_memoria_restar_negativo(self, calc):
        """Test restar valor negativo (suma) de memoria"""
        calc.memoria = 5
        calc.expresion = "-3"
        calc.memoria_restar()
        assert calc.memoria == 8.0
    
    def test_memoria_recuperar(self, calc):
        """Test recuperar valor de memoria"""
        calc.memoria = 42
        calc.memoria_recuperar()
        assert calc.expresion == "42"
        assert calc.entrada_texto.get() == "42"
    
    def test_memoria_recuperar_cero(self, calc):
        """Test recuperar memoria cuando está en 0"""
        calc.memoria = 0
        calc.memoria_recuperar()
        assert calc.expresion == "0"
    
    def test_memoria_recuperar_negativo(self, calc):
        """Test recuperar valor negativo de memoria"""
        calc.memoria = -15
        calc.memoria_recuperar()
        assert calc.expresion == "-15"
    
    def test_memoria_limpiar(self, calc):
        """Test limpiar memoria"""
        calc.memoria = 42
        calc.memoria_limpiar()
        assert calc.memoria == 0
        assert calc.entrada_texto.get() == "MC (0)"
    
    def test_memoria_operaciones_combinadas(self, calc):
        """Test combinación de operaciones de memoria"""
        # M+ 10
        calc.expresion = "10"
        calc.memoria_sumar()
        assert calc.memoria == 10.0
        
        # M+ 5
        calc.expresion = "5"
        calc.memoria_sumar()
        assert calc.memoria == 15.0
        
        # M- 3
        calc.expresion = "3"
        calc.memoria_restar()
        assert calc.memoria == 12.0
        
        # MR
        calc.memoria_recuperar()
        assert calc.expresion == "12.0"
        
        # MC
        calc.memoria_limpiar()
        assert calc.memoria == 0
    
    def test_memoria_con_expresion(self, calc):
        """Test memoria con expresión matemática"""
        calc.expresion = "5+3"
        calc.memoria_sumar()
        assert calc.memoria == 8.0
    
    def test_memoria_sin_expresion(self, calc):
        """Test operación de memoria sin expresión"""
        calc.expresion = ""
        calc.memoria_sumar()
        # No debe cambiar la memoria si no hay expresión
        assert calc.memoria == 0
    
    def test_memoria_persistencia_entre_calculos(self, calc):
        """Test que la memoria persiste entre cálculos"""
        # Guardar en memoria
        calc.expresion = "10"
        calc.memoria_sumar()
        
        # Hacer un cálculo diferente
        calc.expresion = "5+5"
        calc.calcular()
        
        # La memoria debe seguir siendo 10
        assert calc.memoria == 10.0
    
    def test_memoria_con_resultado_anterior(self, calc):
        """Test usar memoria después de un cálculo"""
        # Calcular algo
        calc.expresion = "5+5"
        calc.calcular()
        
        # Guardar resultado en memoria
        calc.memoria_sumar()
        assert calc.memoria == 10.0
        
        # Hacer otro cálculo
        calc.expresion = "3*3"
        calc.calcular()
        
        # Recuperar memoria
        calc.memoria_recuperar()
        assert calc.expresion == "10.0"


class TestMemoriaEdgeCases:
    """Tests para casos extremos del sistema de memoria"""
    
    @pytest.fixture
    def calc(self):
        """Fixture que crea una instancia de la calculadora"""
        root = tk.Tk()
        calculadora = Calculadora(root)
        yield calculadora
        root.destroy()
    
    def test_memoria_numero_muy_grande(self, calc):
        """Test memoria con número muy grande"""
        calc.expresion = "999999999"
        calc.memoria_sumar()
        assert calc.memoria == 999999999.0
    
    def test_memoria_numero_muy_pequeno(self, calc):
        """Test memoria con número muy pequeño"""
        calc.expresion = "0.0000001"
        calc.memoria_sumar()
        assert calc.memoria == pytest.approx(0.0000001, rel=1e-9)
    
    def test_memoria_overflow(self, calc):
        """Test memoria con operaciones que podrían causar overflow"""
        calc.expresion = "999999999"
        calc.memoria_sumar()
        calc.expresion = "999999999"
        calc.memoria_sumar()
        assert calc.memoria == 1999999998.0
    
    def test_memoria_precision_decimal(self, calc):
        """Test precisión decimal en memoria"""
        calc.expresion = "0.1"
        calc.memoria_sumar()
        calc.expresion = "0.2"
        calc.memoria_sumar()
        # 0.1 + 0.2 puede tener problemas de precisión
        assert calc.memoria == pytest.approx(0.3, rel=1e-9)

# Made with Bob
