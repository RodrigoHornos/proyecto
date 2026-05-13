#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora GUI con Tkinter
Incluye operaciones básicas, funciones científicas y sistema de memoria
"""

import tkinter as tk
from tkinter import ttk
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Variables
        self.expresion = ""
        self.entrada_texto = tk.StringVar()
        self.memoria = 0
        self.resultado_anterior = 0
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_pantalla()
        self.crear_botones()
        
    def configurar_estilo(self):
        """Configura los colores y estilos de la calculadora"""
        self.root.configure(bg='#2C3E50')
        
        # Colores
        self.color_fondo = '#2C3E50'
        self.color_pantalla = '#34495E'
        self.color_boton_numero = '#ECF0F1'
        self.color_boton_operacion = '#3498DB'
        self.color_boton_cientifico = '#9B59B6'
        self.color_boton_memoria = '#E74C3C'
        self.color_boton_especial = '#F39C12'
        self.color_texto = '#2C3E50'
        self.color_texto_claro = '#FFFFFF'
        
    def crear_pantalla(self):
        """Crea la pantalla de visualización"""
        frame_pantalla = tk.Frame(self.root, bg=self.color_fondo, pady=20)
        frame_pantalla.pack(fill=tk.BOTH)
        
        # Pantalla de entrada
        pantalla = tk.Entry(
            frame_pantalla,
            textvariable=self.entrada_texto,
            font=('Arial', 24, 'bold'),
            bg=self.color_pantalla,
            fg=self.color_texto_claro,
            bd=0,
            justify='right',
            state='readonly'
        )
        pantalla.pack(fill=tk.BOTH, padx=10, ipady=20)
        
    def crear_botones(self):
        """Crea todos los botones de la calculadora"""
        frame_botones = tk.Frame(self.root, bg=self.color_fondo)
        frame_botones.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Definición de botones por filas
        botones = [
            # Fila 1: Memoria y funciones especiales
            [
                ('MC', self.color_boton_memoria, self.memoria_limpiar),
                ('MR', self.color_boton_memoria, self.memoria_recuperar),
                ('M+', self.color_boton_memoria, self.memoria_sumar),
                ('M-', self.color_boton_memoria, self.memoria_restar)
            ],
            # Fila 2: Funciones científicas
            [
                ('sin', self.color_boton_cientifico, lambda: self.funcion_cientifica('sin')),
                ('cos', self.color_boton_cientifico, lambda: self.funcion_cientifica('cos')),
                ('tan', self.color_boton_cientifico, lambda: self.funcion_cientifica('tan')),
                ('√', self.color_boton_cientifico, lambda: self.funcion_cientifica('sqrt'))
            ],
            # Fila 3: Más funciones científicas y operaciones
            [
                ('x²', self.color_boton_cientifico, lambda: self.funcion_cientifica('pow')),
                ('log', self.color_boton_cientifico, lambda: self.funcion_cientifica('log')),
                ('C', self.color_boton_especial, self.limpiar),
                ('CE', self.color_boton_especial, self.borrar_entrada)
            ],
            # Fila 4: Números y operaciones
            [
                ('7', self.color_boton_numero, lambda: self.agregar_caracter('7')),
                ('8', self.color_boton_numero, lambda: self.agregar_caracter('8')),
                ('9', self.color_boton_numero, lambda: self.agregar_caracter('9')),
                ('/', self.color_boton_operacion, lambda: self.agregar_caracter('/'))
            ],
            # Fila 5
            [
                ('4', self.color_boton_numero, lambda: self.agregar_caracter('4')),
                ('5', self.color_boton_numero, lambda: self.agregar_caracter('5')),
                ('6', self.color_boton_numero, lambda: self.agregar_caracter('6')),
                ('*', self.color_boton_operacion, lambda: self.agregar_caracter('*'))
            ],
            # Fila 6
            [
                ('1', self.color_boton_numero, lambda: self.agregar_caracter('1')),
                ('2', self.color_boton_numero, lambda: self.agregar_caracter('2')),
                ('3', self.color_boton_numero, lambda: self.agregar_caracter('3')),
                ('-', self.color_boton_operacion, lambda: self.agregar_caracter('-'))
            ],
            # Fila 7
            [
                ('0', self.color_boton_numero, lambda: self.agregar_caracter('0')),
                ('.', self.color_boton_numero, lambda: self.agregar_caracter('.')),
                ('+/-', self.color_boton_especial, self.cambiar_signo),
                ('+', self.color_boton_operacion, lambda: self.agregar_caracter('+'))
            ],
            # Fila 8
            [
                ('=', self.color_boton_operacion, self.calcular, 4)
            ]
        ]
        
        # Crear botones
        for fila_idx, fila in enumerate(botones):
            for col_idx, boton_info in enumerate(fila):
                if len(boton_info) == 4:  # Botón con colspan
                    texto, color, comando, colspan = boton_info
                else:
                    texto, color, comando = boton_info
                    colspan = 1
                
                btn = tk.Button(
                    frame_botones,
                    text=texto,
                    font=('Arial', 14, 'bold'),
                    bg=color,
                    fg=self.color_texto if color == self.color_boton_numero else self.color_texto_claro,
                    bd=0,
                    padx=10,
                    pady=10,
                    command=comando,
                    cursor='hand2'
                )
                btn.grid(
                    row=fila_idx,
                    column=col_idx,
                    columnspan=colspan,
                    sticky='nsew',
                    padx=2,
                    pady=2
                )
        
        # Configurar peso de filas y columnas para expansión
        for i in range(8):
            frame_botones.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame_botones.grid_columnconfigure(i, weight=1)
    
    def agregar_caracter(self, caracter):
        """Agrega un carácter a la expresión"""
        self.expresion += str(caracter)
        self.entrada_texto.set(self.expresion)
    
    def limpiar(self):
        """Limpia toda la expresión"""
        self.expresion = ""
        self.entrada_texto.set("")
    
    def borrar_entrada(self):
        """Borra el último carácter"""
        self.expresion = self.expresion[:-1]
        self.entrada_texto.set(self.expresion)
    
    def cambiar_signo(self):
        """Cambia el signo del número actual"""
        try:
            if self.expresion:
                # Si hay una expresión, evaluar y cambiar signo
                valor = eval(self.expresion)
                self.expresion = str(-valor)
                self.entrada_texto.set(self.expresion)
        except:
            self.entrada_texto.set("Error")
    
    def calcular(self):
        """Calcula el resultado de la expresión"""
        try:
            if self.expresion:
                resultado = eval(self.expresion)
                self.resultado_anterior = resultado
                self.entrada_texto.set(str(resultado))
                self.expresion = str(resultado)
        except ZeroDivisionError:
            self.entrada_texto.set("Error: Div/0")
            self.expresion = ""
        except Exception as e:
            self.entrada_texto.set("Error")
            self.expresion = ""
    
    def funcion_cientifica(self, funcion):
        """Aplica una función científica al valor actual"""
        try:
            if self.expresion:
                valor = float(eval(self.expresion))
                resultado = 0  # Inicializar resultado
                
                if funcion == 'sin':
                    resultado = math.sin(math.radians(valor))
                elif funcion == 'cos':
                    resultado = math.cos(math.radians(valor))
                elif funcion == 'tan':
                    resultado = math.tan(math.radians(valor))
                elif funcion == 'sqrt':
                    if valor < 0:
                        self.entrada_texto.set("Error: √ negativa")
                        self.expresion = ""
                        return
                    resultado = math.sqrt(valor)
                elif funcion == 'pow':
                    resultado = valor ** 2
                elif funcion == 'log':
                    if valor <= 0:
                        self.entrada_texto.set("Error: log ≤ 0")
                        self.expresion = ""
                        return
                    resultado = math.log10(valor)
                
                self.expresion = str(resultado)
                self.entrada_texto.set(self.expresion)
        except Exception as e:
            self.entrada_texto.set("Error")
            self.expresion = ""
    
    def memoria_sumar(self):
        """Suma el valor actual a la memoria"""
        try:
            if self.expresion:
                valor = float(eval(self.expresion))
                self.memoria += valor
                self.entrada_texto.set(f"M+ ({self.memoria})")
        except:
            self.entrada_texto.set("Error")
    
    def memoria_restar(self):
        """Resta el valor actual de la memoria"""
        try:
            if self.expresion:
                valor = float(eval(self.expresion))
                self.memoria -= valor
                self.entrada_texto.set(f"M- ({self.memoria})")
        except:
            self.entrada_texto.set("Error")
    
    def memoria_recuperar(self):
        """Recupera el valor de la memoria"""
        self.expresion = str(self.memoria)
        self.entrada_texto.set(self.expresion)
    
    def memoria_limpiar(self):
        """Limpia la memoria"""
        self.memoria = 0
        self.entrada_texto.set("MC (0)")


def main():
    """Función principal para ejecutar la calculadora"""
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Made with Bob
