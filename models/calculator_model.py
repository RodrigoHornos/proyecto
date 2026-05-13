#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de la Calculadora
Contiene toda la lógica de cálculo y operaciones matemáticas
"""

import math
from math_parser import safe_eval


class CalculatorModel:
    """
    Modelo que encapsula la lógica de negocio de la calculadora
    Responsable de:
    - Gestión de la expresión actual
    - Evaluación de expresiones matemáticas
    - Aplicación de funciones científicas
    - Validación de operaciones
    """
    
    def __init__(self):
        """Inicializa el modelo de la calculadora"""
        self._expression = ""
        self._last_result = 0
    
    @property
    def expression(self):
        """Obtiene la expresión actual"""
        return self._expression
    
    @expression.setter
    def expression(self, value):
        """Establece la expresión actual"""
        self._expression = str(value) if value is not None else ""
    
    @property
    def last_result(self):
        """Obtiene el último resultado calculado"""
        return self._last_result
    
    def add_character(self, character):
        """
        Añade un carácter a la expresión
        
        Args:
            character: Carácter a añadir (número, operador, etc.)
        """
        self._expression += str(character)
    
    def clear(self):
        """Limpia la expresión actual"""
        self._expression = ""
    
    def delete_last(self):
        """Elimina el último carácter de la expresión"""
        if self._expression:
            self._expression = self._expression[:-1]
    
    def change_sign(self):
        """
        Cambia el signo del número o expresión actual
        
        Returns:
            tuple: (success: bool, result: str/float, error: str/None)
        """
        try:
            if not self._expression:
                return False, "", "No hay expresión"
            
            # Evaluar la expresión actual
            value = safe_eval(self._expression)
            result = -value
            
            # Formatear resultado
            if result == int(result):
                self._expression = str(int(result))
            else:
                self._expression = str(result)
            
            return True, self._expression, None
            
        except ValueError as e:
            return False, "", "Error de sintaxis"
        except Exception as e:
            return False, "", f"Error: {str(e)}"
    
    def calculate(self):
        """
        Calcula el resultado de la expresión actual
        
        Returns:
            tuple: (success: bool, result: str/float, error: str/None)
        """
        try:
            if not self._expression:
                return False, "", "No hay expresión"
            
            # Evaluar usando el parser seguro
            result = safe_eval(self._expression)
            self._last_result = result
            
            # Formatear resultado: enteros sin decimales
            if result == int(result):
                formatted_result = str(int(result))
            else:
                formatted_result = str(result)
            
            self._expression = formatted_result
            return True, formatted_result, None
            
        except ZeroDivisionError:
            return False, "", "Error: Div/0"
        except ValueError:
            return False, "", "Error: Sintaxis"
        except OverflowError:
            return False, "", "Error: Overflow"
        except Exception as e:
            return False, "", "Error"
    
    def apply_scientific_function(self, function_name):
        """
        Aplica una función científica al valor actual
        
        Args:
            function_name: Nombre de la función (sin, cos, tan, sqrt, pow, log)
        
        Returns:
            tuple: (success: bool, result: str/float, error: str/None)
        """
        try:
            if not self._expression:
                return False, "", "No hay expresión"
            
            # Evaluar la expresión actual
            value = float(safe_eval(self._expression))
            
            # Aplicar la función correspondiente
            if function_name == 'sin':
                result = math.sin(math.radians(value))
            elif function_name == 'cos':
                result = math.cos(math.radians(value))
            elif function_name == 'tan':
                result = math.tan(math.radians(value))
            elif function_name == 'sqrt':
                if value < 0:
                    return False, "", "Error: √ negativa"
                result = math.sqrt(value)
            elif function_name == 'pow':
                result = value ** 2
            elif function_name == 'log':
                if value <= 0:
                    return False, "", "Error: log ≤ 0"
                result = math.log10(value)
            else:
                return False, "", f"Función desconocida: {function_name}"
            
            self._expression = str(result)
            return True, str(result), None
            
        except ValueError:
            return False, "", "Error: Sintaxis"
        except Exception as e:
            return False, "", "Error"
    
    def get_expression_value(self):
        """
        Obtiene el valor numérico de la expresión actual sin modificarla
        
        Returns:
            tuple: (success: bool, value: float, error: str/None)
        """
        try:
            if not self._expression:
                return False, 0, "No hay expresión"
            
            value = float(safe_eval(self._expression))
            return True, value, None
            
        except ValueError:
            return False, 0, "Error: Sintaxis"
        except Exception as e:
            return False, 0, f"Error: {str(e)}"

# Made with Bob
