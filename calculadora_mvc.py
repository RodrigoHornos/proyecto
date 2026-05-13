#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora Científica con Arquitectura MVC
Punto de entrada principal de la aplicación
"""

import tkinter as tk
from views import CalculatorView
from controllers import CalculatorController


def main():
    """
    Función principal que inicializa la aplicación con arquitectura MVC
    
    Flujo de inicialización:
    1. Crear ventana raíz de Tkinter
    2. Crear la Vista (CalculatorView)
    3. Crear el Controlador (CalculatorController)
    4. El Controlador crea los Modelos (CalculatorModel, MemoryModel)
    5. El Controlador conecta Vista y Modelos
    6. Iniciar el loop de eventos de Tkinter
    """
    # Crear ventana raíz
    root = tk.Tk()
    
    # Crear vista
    view = CalculatorView(root)
    
    # Crear controlador (conecta vista y modelos)
    controller = CalculatorController(view)
    
    # Iniciar aplicación
    root.mainloop()


if __name__ == "__main__":
    main()

# Made with Bob
