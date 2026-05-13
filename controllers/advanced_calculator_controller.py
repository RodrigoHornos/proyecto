#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controlador Avanzado de la Calculadora
Coordina la interacción entre todos los modelos y la vista avanzada
"""

from models import (
    CalculatorModel, MemoryModel, HistoryModel, 
    KeyboardModel, ConfigModel, Theme
)
from models.mode_model import ModeModel, CalculatorMode
from models.scientific_model import ScientificModel
from models.export_pdf_model import PDFExportModel
from models.export_excel_model import ExcelExportModel
from models.programmer_model import ProgrammerModel
from models.graphing_model import GraphingModel


class AdvancedCalculatorController:
    """
    Controlador avanzado que coordina todos los modelos y la vista avanzada
    Responsable de:
    - Manejar eventos de la vista avanzada
    - Actualizar todos los modelos según las acciones del usuario
    - Actualizar la vista según los cambios en los modelos
    - Coordinar cambios de modo
    - Gestionar historial, temas y exportación
    """
    
    def __init__(self, view):
        """
        Inicializa el controlador avanzado
        
        Args:
            view: Instancia de AdvancedCalculatorView
        """
        self.view = view
        
        # Inicializar todos los modelos
        self.calculator = CalculatorModel()
        self.memory = MemoryModel()
        self.history = HistoryModel()
        self.keyboard = KeyboardModel()
        self.config = ConfigModel()
        self.mode_model = ModeModel()
        self.scientific = ScientificModel()
        self.export_pdf = PDFExportModel()
        self.export_excel = ExcelExportModel()
        self.programmer = ProgrammerModel()
        self.graphing = GraphingModel()
        
        # Aplicar tema guardado (la configuración se carga automáticamente en __init__)
        theme = self.config.theme
        theme_colors = self.config.get_theme_colors(theme)
        self.view.apply_theme(theme_colors)
        
        # Conectar callbacks de la vista
        self._connect_view_callbacks()
        
        # Configurar atajos de teclado
        self._setup_keyboard_shortcuts()
        
        # Sincronizar vista con modelo inicial
        self._update_display()
        self._update_history_display()
    
    def _connect_view_callbacks(self):
        """Conecta los callbacks de la vista con los métodos del controlador"""
        # Callbacks básicos
        self.view.on_number_click = self.handle_number
        self.view.on_operator_click = self.handle_operator
        self.view.on_function_click = self.handle_function
        self.view.on_memory_click = self.handle_memory
        self.view.on_clear_click = self.handle_clear
        self.view.on_delete_click = self.handle_delete
        self.view.on_sign_click = self.handle_sign
        self.view.on_equals_click = self.handle_equals
        
        # Callbacks de menú
        self.view.on_export_pdf = self.handle_export_pdf
        self.view.on_export_excel = self.handle_export_excel
        self.view.on_clear_history = self.handle_clear_history
        self.view.on_theme_change = self.handle_change_theme
        self.view.on_mode_change = self.handle_mode_change
    
    def _setup_keyboard_shortcuts(self):
        """Configura los atajos de teclado"""
        # TODO: Implementar atajos de teclado completos
        # Por ahora, configurar solo los básicos
        self.view.root.bind('<Return>', lambda e: self.handle_equals())
        self.view.root.bind('<KP_Enter>', lambda e: self.handle_equals())
        self.view.root.bind('<Escape>', lambda e: self.handle_clear())
        self.view.root.bind('<BackSpace>', lambda e: self.handle_delete())
        
        # Números
        for i in range(10):
            self.view.root.bind(str(i), lambda e, n=i: self.handle_number(str(n)))
        
        # Operadores
        self.view.root.bind('+', lambda e: self.handle_operator('+'))
        self.view.root.bind('-', lambda e: self.handle_operator('-'))
        self.view.root.bind('*', lambda e: self.handle_operator('*'))
        self.view.root.bind('/', lambda e: self.handle_operator('/'))
        self.view.root.bind('.', lambda e: self.handle_number('.'))
    
    def _update_display(self):
        """Actualiza la pantalla con la expresión actual del modelo"""
        self.view.set_display(self.calculator.expression)
    
    def _update_history_display(self):
        """Actualiza el panel de historial"""
        entries = self.history.get_entries()
        history_text = []
        for entry in entries:
            history_text.append(f"{entry.expression} = {entry.result}")
        self.view.update_history(history_text)
    
    def handle_number(self, number):
        """
        Maneja la entrada de un número o punto decimal
        
        Args:
            number: Número o carácter a añadir
        """
        self.calculator.add_character(str(number))
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
        Maneja la aplicación de una función
        
        Args:
            function: Nombre de la función
        """
        current_mode = self.mode_model.current_mode
        
        # Funciones científicas
        if function in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                       'sqrt', 'pow', 'log', 'ln', 'exp', 'factorial']:
            success, result, error = self.calculator.apply_scientific_function(function)
            
            if success:
                self._update_display()
            else:
                self.view.show_error(error)
                self.calculator.clear()
        
        # Funciones de programación
        elif function in ['and', 'or', 'xor', 'not', 'lshift', 'rshift']:
            # Implementar operaciones bitwise
            pass
        
        # Constantes
        elif function in ['pi', 'e']:
            if function == 'pi':
                self.calculator.expression += 'π'
            elif function == 'e':
                self.calculator.expression += 'e'
            self._update_display()
    
    def handle_memory(self, operation):
        """
        Maneja las operaciones de memoria
        
        Args:
            operation: Operación de memoria (add, subtract, recall, clear)
        """
        if operation == 'clear':
            self.memory.clear()
            self.view.set_display("MC (0)")
            
        elif operation == 'recall':
            value = self.memory.recall()
            self.calculator.expression = str(value)
            self._update_display()
            
        elif operation in ['add', 'subtract']:
            success, value, error = self.calculator.get_expression_value()
            
            if success:
                if operation == 'add':
                    new_value = self.memory.add(value)
                    self.view.set_display(f"M+ ({new_value})")
                else:
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
        expression = self.calculator.expression
        success, result, error = self.calculator.calculate()
        
        if success:
            # Añadir al historial
            self.history.add_entry(expression, str(result))
            self._update_display()
            self._update_history_display()
        else:
            self.view.show_error(error)
            self.calculator.clear()
    
    def handle_export_pdf(self):
        """Maneja la exportación a PDF"""
        entries = self.history.get_entries()
        if not entries:
            self.view.show_error("No hay historial para exportar")
            return
        
        # Solicitar ruta de archivo
        filepath = self.view.ask_save_file("PDF", [("PDF files", "*.pdf")])
        if not filepath:
            return
        
        # Exportar
        success, message = self.export_pdf.export_history(entries, filepath)
        if success:
            self.view.show_info(f"Historial exportado a {filepath}")
        else:
            self.view.show_error(message)
    
    def handle_export_excel(self):
        """Maneja la exportación a Excel"""
        entries = self.history.get_entries()
        if not entries:
            self.view.show_error("No hay historial para exportar")
            return
        
        # Solicitar ruta de archivo
        filepath = self.view.ask_save_file("Excel", [("Excel files", "*.xlsx")])
        if not filepath:
            return
        
        # Exportar
        success, message = self.export_excel.export_history(entries, filepath)
        if success:
            self.view.show_info(f"Historial exportado a {filepath}")
        else:
            self.view.show_error(message)
    
    def handle_clear_history(self):
        """Maneja el borrado del historial"""
        self.history.clear()
        self._update_history_display()
        self.view.show_info("Historial borrado")
    
    def handle_change_theme(self, theme_name):
        """
        Maneja el cambio de tema
        
        Args:
            theme_name: Nombre del tema (light, dark, blue, green, purple, high_contrast)
        """
        # Mapear nombre a enum Theme
        theme_map = {
            'light': Theme.LIGHT,
            'dark': Theme.DARK,
            'blue': Theme.BLUE,
            'green': Theme.GREEN,
            'purple': Theme.PURPLE,
            'high_contrast': Theme.HIGH_CONTRAST
        }
        
        theme = theme_map.get(theme_name.lower(), Theme.LIGHT)
        
        # Actualizar configuración
        self.config.theme = theme
        
        # Aplicar tema en la vista
        theme_colors = self.config.get_theme_colors(theme)
        self.view.apply_theme(theme_colors)
    
    def handle_mode_change(self, mode_name):
        """
        Maneja el cambio de modo de calculadora
        
        Args:
            mode_name: Nombre del modo (basic, extended, scientific, programming, graphing)
        """
        # Mapear nombre a enum CalculatorMode
        mode_map = {
            'basic': CalculatorMode.BASIC,
            'extended': CalculatorMode.EXTENDED,
            'scientific': CalculatorMode.SCIENTIFIC,
            'programming': CalculatorMode.PROGRAMMER,
            'graphing': CalculatorMode.GRAPHING
        }
        
        mode = mode_map.get(mode_name, CalculatorMode.BASIC)
        
        # Cambiar modo en el modelo
        self.mode_model.set_mode(mode)
        
        # La vista ya se encarga de recrear los botones
        # Solo necesitamos actualizar el display
        self._update_display()
    
    def get_calculator_model(self):
        """Obtiene el modelo de la calculadora (útil para testing)"""
        return self.calculator
    
    def get_memory_model(self):
        """Obtiene el modelo de memoria (útil para testing)"""
        return self.memory
    
    def get_history_model(self):
        """Obtiene el modelo de historial (útil para testing)"""
        return self.history
    
    def get_config_model(self):
        """Obtiene el modelo de configuración (útil para testing)"""
        return self.config
    
    def get_mode_model(self):
        """Obtiene el modelo de modos (útil para testing)"""
        return self.mode_model

# Made with Bob