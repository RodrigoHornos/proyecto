#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista Avanzada de la Calculadora
Interfaz gráfica completa con menú, modos, historial y temas
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, Optional, Dict, List


class AdvancedCalculatorView:
    """
    Vista avanzada que incluye:
    - Menú superior (Archivo, Editar, Ver, Modos, Ayuda)
    - Selector de modos (Básico, Ampliado, Científico, Programación, Gráfico)
    - Panel de historial lateral
    - Sistema de temas
    - Atajos de teclado
    """
    
    def __init__(self, root):
        """
        Inicializa la vista avanzada
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("Calculadora Profesional")
        self.root.geometry("900x700")
        
        # Variables
        self.display_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="Científico")
        self.theme_var = tk.StringVar(value="Default")
        
        # Callbacks (se establecen desde el controlador)
        self.on_number_click = None
        self.on_operator_click = None
        self.on_function_click = None
        self.on_memory_click = None
        self.on_clear_click = None
        self.on_delete_click = None
        self.on_equals_click = None
        self.on_mode_change = None
        self.on_theme_change = None
        self.on_export_pdf = None
        self.on_export_excel = None
        self.on_clear_history = None
        
        # Colores del tema (se actualizan con apply_theme)
        self.colors = {}
        self._setup_default_colors()
        
        # Crear interfaz
        self._create_menu()
        self._create_main_layout()
        
    def _setup_default_colors(self):
        """Configura los colores por defecto"""
        self.colors = {
            'bg': '#2C3E50',
            'display': '#34495E',
            'number': '#ECF0F1',
            'operator': '#3498DB',
            'scientific': '#9B59B6',
            'memory': '#E74C3C',
            'special': '#F39C12',
            'text_dark': '#2C3E50',
            'text_light': '#FFFFFF',
            'history_bg': '#34495E',
            'history_fg': '#ECF0F1'
        }
    
    def _create_menu(self):
        """Crea el menú superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo cálculo", command=self._handle_clear)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar a PDF", command=self._handle_export_pdf)
        file_menu.add_command(label="Exportar a Excel", command=self._handle_export_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Limpiar", command=self._handle_clear)
        edit_menu.add_command(label="Borrar", command=self._handle_delete)
        edit_menu.add_separator()
        edit_menu.add_command(label="Limpiar historial", command=self._handle_clear_history)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        
        # Submenú de temas
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Tema", menu=theme_menu)
        # Usar los temas disponibles en ConfigModel
        themes = [
            ("Claro", "light"),
            ("Oscuro", "dark"),
            ("Azul", "blue"),
            ("Verde", "green"),
            ("Púrpura", "purple"),
            ("Alto Contraste", "high_contrast")
        ]
        for label, value in themes:
            theme_menu.add_radiobutton(
                label=label,
                variable=self.theme_var,
                value=value,
                command=lambda t=value: self._handle_theme_change(t)
            )
        
        # Menú Modos
        modes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modos", menu=modes_menu)
        modes = ["Básico", "Ampliado", "Científico", "Programación", "Gráfico"]
        for mode in modes:
            modes_menu.add_radiobutton(
                label=mode,
                variable=self.mode_var,
                value=mode,
                command=lambda m=mode: self._handle_mode_change(m)
            )
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Atajos de teclado", command=self._show_shortcuts)
        help_menu.add_command(label="Acerca de", command=self._show_about)
    
    def _create_main_layout(self):
        """Crea el layout principal con panel de historial"""
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda: Calculadora
        calc_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Selector de modo
        self._create_mode_selector(calc_frame)
        
        # Pantalla
        self._create_display(calc_frame)
        
        # Botones
        self.buttons_frame = tk.Frame(calc_frame, bg=self.colors['bg'])
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self._create_buttons()
        
        # Columna derecha: Historial
        self._create_history_panel(main_frame)
    
    def _create_mode_selector(self, parent):
        """Crea el selector de modos"""
        frame = tk.Frame(parent, bg=self.colors['bg'])
        frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame,
            text="Modo:",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        modes = ["Básico", "Ampliado", "Científico", "Programación", "Gráfico"]
        for mode in modes:
            btn = tk.Radiobutton(
                frame,
                text=mode,
                variable=self.mode_var,
                value=mode,
                font=('Arial', 9),
                bg=self.colors['bg'],
                fg=self.colors['text_light'],
                selectcolor=self.colors['operator'],
                command=lambda m=mode: self._handle_mode_change(m)
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def _create_display(self, parent):
        """Crea la pantalla de visualización"""
        frame = tk.Frame(parent, bg=self.colors['bg'])
        frame.pack(fill=tk.X, pady=(0, 10))
        
        self.display = tk.Entry(
            frame,
            textvariable=self.display_var,
            font=('Arial', 24, 'bold'),
            bg=self.colors['display'],
            fg=self.colors['text_light'],
            bd=0,
            justify='right',
            state='readonly'
        )
        self.display.pack(fill=tk.X, ipady=20)
    
    def _create_buttons(self):
        """Crea los botones según el modo actual"""
        # Limpiar botones existentes
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        mode = self.mode_var.get()
        
        if mode == "Básico":
            self._create_basic_buttons()
        elif mode == "Ampliado":
            self._create_extended_buttons()
        elif mode == "Científico":
            self._create_scientific_buttons()
        elif mode == "Programación":
            self._create_programmer_buttons()
        elif mode == "Gráfico":
            self._create_graphing_buttons()
    
    def _create_basic_buttons(self):
        """Crea botones para modo básico"""
        buttons = [
            # Fila 1
            [('C', 'special', 'clear'), ('CE', 'special', 'delete'), 
             ('%', 'operator', '%'), ('/', 'operator', '/')],
            # Fila 2
            [('7', 'number', '7'), ('8', 'number', '8'), 
             ('9', 'number', '9'), ('*', 'operator', '*')],
            # Fila 3
            [('4', 'number', '4'), ('5', 'number', '5'), 
             ('6', 'number', '6'), ('-', 'operator', '-')],
            # Fila 4
            [('1', 'number', '1'), ('2', 'number', '2'), 
             ('3', 'number', '3'), ('+', 'operator', '+')],
            # Fila 5
            [('0', 'number', '0'), ('.', 'number', '.'), 
             ('+/-', 'special', 'sign'), ('=', 'operator', '=')]
        ]
        self._create_button_grid(buttons)
    
    def _create_extended_buttons(self):
        """Crea botones para modo ampliado"""
        buttons = [
            # Fila 1: Memoria
            [('MC', 'memory', 'mc'), ('MR', 'memory', 'mr'), 
             ('M+', 'memory', 'm+'), ('M-', 'memory', 'm-')],
            # Fila 2: Funciones
            [('√', 'scientific', 'sqrt'), ('x²', 'scientific', 'pow'), 
             ('C', 'special', 'clear'), ('CE', 'special', 'delete')],
            # Filas 3-7: Números y operadores básicos
            [('7', 'number', '7'), ('8', 'number', '8'), 
             ('9', 'number', '9'), ('/', 'operator', '/')],
            [('4', 'number', '4'), ('5', 'number', '5'), 
             ('6', 'number', '6'), ('*', 'operator', '*')],
            [('1', 'number', '1'), ('2', 'number', '2'), 
             ('3', 'number', '3'), ('-', 'operator', '-')],
            [('0', 'number', '0'), ('.', 'number', '.'), 
             ('+/-', 'special', 'sign'), ('+', 'operator', '+')],
            [('=', 'operator', '=', 4)]
        ]
        self._create_button_grid(buttons)
    
    def _create_scientific_buttons(self):
        """Crea botones para modo científico"""
        buttons = [
            # Fila 1: Memoria
            [('MC', 'memory', 'mc'), ('MR', 'memory', 'mr'), 
             ('M+', 'memory', 'm+'), ('M-', 'memory', 'm-')],
            # Fila 2: Funciones trigonométricas
            [('sin', 'scientific', 'sin'), ('cos', 'scientific', 'cos'), 
             ('tan', 'scientific', 'tan'), ('√', 'scientific', 'sqrt')],
            # Fila 3: Más funciones
            [('x²', 'scientific', 'pow'), ('log', 'scientific', 'log'), 
             ('ln', 'scientific', 'ln'), ('π', 'scientific', 'pi')],
            # Fila 4: Controles
            [('C', 'special', 'clear'), ('CE', 'special', 'delete'), 
             ('(', 'operator', '('), (')', 'operator', ')')],
            # Filas 5-8: Números y operadores
            [('7', 'number', '7'), ('8', 'number', '8'), 
             ('9', 'number', '9'), ('/', 'operator', '/')],
            [('4', 'number', '4'), ('5', 'number', '5'), 
             ('6', 'number', '6'), ('*', 'operator', '*')],
            [('1', 'number', '1'), ('2', 'number', '2'), 
             ('3', 'number', '3'), ('-', 'operator', '-')],
            [('0', 'number', '0'), ('.', 'number', '.'), 
             ('+/-', 'special', 'sign'), ('+', 'operator', '+')],
            [('=', 'operator', '=', 4)]
        ]
        self._create_button_grid(buttons)
    
    def _create_programmer_buttons(self):
        """Crea botones para modo programación"""
        buttons = [
            # Fila 1: Bases
            [('BIN', 'special', 'bin'), ('OCT', 'special', 'oct'), 
             ('DEC', 'special', 'dec'), ('HEX', 'special', 'hex')],
            # Fila 2: Operaciones bit a bit
            [('AND', 'operator', 'and'), ('OR', 'operator', 'or'), 
             ('XOR', 'operator', 'xor'), ('NOT', 'operator', 'not')],
            # Fila 3: Shifts
            [('<<', 'operator', 'lshift'), ('>>', 'operator', 'rshift'), 
             ('C', 'special', 'clear'), ('CE', 'special', 'delete')],
            # Filas 4-7: Números hexadecimales
            [('D', 'number', 'D'), ('E', 'number', 'E'), 
             ('F', 'number', 'F'), ('/', 'operator', '/')],
            [('A', 'number', 'A'), ('B', 'number', 'B'), 
             ('C', 'number', 'C'), ('*', 'operator', '*')],
            [('7', 'number', '7'), ('8', 'number', '8'), 
             ('9', 'number', '9'), ('-', 'operator', '-')],
            [('4', 'number', '4'), ('5', 'number', '5'), 
             ('6', 'number', '6'), ('+', 'operator', '+')],
            [('1', 'number', '1'), ('2', 'number', '2'), 
             ('3', 'number', '3'), ('=', 'operator', '=')],
            [('0', 'number', '0', 4)]
        ]
        self._create_button_grid(buttons)
    
    def _create_graphing_buttons(self):
        """Crea botones para modo gráfico"""
        buttons = [
            # Fila 1: Funciones de graficación
            [('Graficar', 'special', 'graph'), ('Raíces', 'scientific', 'roots'), 
             ('Derivada', 'scientific', 'derivative'), ('Integral', 'scientific', 'integral')],
            # Fila 2: Análisis
            [('Extremos', 'scientific', 'extrema'), ('Límite', 'scientific', 'limit'), 
             ('C', 'special', 'clear'), ('CE', 'special', 'delete')],
            # Filas 3-6: Entrada de función
            [('x', 'number', 'x'), ('y', 'number', 'y'), 
             ('^', 'operator', '^'), ('/', 'operator', '/')],
            [('sin', 'scientific', 'sin'), ('cos', 'scientific', 'cos'), 
             ('tan', 'scientific', 'tan'), ('*', 'operator', '*')],
            [('(', 'operator', '('), (')', 'operator', ')'), 
             ('π', 'scientific', 'pi'), ('-', 'operator', '-')],
            [('e', 'scientific', 'e'), ('log', 'scientific', 'log'), 
             ('ln', 'scientific', 'ln'), ('+', 'operator', '+')],
            [('=', 'operator', '=', 4)]
        ]
        self._create_button_grid(buttons)
    
    def _create_button_grid(self, buttons):
        """
        Crea una cuadrícula de botones
        
        Args:
            buttons: Lista de filas, cada fila es una lista de tuplas (texto, tipo, valor, [colspan])
        """
        for row_idx, row in enumerate(buttons):
            col_idx = 0
            for btn_info in row:
                text = btn_info[0]
                btn_type = btn_info[1]
                value = btn_info[2]
                colspan = btn_info[3] if len(btn_info) > 3 else 1
                
                # Determinar color
                color = self.colors.get(btn_type, self.colors['number'])
                
                # Determinar comando
                if btn_type == 'number':
                    cmd = lambda v=value: self._handle_number(v)
                elif btn_type == 'operator':
                    if value == '=':
                        cmd = self._handle_equals
                    else:
                        cmd = lambda v=value: self._handle_operator(v)
                elif btn_type == 'scientific':
                    cmd = lambda v=value: self._handle_function(v)
                elif btn_type == 'memory':
                    cmd = lambda v=value: self._handle_memory(v)
                elif btn_type == 'special':
                    if value == 'clear':
                        cmd = self._handle_clear
                    elif value == 'delete':
                        cmd = self._handle_delete
                    elif value == 'sign':
                        cmd = lambda: self._handle_function('sign')
                    else:
                        cmd = lambda v=value: self._handle_function(v)
                else:
                    cmd = None
                
                btn = tk.Button(
                    self.buttons_frame,
                    text=text,
                    font=('Arial', 12, 'bold'),
                    bg=color,
                    fg=self.colors['text_dark'] if btn_type == 'number' else self.colors['text_light'],
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
                col_idx += colspan
        
        # Configurar expansión
        for i in range(len(buttons)):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
    
    def _create_history_panel(self, parent):
        """Crea el panel de historial lateral"""
        frame = tk.Frame(parent, bg=self.colors['history_bg'], width=250)
        frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 10), pady=10)
        frame.pack_propagate(False)
        
        # Título
        tk.Label(
            frame,
            text="Historial",
            font=('Arial', 14, 'bold'),
            bg=self.colors['history_bg'],
            fg=self.colors['history_fg']
        ).pack(pady=10)
        
        # Lista de historial con scrollbar
        scroll_frame = tk.Frame(frame, bg=self.colors['history_bg'])
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            scroll_frame,
            font=('Courier', 10),
            bg=self.colors['display'],
            fg=self.colors['history_fg'],
            bd=0,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Botón limpiar historial
        tk.Button(
            frame,
            text="Limpiar Historial",
            font=('Arial', 10),
            bg=self.colors['memory'],
            fg=self.colors['text_light'],
            bd=0,
            padx=10,
            pady=5,
            command=self._handle_clear_history,
            cursor='hand2'
        ).pack(pady=10)
    
    # Métodos de manejo de eventos
    
    def _handle_number(self, number):
        """Maneja clic en número"""
        if self.on_number_click:
            self.on_number_click(number)
    
    def _handle_operator(self, operator):
        """Maneja clic en operador"""
        if self.on_operator_click:
            self.on_operator_click(operator)
    
    def _handle_function(self, function):
        """Maneja clic en función"""
        if self.on_function_click:
            self.on_function_click(function)
    
    def _handle_memory(self, operation):
        """Maneja operación de memoria"""
        if self.on_memory_click:
            self.on_memory_click(operation)
    
    def _handle_clear(self):
        """Maneja limpiar"""
        if self.on_clear_click:
            self.on_clear_click()
    
    def _handle_delete(self):
        """Maneja borrar"""
        if self.on_delete_click:
            self.on_delete_click()
    
    def _handle_equals(self):
        """Maneja igual"""
        if self.on_equals_click:
            self.on_equals_click()
    
    def _handle_mode_change(self, mode):
        """Maneja cambio de modo"""
        self._create_buttons()  # Recrear botones
        if self.on_mode_change:
            self.on_mode_change(mode)
    
    def _handle_theme_change(self, theme):
        """Maneja cambio de tema"""
        if self.on_theme_change:
            self.on_theme_change(theme)
    
    def _handle_export_pdf(self):
        """Maneja exportación a PDF"""
        if self.on_export_pdf:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if filename:
                self.on_export_pdf(filename)
    
    def _handle_export_excel(self):
        """Maneja exportación a Excel"""
        if self.on_export_excel:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            if filename:
                self.on_export_excel(filename)
    
    def _handle_clear_history(self):
        """Maneja limpiar historial"""
        if self.on_clear_history:
            self.on_clear_history()
        self.history_listbox.delete(0, tk.END)
    
    def _show_shortcuts(self):
        """Muestra diálogo de atajos de teclado"""
        shortcuts = """
Atajos de Teclado:

Números: 0-9
Operadores: +, -, *, /
Igual: Enter o =
Limpiar: Escape
Borrar: Backspace
Punto decimal: .

Funciones:
s - sin
c - cos
t - tan
r - raíz cuadrada
p - potencia al cuadrado
l - logaritmo

Memoria:
Ctrl+M - M+
Ctrl+R - MR
Ctrl+L - MC
        """
        messagebox.showinfo("Atajos de Teclado", shortcuts)
    
    def _show_about(self):
        """Muestra diálogo Acerca de"""
        about_text = """
Calculadora Profesional v1.1

Una calculadora científica completa con:
- 5 modos de operación
- Sistema de historial
- Exportación a PDF y Excel
- Múltiples temas
- Atajos de teclado

Desarrollado con Python y Tkinter
        """
        messagebox.showinfo("Acerca de", about_text)
    
    # Métodos públicos para actualizar la vista
    
    def set_display(self, text):
        """Actualiza el texto de la pantalla"""
        self.display_var.set(str(text))
    
    def get_display(self):
        """Obtiene el texto de la pantalla"""
        return self.display_var.get()
    
    def show_error(self, message):
        """Muestra un error en la pantalla"""
        self.display_var.set(f"Error: {message}")
    
    def show_info(self, message):
        """Muestra un mensaje informativo"""
        from tkinter import messagebox
        messagebox.showinfo("Información", message)
    
    def ask_save_file(self, title, filetypes):
        """
        Solicita al usuario una ruta para guardar un archivo
        
        Args:
            title: Título del diálogo
            filetypes: Lista de tuplas (descripción, extensión)
            
        Returns:
            Ruta del archivo o None si se cancela
        """
        from tkinter import filedialog
        return filedialog.asksaveasfilename(
            title=title,
            filetypes=filetypes,
            defaultextension=filetypes[0][1] if filetypes else ""
        )
    
    def clear_display(self):
        """Limpia la pantalla"""
        self.display_var.set("")
    
    def add_to_history(self, entry):
        """
        Añade una entrada al historial
        
        Args:
            entry: Texto a añadir al historial
        """
        self.history_listbox.insert(0, entry)
    
    def clear_history(self):
        """Limpia el historial"""
        self.history_listbox.delete(0, tk.END)
    
    def update_history(self, entries: list):
        """
        Actualiza el historial completo
        
        Args:
            entries: Lista de entradas de historial
        """
        self.clear_history()
        for entry in reversed(entries):  # Invertir para mostrar más recientes primero
            self.history_listbox.insert(0, entry)
    
    def apply_theme(self, theme_colors: Dict[str, str]):
        """
        Aplica un tema de colores a toda la interfaz
        
        Args:
            theme_colors: Diccionario con los colores del tema
        """
        # Mapear colores del tema a los colores de la vista
        color_mapping = {
            'bg': 'bg',
            'fg': 'text_light',
            'button_bg': 'number',
            'button_fg': 'text_dark',
            'button_active': 'number',
            'display_bg': 'display',
            'display_fg': 'text_light',
            'operator_bg': 'operator',
            'operator_fg': 'text_light',
            'equals_bg': 'special',
            'equals_fg': 'text_light'
        }
        
        # Actualizar colores internos
        for theme_key, view_key in color_mapping.items():
            if theme_key in theme_colors:
                self.colors[view_key] = theme_colors[theme_key]
        
        # Aplicar colores recursivamente a todos los widgets
        self._apply_colors_recursive(self.root)
        
        # Recrear botones con nuevos colores
        self._create_buttons()
    
    def _apply_colors_recursive(self, widget):
        """
        Aplica colores recursivamente a un widget y sus hijos
        
        Args:
            widget: Widget de Tkinter
        """
        widget_type = widget.winfo_class()
        
        try:
            # Aplicar colores según el tipo de widget
            if widget_type in ['Frame', 'Toplevel']:
                widget.configure(bg=self.colors['bg'])
            
            elif widget_type == 'Label':
                widget.configure(
                    bg=self.colors['bg'],
                    fg=self.colors['text_light']
                )
            
            elif widget_type == 'Entry':
                # Es el display
                widget.configure(
                    bg=self.colors['display'],
                    fg=self.colors['text_light']
                )
            
            elif widget_type == 'Listbox':
                # Es el historial
                widget.configure(
                    bg=self.colors.get('display', '#34495E'),
                    fg=self.colors['text_light']
                )
            
            elif widget_type == 'Button':
                # Los botones se recrean, pero aplicamos color de fondo general
                widget.configure(bg=self.colors['number'])
            
            elif widget_type == 'Radiobutton':
                widget.configure(
                    bg=self.colors['bg'],
                    fg=self.colors['text_light'],
                    selectcolor=self.colors.get('operator', '#3498DB')
                )
        
        except tk.TclError:
            # Algunos widgets no soportan ciertas opciones
            pass
        
        # Aplicar recursivamente a los hijos
        for child in widget.winfo_children():
            self._apply_colors_recursive(child)


# Made with Bob