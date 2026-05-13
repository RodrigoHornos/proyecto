#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista de la Calculadora
Maneja toda la interfaz gráfica usando Tkinter
"""

import tkinter as tk


class CalculatorView:
    """
    Vista que encapsula la interfaz gráfica de la calculadora
    Responsable de:
    - Crear y gestionar widgets de Tkinter
    - Mostrar información al usuario
    - Capturar eventos de usuario
    - Delegar lógica al controlador
    """
    
    def __init__(self, root):
        """
        Inicializa la vista de la calculadora
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Variable para el texto de entrada
        self.display_var = tk.StringVar()
        
        # Colores del tema
        self._setup_colors()
        
        # Crear componentes de la interfaz
        self._create_display()
        self._create_buttons()
        
        # Callbacks del controlador (se establecen después)
        self.on_number_click = None
        self.on_operator_click = None
        self.on_function_click = None
        self.on_memory_click = None
        self.on_clear_click = None
        self.on_delete_click = None
        self.on_sign_click = None
        self.on_equals_click = None
    
    def _setup_colors(self):
        """Configura los colores del tema"""
        self.root.configure(bg='#2C3E50')
        
        self.color_bg = '#2C3E50'
        self.color_display = '#34495E'
        self.color_number = '#ECF0F1'
        self.color_operator = '#3498DB'
        self.color_scientific = '#9B59B6'
        self.color_memory = '#E74C3C'
        self.color_special = '#F39C12'
        self.color_text_dark = '#2C3E50'
        self.color_text_light = '#FFFFFF'
    
    def _create_display(self):
        """Crea la pantalla de visualización"""
        frame = tk.Frame(self.root, bg=self.color_bg, pady=20)
        frame.pack(fill=tk.BOTH)
        
        display = tk.Entry(
            frame,
            textvariable=self.display_var,
            font=('Arial', 24, 'bold'),
            bg=self.color_display,
            fg=self.color_text_light,
            bd=0,
            justify='right',
            state='readonly'
        )
        display.pack(fill=tk.BOTH, padx=10, ipady=20)
    
    def _create_buttons(self):
        """Crea todos los botones de la calculadora"""
        frame = tk.Frame(self.root, bg=self.color_bg)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Definición de botones: (texto, color, callback_type, callback_arg, colspan)
        buttons = [
            # Fila 1: Memoria
            [
                ('MC', self.color_memory, 'memory', 'clear', 1),
                ('MR', self.color_memory, 'memory', 'recall', 1),
                ('M+', self.color_memory, 'memory', 'add', 1),
                ('M-', self.color_memory, 'memory', 'subtract', 1)
            ],
            # Fila 2: Funciones científicas
            [
                ('sin', self.color_scientific, 'function', 'sin', 1),
                ('cos', self.color_scientific, 'function', 'cos', 1),
                ('tan', self.color_scientific, 'function', 'tan', 1),
                ('√', self.color_scientific, 'function', 'sqrt', 1)
            ],
            # Fila 3: Más funciones y controles
            [
                ('x²', self.color_scientific, 'function', 'pow', 1),
                ('log', self.color_scientific, 'function', 'log', 1),
                ('C', self.color_special, 'clear', None, 1),
                ('CE', self.color_special, 'delete', None, 1)
            ],
            # Fila 4-7: Números y operadores
            [
                ('7', self.color_number, 'number', '7', 1),
                ('8', self.color_number, 'number', '8', 1),
                ('9', self.color_number, 'number', '9', 1),
                ('/', self.color_operator, 'operator', '/', 1)
            ],
            [
                ('4', self.color_number, 'number', '4', 1),
                ('5', self.color_number, 'number', '5', 1),
                ('6', self.color_number, 'number', '6', 1),
                ('*', self.color_operator, 'operator', '*', 1)
            ],
            [
                ('1', self.color_number, 'number', '1', 1),
                ('2', self.color_number, 'number', '2', 1),
                ('3', self.color_number, 'number', '3', 1),
                ('-', self.color_operator, 'operator', '-', 1)
            ],
            [
                ('0', self.color_number, 'number', '0', 1),
                ('.', self.color_number, 'number', '.', 1),
                ('+/-', self.color_special, 'sign', None, 1),
                ('+', self.color_operator, 'operator', '+', 1)
            ],
            # Fila 8: Igual
            [
                ('=', self.color_operator, 'equals', None, 4)
            ]
        ]
        
        # Crear botones
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_info in enumerate(row):
                text, color, callback_type, arg, colspan = btn_info
                
                # Determinar el comando según el tipo
                if callback_type == 'number':
                    cmd = lambda a=arg: self._handle_number(a)
                elif callback_type == 'operator':
                    cmd = lambda a=arg: self._handle_operator(a)
                elif callback_type == 'function':
                    cmd = lambda a=arg: self._handle_function(a)
                elif callback_type == 'memory':
                    cmd = lambda a=arg: self._handle_memory(a)
                elif callback_type == 'clear':
                    cmd = self._handle_clear
                elif callback_type == 'delete':
                    cmd = self._handle_delete
                elif callback_type == 'sign':
                    cmd = self._handle_sign
                elif callback_type == 'equals':
                    cmd = self._handle_equals
                else:
                    cmd = None
                
                btn = tk.Button(
                    frame,
                    text=text,
                    font=('Arial', 14, 'bold'),
                    bg=color,
                    fg=self.color_text_dark if color == self.color_number else self.color_text_light,
                    bd=0,
                    padx=10,
                    pady=10,
                    command=cmd,
                    cursor='hand2'
                )
                btn.grid(
                    row=row_idx,
                    column=col_idx,
                    columnspan=colspan,
                    sticky='nsew',
                    padx=2,
                    pady=2
                )
        
        # Configurar expansión de filas y columnas
        for i in range(8):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
    
    # Métodos para manejar eventos (delegan al controlador)
    
    def _handle_number(self, number):
        """Maneja clic en botón numérico"""
        if self.on_number_click:
            self.on_number_click(number)
    
    def _handle_operator(self, operator):
        """Maneja clic en botón de operador"""
        if self.on_operator_click:
            self.on_operator_click(operator)
    
    def _handle_function(self, function):
        """Maneja clic en botón de función científica"""
        if self.on_function_click:
            self.on_function_click(function)
    
    def _handle_memory(self, operation):
        """Maneja clic en botón de memoria"""
        if self.on_memory_click:
            self.on_memory_click(operation)
    
    def _handle_clear(self):
        """Maneja clic en botón limpiar"""
        if self.on_clear_click:
            self.on_clear_click()
    
    def _handle_delete(self):
        """Maneja clic en botón borrar"""
        if self.on_delete_click:
            self.on_delete_click()
    
    def _handle_sign(self):
        """Maneja clic en botón cambiar signo"""
        if self.on_sign_click:
            self.on_sign_click()
    
    def _handle_equals(self):
        """Maneja clic en botón igual"""
        if self.on_equals_click:
            self.on_equals_click()
    
    # Métodos públicos para actualizar la vista
    
    def set_display(self, text):
        """
        Actualiza el texto de la pantalla
        
        Args:
            text: Texto a mostrar
        """
        self.display_var.set(str(text))
    
    def get_display(self):
        """
        Obtiene el texto actual de la pantalla
        
        Returns:
            str: Texto de la pantalla
        """
        return self.display_var.get()
    
    def show_error(self, message):
        """
        Muestra un mensaje de error en la pantalla
        
        Args:
            message: Mensaje de error a mostrar
        """
        self.display_var.set(message)
    
    def clear_display(self):
        """Limpia la pantalla"""
        self.display_var.set("")

# Made with Bob
