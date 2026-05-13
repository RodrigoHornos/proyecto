#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser matemático seguro para la calculadora
Reemplaza eval() con sympy para mayor seguridad y control
"""

import sympy
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)
import math


class MathParser:
    """
    Parser matemático seguro que utiliza sympy para evaluar expresiones
    matemáticas sin los riesgos de seguridad de eval()
    """
    
    def __init__(self):
        """Inicializa el parser con las transformaciones necesarias"""
        # Transformaciones para parsing más flexible
        self.transformations = (
            standard_transformations +
            (implicit_multiplication_application, convert_xor)
        )
        
        # Símbolos permitidos para evaluación
        self.local_dict = {
            'pi': sympy.pi,
            'e': sympy.E,
            'sqrt': sympy.sqrt,
            'sin': sympy.sin,
            'cos': sympy.cos,
            'tan': sympy.tan,
            'log': lambda x: sympy.log(x, 10),  # log10 por defecto
            'ln': sympy.ln,
            'exp': sympy.exp,
            'abs': sympy.Abs,
        }
    
    def parse(self, expression):
        """
        Parsea y evalúa una expresión matemática de forma segura
        
        Args:
            expression (str): Expresión matemática a evaluar
            
        Returns:
            float: Resultado de la evaluación
            
        Raises:
            ValueError: Si la expresión no es válida
            ZeroDivisionError: Si hay división por cero
            OverflowError: Si el resultado es demasiado grande
        """
        if not expression or not isinstance(expression, str):
            raise ValueError("Expresión vacía o inválida")
        
        # Limpiar la expresión
        expression = expression.strip()
        
        # Validar caracteres permitidos
        if not self._validate_expression(expression):
            raise ValueError("Expresión contiene caracteres no permitidos")
        
        try:
            # Parsear la expresión con sympy
            parsed = parse_expr(
                expression,
                local_dict=self.local_dict,
                transformations=self.transformations,
                evaluate=True
            )
            
            # Evaluar numéricamente
            try:
                result = float(parsed.evalf())
            except (TypeError, ValueError) as e:
                # Manejar casos especiales como división por cero (que da zoo en sympy)
                if 'zoo' in str(parsed) or 'oo' in str(parsed):
                    raise ZeroDivisionError("División por cero")
                raise ValueError(f"No se puede convertir el resultado a número: {str(e)}")
            
            # Validar el resultado
            if math.isnan(result):
                raise ValueError("Resultado no es un número válido")
            if math.isinf(result):
                raise ZeroDivisionError("División por cero")
            
            # Formatear el resultado: si es entero, devolver como entero
            if result == int(result):
                return float(int(result))
            
            return result
            
        except sympy.SympifyError as e:
            raise ValueError(f"Error de sintaxis en la expresión: {str(e)}")
        except ZeroDivisionError:
            raise ZeroDivisionError("División por cero")
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión: {str(e)}")
    
    def _validate_expression(self, expression):
        """
        Valida que la expresión solo contenga caracteres permitidos
        
        Args:
            expression (str): Expresión a validar
            
        Returns:
            bool: True si la expresión es válida, False en caso contrario
        """
        # Caracteres permitidos: números, operadores, paréntesis, punto decimal
        # y letras para funciones matemáticas
        allowed_chars = set('0123456789+-*/().epi ')
        allowed_words = {'sin', 'cos', 'tan', 'sqrt', 'log', 'ln', 'exp', 'abs'}
        
        # Verificar caracteres individuales
        for char in expression:
            if char.isalpha():
                continue  # Las letras se verifican como palabras
            if char not in allowed_chars:
                return False
        
        # Verificar que las palabras sean funciones permitidas
        import re
        words = re.findall(r'[a-zA-Z]+', expression)
        for word in words:
            if word.lower() not in allowed_words and word not in ['e', 'pi']:
                return False
        
        return True
    
    def validate_syntax(self, expression):
        """
        Valida la sintaxis de una expresión sin evaluarla
        
        Args:
            expression (str): Expresión a validar
            
        Returns:
            tuple: (bool, str) - (es_válida, mensaje_error)
        """
        if not expression or not isinstance(expression, str):
            return False, "Expresión vacía o inválida"
        
        expression = expression.strip()
        
        if not self._validate_expression(expression):
            return False, "Expresión contiene caracteres no permitidos"
        
        try:
            parse_expr(
                expression,
                local_dict=self.local_dict,
                transformations=self.transformations,
                evaluate=False
            )
            return True, "Expresión válida"
        except Exception as e:
            return False, f"Error de sintaxis: {str(e)}"


# Instancia global del parser para uso en la calculadora
_parser_instance = None


def get_parser():
    """
    Obtiene la instancia singleton del parser
    
    Returns:
        MathParser: Instancia del parser matemático
    """
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = MathParser()
    return _parser_instance


def safe_eval(expression):
    """
    Función de conveniencia para evaluar expresiones de forma segura
    Reemplazo directo de eval() en el código existente
    
    Args:
        expression (str): Expresión matemática a evaluar
        
    Returns:
        float: Resultado de la evaluación
        
    Raises:
        ValueError: Si la expresión no es válida
        ZeroDivisionError: Si hay división por cero
    """
    parser = get_parser()
    return parser.parse(expression)


# Ejemplos de uso y tests básicos
if __name__ == "__main__":
    parser = MathParser()
    
    # Tests básicos
    test_cases = [
        ("2+2", 4.0),
        ("10-5", 5.0),
        ("3*4", 12.0),
        ("15/3", 5.0),
        ("2**3", 8.0),
        ("sqrt(16)", 4.0),
        ("sin(0)", 0.0),
        ("2+3*4", 14.0),
        ("(2+3)*4", 20.0),
        ("pi", 3.141592653589793),
    ]
    
    print("Ejecutando tests del parser...")
    for expr, expected in test_cases:
        try:
            result = parser.parse(expr)
            status = "✓" if abs(result - expected) < 0.0001 else "✗"
            print(f"{status} {expr} = {result} (esperado: {expected})")
        except Exception as e:
            print(f"✗ {expr} - Error: {e}")
    
    # Test de validación
    print("\nTests de validación:")
    invalid_cases = [
        "import os",
        "__import__('os')",
        "exec('print(1)')",
        "eval('1+1')",
    ]
    
    for expr in invalid_cases:
        is_valid, msg = parser.validate_syntax(expr)
        status = "✓" if not is_valid else "✗"
        print(f"{status} '{expr}' rechazada: {msg}")

# Made with Bob
