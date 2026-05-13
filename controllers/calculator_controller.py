#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controlador de la Calculadora
Coordina la interacción entre el modelo y la vista
"""

from models import CalculatorModel, MemoryModel


class CalculatorController:
    """
    Controlador que coordina el modelo y la vista
    Responsable de:
    - Manejar eventos de la vista
    - Actualizar el modelo según las acciones del usuario
    - Actualizar la vista según los cambios en el modelo
    - Implementar la lógica de flujo de la aplicación
    """
    
    def __init__(self, view):
        """
        Inicializa el controlador
        
        Args:
            view: Instancia de CalculatorView
        """
        self.view = view
        self.calculator = CalculatorModel()
        self.memory = MemoryModel()
        
        # Conectar callbacks de la vista
        self._connect_view_callbacks()
        
        # Sincronizar vista con modelo inicial
        self._update_display()
    
    def _connect_view_callbacks(self):
        """Conecta los callbacks de la vista con los métodos del controlador"""
        self.view.on_number_click = self.handle_number
        self.view.on_operator_click = self.handle_operator
        self.view.on_function_click = self.handle_function
        self.view.on_memory_click = self.handle_memory
        self.view.on_clear_click = self.handle_clear
        self.view.on_delete_click = self.handle_delete
        self.view.on_sign_click = self.handle_sign
        self.view.on_equals_click = self.handle_equals
    
    def _update_display(self):
        """Actualiza la pantalla con la expresión actual del modelo"""
        self.view.set_display(self.calculator.expression)
    
    def handle_number(self, number):
        """
        Maneja la entrada de un número o punto decimal
        
        Args:
            number: Número o carácter a añadir
        """
        self.calculator.add_character(number)
        self._update_display()
    
    def handle_operator(self, operator):
        """
        Maneja la entrada de un operador
        
        Args:
            operator: Operador matemático (+, -, *, /)
        """
        self.calculator.add_character(operator)
        self._update_display()
    
    def handle_function(self, function):
        """
        Maneja la aplicación de una función científica
        
        Args:
            function: Nombre de la función (sin, cos, tan, sqrt, pow, log)
        """
        success, result, error = self.calculator.apply_scientific_function(function)
        
        if success:
            self._update_display()
        else:
            self.view.show_error(error)
            self.calculator.clear()
    
    def handle_memory(self, operation):
        """
        Maneja las operaciones de memoria
        
        Args:
            operation: Operación de memoria (add, subtract, recall, clear)
        """
        if operation == 'clear':
            # MC: Limpiar memoria
            self.memory.clear()
            self.view.set_display(f"MC (0)")
            
        elif operation == 'recall':
            # MR: Recuperar memoria
            value = self.memory.recall()
            self.calculator.expression = str(value)
            self._update_display()
            
        elif operation in ['add', 'subtract']:
            # M+ o M-: Sumar o restar a memoria
            success, value, error = self.calculator.get_expression_value()
            
            if success:
                if operation == 'add':
                    new_value = self.memory.add(value)
                    self.view.set_display(f"M+ ({new_value})")
                else:  # subtract
                    new_value = self.memory.subtract(value)
                    self.view.set_display(f"M- ({new_value})")
            else:
                self.view.show_error(error)
    
    def handle_clear(self):
        """Maneja el botón de limpiar (C)"""
        self.calculator.clear()
        self._update_display()
    
    def handle_delete(self):
        """Maneja el botón de borrar último carácter (CE)"""
        self.calculator.delete_last()
        self._update_display()
    
    def handle_sign(self):
        """Maneja el botón de cambiar signo (+/-)"""
        success, result, error = self.calculator.change_sign()
        
        if success:
            self._update_display()
        else:
            if error:
                self.view.show_error(error)
    
    def handle_equals(self):
        """Maneja el botón de igual (=)"""
        success, result, error = self.calculator.calculate()
        
        if success:
            self._update_display()
        else:
            self.view.show_error(error)
            self.calculator.clear()
    
    def get_calculator_model(self):
        """
        Obtiene el modelo de la calculadora (útil para testing)
        
        Returns:
            CalculatorModel: Instancia del modelo
        """
        return self.calculator
    
    def get_memory_model(self):
        """
        Obtiene el modelo de memoria (útil para testing)
        
        Returns:
            MemoryModel: Instancia del modelo de memoria
        """
        return self.memory

# Made with Bob
